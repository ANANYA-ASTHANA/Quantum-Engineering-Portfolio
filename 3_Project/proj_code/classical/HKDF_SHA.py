import numpy as np
from hashlib import sha3_256
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

def bits_to_bytes(bits: np.ndarray) -> bytes:
    """
    bits: 1D np.array of 0/1 (dtype uint8 or bool)
    returns: bytes packed MSB→LSB within each byte (np.packbits convention)
    """
    bits = np.asarray(bits, dtype=np.uint8).flatten()
    if bits.size % 8 != 0:
        raise ValueError(f"Bit length must be multiple of 8, got {bits.size}")
    packed = np.packbits(bits)         # each group of 8 bits → 1 byte
    return packed.tobytes()


def bytes_to_bits(b: bytes) -> np.ndarray:
    """
    b: bytes
    returns: 1D np.array of 0/1 (dtype=uint8), length = 8 * len(b)
    """
    arr = np.frombuffer(b, dtype=np.uint8)
    bits = np.unpackbits(arr)
    return bits.astype(np.uint8)

def hkdf_sha3(master_bits: np.ndarray, num_keys: int, key_len_bits: int = 256, salt: bytes = b"", info: bytes = b"QKD-HKDF"):
    """
    Derives multiple session keys using HKDF-SHA3-256.
    master_bits: np.array of 0/1 (PA output)
    num_keys: how many session keys to derive
    key_len_bits: typically 256 for AES-256
    returns: list of np.array bits, each of length key_len_bits
    """
    key_len_bytes = key_len_bits // 8
    total_len_bytes = num_keys * key_len_bytes

    ikm = bits_to_bytes(master_bits)

    hkdf = HKDF(
        algorithm=hashes.SHA3_256(),
        length=total_len_bytes,  # Generate all keys at once
        salt=salt or None,
        info=info,
        backend=default_backend()
    )
    okm = hkdf.derive(ikm)  # bytes
    
   # Split into per-session-key bytes → bits
    keys_bits = []
    for i in range(num_keys):
        chunk = okm[i*key_len_bytes:(i+1)*key_len_bytes]
        bits = bytes_to_bits(chunk)      # np.array of 0/1, length = key_len_bits
        keys_bits.append(bits)

    return keys_bits

