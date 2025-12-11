from cqc.pythonLib import CQCConnection
import json
import random
import time

def bob_e91(num_bits=7000):
    raw_key_bits = []
    bob_bases = []
    with CQCConnection("Bob") as Bob:
        for _ in range(num_bits):
            # Receive entangled qubit
            q = Bob.recvEPR()
            #print("EPR Pair generated!")
            # Choose a random measurement basis: Z (0), X (1), or Y (2)
            basis = random.choice([0, 1, 2])
            bob_bases.append(basis)
            #print("Basis selected!")
            # Apply corresponding transformation
            if basis == 1:
                q.H()  # X-basis
            elif basis == 2:
                q.K()  # Y-basis 
                
            # Measure the qubit
            qb = q.measure()
            # Fix up bit depending on basis and entangled state
            if basis == 2:   # Y-basis
            # For |Phi+>, Y outcomes are anti-correlated ⇒ flip Bob's bit
                qb ^= 1     # qb = qb ^ 1
            raw_key_bits.append(qb)
            #print("Qubit measured!")
            #q.release()
            # Send basis choice to Alice
            #Bob.sendClassical("Alice", basis)
            #print("Basis sent to Alice!")
        print(f"Everything done! Raw key length: {len(raw_key_bits)} bits")
    
    # Receive Alice's basis choices
    alice_bases = Bob.recvClassical(msg_size=7000)
    print(f"Alice's Bases Length: {len(alice_bases)} bits")
    
    # Send basis choice to Alice
    Bob.sendClassical("Alice", bob_bases)
    print(f"Bases sent to Alice! Bases length: {len(bob_bases)} bits")
    
    # Perform key sifting: Keep only bits where bases match
    sifted_key = [raw_key_bits[i] for i in range(num_bits) if alice_bases[i] == bob_bases[i]]
    sifted_key_bases = [bob_bases[i] for i in range(num_bits) if alice_bases[i] == bob_bases[i]]
    print(f"Bob's Sifted Key Length: {len(sifted_key)} bits")
    #print(f"Bob's Sifted Key: {sifted_key}")
    #print(f"Bob's Sifted Key Bases: {sifted_key_bases}")
    # Wait for Alice's messages
    #time.sleep(4)

    # Receive test bit indices and values from Alice
    print("[Bob] Waiting to receive test indices from Alice...")
    test_indices = json.loads(Bob.recvClassical(msg_size=4096).decode())
    print("Test indices received!")
    print(f"Received indices: {test_indices}")
    print("[Bob] Sending acknowledgement for test indices...")
    Bob.sendClassical("Alice", [1])
    print("[Bob] Acknowledgement sent.")
    #time.sleep(2)
    print("[Bob] Waiting to receive Alice's test bits...")
    alice_test_bits = Bob.recvClassical()
    print("Test bits received!")
    print(f"Received test bits: {alice_test_bits}")
    # Extract corresponding test bits from Bob's sifted key
    bob_test_bits = [sifted_key[i] for i in test_indices]

    # Send Bob's test bits to Alice
    Bob.sendClassical("Alice", bob_test_bits)
    print("Test bits sent!")
    print(f"Test bits: {bob_test_bits}")
    # Compute QBER (Quantum Bit Error Rate)
    errors = sum(1 for a, b in zip(alice_test_bits, bob_test_bits) if a != b)
    qber = errors / len(test_indices) if test_indices else 0  # Avoid division by zero

    print(f"Bob's Computed QBER: {qber * 100:.2f}%")

    # If QBER exceeds threshold, abort key generation
    if qber > 0.05:  # Threshold set based on project scenario
        print("High QBER detected! Possible eavesdropping or noise. Aborting QKD.")
        return None

    # Remove test bits and keep final raw key
    final_raw_key = [sifted_key[i] for i in range(len(sifted_key)) if i not in test_indices]

    print(f"Bob's Final Raw Key ({len(final_raw_key)} bits)")

    return final_raw_key  # Return all remaining bits

if __name__ == "__main__":
    bob_e91()

