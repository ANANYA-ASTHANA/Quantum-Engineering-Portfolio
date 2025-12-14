import numpy as np
import random
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.circuit.library import XXPlusYYGate

def tf_input_state(delta_phi: float) -> Statevector:
    """
    Ideal single-photon-like TF input:
      (|10> + e^{iΔφ}|01>) / sqrt(2)
    Qiskit basis order: |q1 q0> => indices: |00|01|10|11 = 0,1,2,3
    """
    v = np.zeros(4, dtype=complex)
    v[2] = 1/np.sqrt(2)                      # |10>
    v[1] = np.exp(1j*delta_phi)/np.sqrt(2)   # |01>
    return Statevector(v)

def beamsplitter_circuit(theta=np.pi/4, phi=0.0) -> QuantumCircuit:
    """
    Ideal 50:50 beamsplitter-like mode mixer on 2 qubits.
    theta = pi/4 gives 50:50 mixing.
    """
    qc = QuantumCircuit(2, name="BS_ideal")
    qc.append(XXPlusYYGate(2*theta, phi), [0, 1])
    return qc

def tf_central_node(delta_phi: float):
    psi_in = tf_input_state(delta_phi)
    qc_bs = beamsplitter_circuit(theta=np.pi/4, phi=0.0)

    psi_out = psi_in.evolve(qc_bs)
    probs = psi_out.probabilities_dict()

    p01 = probs.get("01", 0.0)
    p10 = probs.get("10", 0.0)
    p_other = 1.0 - (p01 + p10)

    outcome = random.choices(["01", "10", "other"], weights=[p01, p10, p_other], k=1)[0]
    return outcome, {"01": p01, "10": p10, "other": p_other, "full": probs}, qc_bs

if __name__ == "__main__":
    for dphi in [0, np.pi/2, np.pi, 3*np.pi/2]:
        out, p, qc = tf_central_node(dphi)
        print(qc.draw(fold=-1))
        print(f"Δφ={dphi:.2f} | P(01)={p['01']:.4f}, P(10)={p['10']:.4f}, sampled={out}\n")

