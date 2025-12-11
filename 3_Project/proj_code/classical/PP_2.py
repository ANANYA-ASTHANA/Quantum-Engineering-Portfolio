#### **Bob's KR, PA and KDF Processes (PP_2.py)**

import socket
import numpy as np
import pyldpc
import pickle
from cryptomite.trevisan import Trevisan # For PA and KDF
from random import randint
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes # For data encryption
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC 
from cryptography.hazmat.primitives import hashes
import HKDF_SHA 

def receive_large_data(ip, port):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind((ip, port))
    print(f"Bob: Listening for incoming data on {ip}:{port}")
    expected_chunks = 32785
    received_data = bytearray()
    for i in range(expected_chunks):
        chunk, _ = udp_socket.recvfrom(2048)
        print(f"Bob: Received chunk {i+1}/{expected_chunks}")
        if not chunk:
            break
        received_data.extend(chunk)
    
    udp_socket.close()
    return pickle.loads(received_data)

def receive_small_data(ip, port):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind((ip, port))
    print(f"Bob: Listening for incoming data on {ip}:{port}")
    expected_chunks = 121
    received_data = bytearray()
    for i in range(expected_chunks):
        chunk, _ = udp_socket.recvfrom(2048)
        print(f"Bob: Received chunk {i+1}/{expected_chunks}")
        if not chunk:
            break
        received_data.extend(chunk)
    
    udp_socket.close()
    return pickle.loads(received_data)

# Derive a 256-bit key from the pre-shared key
def derive_key(pre_shared_key: bytes):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), 
        length=32,  # 256-bit key
        salt=b'some_salt', 
        iterations=100000
    )
    return kdf.derive(pre_shared_key)

def decrypt_data(iv, ciphertext, tag, key):
    """Decrypts data using AES GCM"""
    try:
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag))
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
        return decrypted_data

    except Exception as e:
        raise ValueError(f"Decryption failed: {e}. Possible data tampering detected!")

def split_into_session_keys(final_key, session_key_size=256):
    """Splits final key into multiple 256-bit session keys"""
    num_keys = len(final_key) // session_key_size  # Number of full session keys
    session_keys = [final_key[i * session_key_size:(i + 1) * session_key_size] for i in range(num_keys)]
    
    return session_keys

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

def bob_main():
    pre_shared_key = b"secure_qkd_key"
    
    # Ensure the key is of valid size for AES (e.g., 256 bits for AES-256)
    aes_key = derive_key(pre_shared_key)
    
    # Receive Data from Alice
    data_received = receive_large_data("127.0.0.1", 8080)
    print("Proceeding to extracting every data received...")
    iv_H_from_alice = data_received["iv_H"] # Received IV for H
    iv_encoded_key_from_alice = data_received["iv_encoded_key"]  # Received IV for the encoded key
    ciphertext_H_from_alice = data_received["ciphertext_H"]  # Received ciphertext for H
    ciphertext_encoded_key_from_alice = data_received["ciphertext_encoded_key"] # Received ciphertext for the encoded key
    tag_H_from_alice = data_received["tag_H"]  # Received tag for H
    tag_encoded_key_from_alice = data_received["tag_encoded_key"]  # Received tag for the encoded key
    

    try:
        print("Decrypting and verifying H matrix...")
        decrypted_H = np.frombuffer(decrypt_data(iv_H_from_alice, ciphertext_H_from_alice, tag_H_from_alice, aes_key), dtype=np.int64).reshape(2048, 4096)
        
        print("Decrypting and verifying encoded key...")
        decrypted_encoded_key = np.frombuffer(decrypt_data(iv_encoded_key_from_alice, ciphertext_encoded_key_from_alice, tag_encoded_key_from_alice, aes_key), dtype=np.float64)
       
        print("Bob's Recovered Encoded Key:", decrypted_encoded_key)
        print("Decryption successful!")
    
    except ValueError as e:
        print("Error:", e)

    # Apply BP-based error correction
    decoded_key = pyldpc.decode(decrypted_H, decrypted_encoded_key, snr = 10, maxiter = 2000)
    final_decoded_key = decoded_key[:2051]  # Select 2051 bits of the decoded reconciled key
    print("Bob: Successfully decoded key.")
      
    # Send confirmation to Alice
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.sendto(b"Key successfully reconciled!", ("127.0.0.1", 8081))
    print("Bob: Sent confirmation to Alice.")
    
    udp_socket.close()
    print(f"Reconciled Key Length: {len(final_decoded_key)}")

    # Implement PA using Trevisan's Extractor
    ext = Trevisan(len(final_decoded_key), 1974, 0.01) # Initializing Trevisan's extractor with input length k and extractor error capped at 1% 

    # Receive encrypted seed from Alice
    seed_data_received = receive_small_data("127.0.0.1", 8080)

    # Extract IV, ciphertext, and tag
    iv_seed_from_alice = seed_data_received["iv_seed"]
    ciphertext_seed_from_alice = seed_data_received["ciphertext_seed"]
    tag_seed_from_alice = seed_data_received["tag_seed"]

    # Decrypt the seed bits
    decrypted_seed_bits_bytes = decrypt_data(iv_seed_from_alice, ciphertext_seed_from_alice, tag_seed_from_alice, aes_key)

    # Convert back to list of bits
    decrypted_seed_bits = list(np.frombuffer(decrypted_seed_bits_bytes, dtype=np.uint8))

    print("Bob: Successfully received and decrypted seed bits.")

    # Use decrypted seed bits in PA
    output_bits = ext.extract(final_decoded_key, decrypted_seed_bits)
    final_bits = np.array(output_bits).astype(int)
    print("Compressed Key Length:", len(final_bits))

    # Dual KDF Path for session-key generation
    final_keys = KDF(final_bits, True)
    
    # Split derived key into 256-bits session keys
    session_keys = split_into_session_keys(final_keys)

    # Print each session key (for validation in demo only)
    for idx, key in enumerate(session_keys, start=1):
        print(f"Session Key {idx}: {key}")
    
if __name__ == "__main__":
    bob_main()

