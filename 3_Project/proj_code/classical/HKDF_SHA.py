import secrets
from hashlib import sha3_256
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

def hkdf_sha3(raw_key, salt, info, length, num_keys):
    """Derives multiple session keys using HKDF-SHA3."""
    hkdf = HKDF(
        algorithm=hashes.SHA3_256(),
        length=length * num_keys,  # Generate all keys at once
        salt=salt,
        info=info,
        backend=default_backend()
    )
    derived_keys = hkdf.derive(raw_key)
    
    # Split derived material into num_keys session keys
    return [derived_keys[i * length:(i + 1) * length] for i in range(num_keys)]

# Example usage
raw_key = secrets.token_bytes(128)  # Example raw key (128 bytes)
salt = secrets.token_bytes(16)      # Example salt (16 bytes)
info = b"session_info"              # Additional context info
num_keys = 5                         # Number of session keys to derive
session_keys = hkdf_sha3(raw_key, salt, info, 32, num_keys)  # Each 256-bit key

for i, key in enumerate(session_keys):
    print(f"Session Key {i+1}: {''.join(format(byte, '08b') for byte in key)}")
