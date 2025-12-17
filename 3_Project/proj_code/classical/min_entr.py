from collections import Counter
import numpy as np

def compute_min_entropy(keys):
    """Computes min-entropy based on the most likely full key sequence."""
    key_counts = Counter(map(tuple, keys))  # Count unique key sequences
    total_keys = len(keys)
    
    # Find the probability of the most common sequence
    P_max = max(key_counts.values()) / total_keys
    
    # Compute min-entropy
    H_min = -np.log2(P_max)
    
    return H_min

# Example: If your keys are stored in a list as binary arrays
keys = np.random.randint(0, 2, (1000000, 2051))  # Simulating 1000000 keys of 2051 bits each
min_entropy = compute_min_entropy(keys)
print(f"Min-Entropy: {min_entropy} bits")
