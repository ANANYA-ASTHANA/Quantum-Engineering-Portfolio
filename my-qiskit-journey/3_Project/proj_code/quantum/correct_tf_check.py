from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator
from qiskit.circuit.library import RYGate
import numpy as np

# Define beamsplitter using Hamiltonian-based approach in Qiskit
def beamsplitter_hamiltonian(theta=np.pi/4):
    qc = QuantumCircuit(2)
    """qc.append(RYGate(2 * theta), [0])  # Rotation equivalent to BS interaction
    qc.cx(0, 1)  # Entangling interaction
    qc.append(RYGate(-2 * theta), [0])  # Reverse rotation"""
     # First mixing operation
    qc.append(RYGate(2 * theta), [0])  # Beam splitter effect on qubit 0
    
    # Introduce interaction
    qc.cx(0, 1)  
    
    # Ensure correct phase relation
    qc.append(RYGate(theta), [1])  # Add phase correction on qubit 1
    
    # Final mixing (Hadamard better models a true beam splitter)
    qc.h(0)
    qc.h(1)
    return qc

# Define beamsplitter using gate-based approach (CNOT + H + CZ + H + CNOT)
def beamsplitter_gate_based_revised():
    qc = QuantumCircuit(2)
    # Apply Hadamard on both qubits to create superposition
    qc.h(0)
    qc.h(1)
    
    # Apply Phase Shift to adjust amplitudes
    qc.t(0)
    qc.tdg(1)
    
    # Apply Controlled-Z to introduce entanglement (optical interference)
    qc.cz(0, 1)
    
    # Apply Hadamard again to finalize the interference
    qc.h(0)
    qc.h(1)

    # Apply global phase correction by modifying the global_phase attribute directly
    qc.global_phase = -np.pi/8
  
    return qc

# Get the unitary matrices
unitary_hamiltonian = Operator(beamsplitter_hamiltonian()).data
unitary_gate_based = Operator(beamsplitter_gate_based_revised()).data

# Compute the difference
difference = np.round(unitary_hamiltonian - unitary_gate_based, 8)

print("Hamiltonian-based Unitary:\n", unitary_hamiltonian)
print("\nGate-based Unitary:\n", unitary_gate_based)
print("\nDifference:\n", difference)
