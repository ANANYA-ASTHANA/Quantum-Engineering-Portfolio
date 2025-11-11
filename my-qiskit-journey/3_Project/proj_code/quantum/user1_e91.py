from cqc.pythonLib import CQCConnection
import json
import random
import time
import zmq

def send_raw_key(raw_key):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://127.0.0.1:5555")

    print("[user1_e91] Sending raw key...")
    socket.send_string(raw_key)

    # Optional: Wait for ACK from PP_1
    message = socket.recv_string()
    print(f"[user1_e91] Received reply: {message}")

def alice_e91(num_bits=7000):
    raw_key_bits = []
    alice_bases = []
    with CQCConnection("Alice") as Alice:
        for _ in range(num_bits):
            q = Alice.createEPR("Bob")  # Create entangled qubit
            #print("EPR Pair generated!")
            # Choose a random measurement basis: Z (0), X (1), or Y (2)
            basis = random.choice([0, 1, 2])
            alice_bases.append(basis)
            #print("Basis selected!")
            # Apply corresponding transformation for measurement
            if basis == 1:
                q.H()  # X-basis
            elif basis == 2:
                q.H()  # Y-basis
                q.Y()      # Y gate   

            # Measure the qubit
            raw_key_bits.append(q.measure())
            #print("Qubit measured!")
            #q.release()
            # Send basis choice to Bob
            #Alice.sendClassical("Bob", basis)
            #print("Basis sent to Bob!")
        print(f"Everything done! Raw key length: {len(raw_key_bits)} bits")

    # Send basis choice to Bob
    Alice.sendClassical("Bob", alice_bases)
    print(f"Bases sent to Bob! Bases length: {len(alice_bases)} bits")
    
    # Wait for Bob's measurements
    time.sleep(2)

    # Receive Bob's basis choices
    bob_bases = Alice.recvClassical(msg_size=7000)
    print(f"Bob's Bases Length: {len(bob_bases)} bits")
    
    # Perform key sifting (keep bits where bases matched)
    sifted_key = [raw_key_bits[i] for i in range(num_bits) if alice_bases[i] == bob_bases[i]]
    sifted_key_bases = [alice_bases[i] for i in range(num_bits) if alice_bases[i] == bob_bases[i]]
    print(f"Alice's Sifted Key Length: {len(sifted_key)} bits")
    #print(f"Alice's Sifted Key: {sifted_key}")
    #print(f"Alice's Sifted Key Bases: {sifted_key_bases}")
    # Select test bits
    test_indices = random.sample(range(len(sifted_key)), len(sifted_key) // 10)  # 10% for testing
    test_bits = [sifted_key[i] for i in test_indices]

    # Send test bit indices and values to Bob
    #time.sleep(2)
    print(f"[Alice] Test indices: {test_indices}") 
    Alice.sendClassical("Bob", json.dumps(test_indices).encode())
    print("Test indices sent!")
    #time.sleep(2)
    print("[Alice] Waiting for Bob’s acknowledgement...")
    handshake = Alice.recvClassical()
    print("[Alice] Acknowledgement received.")
    print("[Alice] Sending test bits to Bob...")
    Alice.sendClassical("Bob", test_bits)
    print("Test bits sent!")
    print(f"Test bits: {test_bits}")
    # Wait for Bob's message
    time.sleep(2)

    # Receive Bob's corresponding test bits
    bob_test_bits = Alice.recvClassical()
    print("Test bits received!")
    print(f"Received test bits: {bob_test_bits}")
    # Compute QBER (Quantum Bit Error Rate)
    errors = sum(1 for a, b in zip(test_bits, bob_test_bits) if a != b)
    qber = errors / len(test_indices) if test_indices else 0  # Avoid division by zero

    print(f"Alice's Computed QBER: {qber * 100:.2f}%")

    # If QBER exceeds threshold, abort key generation
    if qber > 0.05:  # Threshold set based on project scenario
        print("High QBER detected! Possible eavesdropping or noise. Aborting QKD.")
        return None

    # Remaining sifted key after test bit removal
    final_raw_key = [sifted_key[i] for i in range(len(sifted_key)) if i not in test_indices]
    print(f"Alice's Final Raw Key ({len(final_raw_key)} bits)")
    # Convert to string
    raw_key_str = str(final_raw_key)  # Ensures it's "[0, 1, 1, 0, ...]"
    time.sleep(1)  # Small delay to ensure server starts
    send_raw_key(raw_key_str) # Send raw key to PP_1.py for key post processing

    return raw_key_str  # Return all remaining bits

if __name__ == "__main__":
    alice_e91()
