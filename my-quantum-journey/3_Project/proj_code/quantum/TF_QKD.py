from qiskit import QuantumCircuit
from qiskit.circuit.library import RYGate
import numpy as np

def enhanced_beamsplitter(theta=np.pi/4):
    print("Function started!")
    qc = QuantumCircuit(2, name="BeamSplitter")
    print("Qubits initialized!")
    # Initial amplitude mixing on qubit 0
    qc.append(RYGate(2 * theta), [0])  # Partial mixing
    print("Amplitude of Qubit 0 mixed!")
    # Add relative phase shift before entangling
    qc.s(0)  # Adds a π/2 phase (i) to match optical matrix
    qc.sdg(1)  # Inverse phase on other path to mimic interference
    print("Relative phase shifts added!")
    # Interaction (simulating Hong-Ou-Mandel style interference)
    qc.cx(0, 1)
    print("Qubits interacted!")
    # Corrective phase adjustment
    qc.t(1)  # Add π/4 phase to refine interference model
    print("Phase of Qubit 1 adjusted!")
    # Final interference layer (balanced 50/50 mixing)
    qc.h(0)
    qc.h(1)
    print("Mixing balanced!")
    
    print(qc)
    return qc
   
enhanced_beamsplitter()
