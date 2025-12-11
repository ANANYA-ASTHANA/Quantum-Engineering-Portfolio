### NS-3 Compatible Key Reconciliation with LDPC (BP-based Decoding), PA and KDF 

#### **Alice's KR, PA and KDF Processes (PP_1.py)**

import socket
import numpy as np
import pickle
import pyldpc  # For working with LDPC codes
import json
import time
from cryptomite.trevisan import Trevisan # For PA and KDF
from random import randint
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes # For data encryption
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC 
from cryptography.hazmat.primitives import hashes
import HKDF_SHA
import zmq

def generate_ldpc_matrices(n, d_v, d_c):
    # Generate LDPC matrices manually 
    H, G = pyldpc.make_ldpc(n, d_v, d_c, systematic = True, seed = 42)
    return H, G

def start_zmq_server():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://127.0.0.1:5555")

    print("[PP_1] Waiting for raw key...")
    message = socket.recv_string()  # Receive one message
    socket.send_string("Key received!")  # Optional ACK

    return message  # Return the raw key

def send_data(data, ip, port):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Split the data into smaller chunks
    serialized_data = pickle.dumps(data)
    chunk_size = 2048  # Adjust the chunk size based on your network's MTU
    total_chunks = (len(serialized_data) + chunk_size - 1) // chunk_size  # Calculate number of chunks
    print(total_chunks)
    # Send each chunk sequentially
    for i in range(total_chunks):
        start_idx = i * chunk_size
        end_idx = min((i + 1) * chunk_size, len(serialized_data))
        udp_socket.sendto(serialized_data[start_idx:end_idx], (ip, port))
        print(f"Alice: Sent chunk {i + 1}/{total_chunks}")
        time.sleep(0.005)
    
    udp_socket.close()

# Derive a 256-bit key from the pre-shared key
def derive_key(pre_shared_key: bytes):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), 
        length=32,  # 256-bit key
        salt=b'some_salt', 
        iterations=100000
    )
    return kdf.derive(pre_shared_key)

def encrypt_data(data, key):
    iv = os.urandom(12)  # Generate a random IV for this encryption
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(data) + encryptor.finalize()
    return iv, ciphertext, encryptor.tag

def split_into_session_keys(final_key, session_key_size=256):
    """Splits final key into multiple 256-bit session keys"""
    num_keys = len(final_key) // session_key_size  # Number of full session keys
    session_keys = [final_key[i * session_key_size:(i + 1) * session_key_size] for i in range(num_keys)]
    
    return session_keys

def write_session_keys_to_file(session_keys, filename="session_keys.py"):
    with open(filename, "w") as f:
        f.write("session_keys = [\n")
        for key in session_keys:
            f.write(f"    {key.tolist()},\n")  # Convert NumPy array to a list
        f.write("]\n")

def KDF(master_key, switch=False):
    if switch==True:
        session_keys = HKDF_SHA.hkdf_sha3(master_key, 12)
        # Concatenate into a single 1-D vector
        session_vec = np.concatenate(session_keys).astype(int)
    else:
        # Double usage of Trevisan's extractor (for KDF)
        ext_KDF = Trevisan(len(master_key), len(master_key), 0.01)

        # Generate the seed length dynamically for KDF
        seed_length_KDF = ext_KDF.ext.get_seed_length()

        # Generate `seed_bits_KDF` from PA output using SHAKE-256
        shake_kdf = hashes.Hash(hashes.SHAKE256(seed_length_KDF // 8))
        shake_kdf.update(master_key.tobytes())
        seed_bits_KDF = list(bin(int.from_bytes(shake_kdf.finalize(), "big"))[2:].zfill(seed_length_KDF))
        seed_bits_KDF = [int(bit) for bit in seed_bits_KDF]

        # Perform KDF using Trevisan
        kdf_output = ext_KDF.extract(master_key, seed_bits_KDF)
        session_vec = np.array(kdf_output).astype(int)

    return session_vec

def alice_main():
    n = 4096  # Code length
    d_v = 4  # Variable node degree
    d_c = 8  # Check node degree
    
    # Generate H and G matrices and encode key using G matrix
    H, G = generate_ldpc_matrices(n, d_v, d_c)
    k = G.shape[1]  # Extracting correct message length 
    #raw_key = np.random.randint(0, 2, k)  # Example raw key for demo purpose
    message = start_zmq_server()
    bit_array = np.array(json.loads(message), dtype=np.uint8)
    raw_key = bit_array[:2051]  # Select 2051 bits of the sifted key
    encoded_key = pyldpc.encode(G, raw_key, snr = 10, seed = 42)
    encoded_key_bytes = encoded_key.astype(np.float64).tobytes()
    # A mutually agreed upon pre-shared key (confidential between the two parties)
    pre_shared_key = b"secure_qkd_key"

    # Ensure the key is of valid size for AES (e.g., 256 bits for AES-256)
    aes_key = derive_key(pre_shared_key)
    
    # Encrypt the H matrix with a unique IV for H
    iv_H, ciphertext_H, tag_H = encrypt_data(H.tobytes(), aes_key)

    # Encrypt the encoded key with a unique IV for the encoded key
    iv_encoded_key, ciphertext_encoded_key, tag_encoded_key = encrypt_data(encoded_key_bytes, aes_key)


    # Send the Data in chunks to Bob
    data_to_send = {"iv_H": iv_H,
    "iv_encoded_key": iv_encoded_key,
    "ciphertext_H": ciphertext_H,
    "ciphertext_encoded_key": ciphertext_encoded_key,
    "tag_H": tag_H,
    "tag_encoded_key": tag_encoded_key}
    send_data(data_to_send, "127.0.0.1", 8080)  # Bob's IP in NS-3
    print("Alice's Original Encoded Key:", encoded_key)
    
    # Wait for Bob's confirmation after decoding
    print("Proceeding to receive confirmation...")
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("127.0.0.1", 8081))  # Alice's receiving port
    print("Successfully bound to port!")
    confirmation, _ = udp_socket.recvfrom(1024)
    print("Alice: Received confirmation from Bob -", confirmation.decode())
    

    # Implement PA using Trevisan's Extractor
    ext = Trevisan(k, 1974, 0.01) # Initializing Trevisan's extractor with input length k and extractor error capped at 1% 
    seed_bits = [randint(0, 1) for _ in range(ext.ext.get_seed_length())] # Seed of length calculated from Trevisan's initializer

    # Convert seed_bits to bytes for encryption
    seed_bits_bytes = np.array(seed_bits, dtype=np.uint8).tobytes()

    # Encrypt the seed bits
    iv_seed, ciphertext_seed, tag_seed = encrypt_data(seed_bits_bytes, aes_key)

    # Send the encrypted seed to Bob
    seed_data = {
        "iv_seed": iv_seed,
        "ciphertext_seed": ciphertext_seed,
        "tag_seed": tag_seed
    }
    send_data(seed_data, "127.0.0.1", 8080)  # Send to Bob
    print("Alice: Sent encrypted seed bits to Bob.")

    # Generating Final Master Key
    output_bits = ext.extract(raw_key, seed_bits) # Extract a compressed key from Original key (using seed)
    final_bits = np.array(output_bits).astype(int)
    print("Compressed Key Length:", len(final_bits))

    # Dual KDF Path for session-key generation
    final_keys = KDF(final_bits, True)

    # Split derived key into 256-bit session keys
    session_keys = split_into_session_keys(final_keys)

    # Print each session key (for validation in demo only)
    for idx, key in enumerate(session_keys, start=1):
        print(f"Session Key {idx}: {key}")

    # Store the session keys for data encryption in the classical channel
    write_session_keys_to_file(session_keys)
    print(f"Session keys successfully written.")

    
if __name__ == "__main__":
    alice_main()
