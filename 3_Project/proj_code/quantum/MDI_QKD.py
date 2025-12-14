from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import random

def bell_state_measurement_circuit():
    qc = QuantumCircuit(2)
    qc.cx(0, 1)
    qc.h(0)
    return qc

def simulate_bsm(alice_state, bob_state):
    print("\nCharlie's Bell-State Measurement process begins...")

    # Combine states: Alice (qubit 0) and Bob (qubit 1)
    combined = alice_state.tensor(bob_state)
    print("Combined statevector created.")

    # Apply Bell-state measurement circuit
    qc = bell_state_measurement_circuit()
    final_state = combined.evolve(qc)
    probs = final_state.probabilities_dict()

    print("Charlie's final state probabilities after BSM:")
    for outcome, prob in probs.items():
        print(f"Outcome {outcome}: {prob:.4f}")

    # Simulate a single measurement outcome based on probabilities
    outcome = random.choices(list(probs.keys()), weights=list(probs.values()), k=1)[0]
    print(f"\nCharlie's measured outcome (simulated): {outcome}")
    return outcome

def prepare_qubit(bit, basis):
    qc = QuantumCircuit(1)
    if basis == 'X':
        if bit == 1:
            qc.x(0)
        qc.h(0)
    elif basis == 'Z':
        if bit == 1:
            qc.x(0)
    return Statevector.from_instruction(qc)

# Alice and Bob choose random bits and bases
alice_bit, alice_basis = random.randint(0,1), random.choice(['X', 'Z'])
bob_bit, bob_basis = random.randint(0,1), random.choice(['X', 'Z'])

print(f"Alice chooses bit {alice_bit} in {alice_basis} basis.")
print(f"Bob chooses bit {bob_bit} in {bob_basis} basis.")

# Prepare qubits
alice_qubit = prepare_qubit(alice_bit, alice_basis)
bob_qubit = prepare_qubit(bob_bit, bob_basis)

# Charlie performs BSM
simulate_bsm(alice_qubit, bob_qubit)
