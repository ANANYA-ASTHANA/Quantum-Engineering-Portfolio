# Quantum–Classical Secure Communication Architecture for 6G Networks
### **Project Summary**
_(Based on Bachelor's Major Project, titled "Future-proofing 6G Networks: A Quantum Approach")_

---

## **1. Abstract**

The rise of quantum computing threatens the security foundation of classical cryptographic systems, while emerging 6G networks introduce unprecedented performance demands across hyper-connected military and government infrastructures. This project develops a hybrid quantum–classical secure communication architecture that integrates **Quantum Key Distribution (QKD)** with **AES-256** in a simulated **6G network**, implemented using **SimulaQron/Qiskit**, **NS-3**, and a custom **Flask-based web system**. The architecture includes multi-layer QKD support (E91, TF-QKD, MDI-QKD), LDPC-based Key Reconciliation (KR), Trevisan-based Privacy Amplification (PA), HKDF/extractor-based Key Derivation Function (KDF) for session key generation, SDN-driven adaptive network modulation, and real-time network visualization. Results show that the proposed system enables reliable quantum key generation, stable AES-256 encrypted communication in realistic channel conditions, and effective anomaly detection across a hierarchical military-grade network. The work demonstrates a feasible, modular, and extendable blueprint for quantum-secured 6G communication infrastructures.

---

## **2. Motivation & Problem Context**

Next-generation networks will need to defend against **quantum-powered attacks** while providing **ultra-low latency** and **high-reliability** communication for critical infrastructures. Classical encryption (RSA, ECC) becomes vulnerable under Shor’s algorithm [1], threatening government, military, and globally distributed core networks. Simultaneously, 6G networks will support massive device densities, mission-critical systems, and quantum-integrated services.

This project is motivated by:

- The imminent need for **quantum-resilient security architectures** [2]
- The gap between theoretical QKD protocols and **realistic network-level integration**
- The lack of simulation frameworks combining **quantum protocols, classical 6G features, and real-time network behavior**

The goal is to design a hybrid architecture that demonstrates **how QKD can be operationalized inside a real, functioning network**, not just theoretically analyzed.

---

## **3. System Architecture Overview**

The system is divided into four tightly integrated layers:

---

### **3.1 Quantum Layer**

Implements multi-protocol QKD:

- **E91** for high-security Cabinet $\leftrightarrow$ HQ links [3]
- **TF-QKD** for long-range HQ $\leftrightarrow$ Regional Base Station links [4] 
- **MDI-QKD** for hardware-attack-resistant inter-base communication [5] 

The quantum layer handles raw-key generation, sifting, QBER estimation, and secure transfer of sifted keys to the classical layer via ZeroMQ.

---

### **3.2 Classical Layer (6G Simulation)**

Implemented using NS-3 with:

- THz/mmWave-like channel characteristics  
- Hierarchical subnets reflecting military layers  
- SDN-driven adaptive modulation (BPSK $\rightarrow$ 1024-QAM based on SNR)  
- Real-time channel metrics (SNR, BER, Load, Packet Loss)  
- Anomaly detection (threshold-based behavioral deviations)  

Nodes exchange AES-256 encrypted messages using session keys derived from QKD.

---

### **3.3 Integration Layer (Quantum → Classical Pipeline)**

The bridge manages:

- Raw key transfer (ZeroMQ REQ–REP)  
- LDPC-based key reconciliation (pyLDPC) [6]
- Privacy amplification (Trevisan’s extractor) for master-key compression [7]
- AES session-key derivation via Trevisan's extractor (double usage)/HKDF-SHA256 (efficient KDF alternative to Trevisan) [8]
- Secure (session) key propagation to backend communication layers  

Together, this creates an end-to-end secure pipeline from quantum measurement $\rightarrow$ key derivation $\rightarrow$ encrypted classical transmission.

---

### **3.4 Web Application Layer (Flask-Based Secure Portal)**

A Flask-based web interface provides user-facing functionality:

- **Multi-Factor Authentication** (password + QKD-challenge),  
- **AES-256-encrypted chat rooms** using session keys from the Integration Layer,  
- **Role-based access control** (users vs. admin),  
- **Real-time NS-3 dashboard** showing SNR, BER, anomalies, and link state (admin only),  
- **Session-key refresh** upon network state changes or on-demand.

This layer demonstrates how quantum-derived entropy can be integrated into operational communication systems.

---

## **4. Methodology**

The project uses a three-pronged engineering + scientific methodology, combining experimental implementation, theoretical validation, and network modeling.

---

### **4.1 Experimental Methodology**

- Simulated QKD protocols in SimulaQron/Qiskit  
- Implemented KR, PA, and KDF via Python  
- Constructed a 6G-like classical network simulation in NS-3  
- Integrated AES-256 encryption and dynamic SDN logic  
- Built a multi-user Flask + Socket.IO communication platform  

This creates a functional prototype demonstrating the full security pipeline.

---

### **4.2 Theoretical/Algorithmic Methodology**

- Formal QKD foundations: E91, TF-QKD interference modeling, MDI-QKD security principles  
- QBER thresholding for eavesdropping detection  
- LDPC-based key reconciliation via belief-propagation  
- Privacy amplification using Trevisan’s extractor  
- Session key derivation using HKDF/entropy extraction  

These techniques ensure the system is cryptographically sound under quantum threats.

---

### **4.3 Modeling Methodology**

- Hierarchical military communication model  
- Simulation of long-range and hardware-attack-prone links  
- SDN-inspired dynamic modulation switching  
- Realistic classical noise modeling (SNR, BER, load patterns)  
- Real-time graph (network) visualization with PyVis  

Modeling ensures that the architecture reflects realistic 6G deployment constraints.

---

## **5. Key Implementations**

---

### **5.1 QKD Protocol Implementations**

#### **E91 (SimulaQron)**

- Random basis selection (Z/X/Y)  
- Entangled pair measurement  
- Basis reconciliation  
- 10% sample for QBER estimation  
- QBER ≤ 5% $\rightarrow$ key accepted (with sample bits removed), else entire key discarded  

#### **TF-QKD (Qiskit)**

- Simulated weak coherent pulses via gate-level approximation  
- Hamiltonian-based beam-splitter model in Qiskit  
- Interference simulation to mimic Charlie’s measurement  

#### **MDI-QKD (Qiskit)**

- Bell-State Measurement simulation  
- Independent qubit preparation (Alice/Bob)  
- BSM-based bit inference and sifting  

---

### **5.2 Quantum-to-Classical Key Transfer**

- ZeroMQ REQ–REP  
- Raw key $\rightarrow$ Classical post-processing  
- Secure ACK (Acknowledgement) exchanges  

---

### **5.3 Post-Processing Pipeline**

#### **Key Reconciliation (LDPC)**

- Parity-check matrix generation  
- LDPC encoding (Alice)  
- Belief-propagation decoding (Bob)  
- Encrypted matrix/bit transmission (AES-GCM)  

#### **Privacy Amplification**

- Trevisan’s extractor  
- AES-protected seed confidentiality  
- Master-key compression  

#### **Key Derivation**

- SHAKE-256 seed derivation  
- Extractor-based entropy expansion  
- Derivation of uniform 256-bit AES keys  

---

### **5.4 Classical Network Simulation**

- Multi-layer node architecture  
- SDN modulation control based on real-time SNR  
- Anomaly detection  
- PyVis-based interactive network visualization  

---

### **5.5 Web Application**

- MFA (Password + QKD-challenge) login  
- Layer-restricted communication  
- AES-256 encrypted messaging  
- Real-time NS-3 visualization for admins  
- Session-key deletion after use (prevents key reuse)

---

## **6. Results (Conceptual Summary)**

---

### **6.1 Quantum Layer Results**

- **E91 produced stable keys with QBER < 5%**, confirming correct entanglement correlations  
- **TF-QKD interference patterns matched expected behavior**, validating beam-splitter modeling  
- **MDI-QKD produced uniformly distributed Bell-state measurements**, confirming correct simulation  

All three protocols performed reliably in adversarial conditions.

---

### **6.2 Post-Processing Results**

- **LDPC successfully reconciled** raw keys held by involved parties
- **Trevisan-based PA produced high-entropy master keys**  
- **HKDF/extractor-derived session keys were uniform and AES-compatible**  

The pipeline consistently produced synchronized keys for both parties.

---

### **6.3 Classical Network Results (Displayed over Web portal)**

- **SDN modulation switched appropriately with SNR fluctuations**  
- **AES-encrypted communication remained stable under variable load**  
- **Anomalies were correctly detected and visualized**  
- **Network topology and channel metrics were accurately rendered**  

Overall, the classical system remained functional and secure under dynamic 6G-like conditions.

---

## **7. Discussion**

The system demonstrates:

- Feasibility of deploying QKD-secured communication in a 6G-like environment  
- Robust post-processing pipeline performance  
- Smooth compatibility between quantum keys and classical encrypted channels  
- Practical value for mission-critical, hierarchical communication networks  

The proposed system bridges theoretical QKD with practical engineering.

---

## **8. Key Contributions**

- Unified multi-protocol QKD implementation  
- Complete LDPC + Trevisan + HKDF pipeline  
- Integration with NS-3 6G-like classical networks  
- SDN-inspired adaptive modulation control  
- End-to-end encrypted communication using QKD-derived keys  
- Real-time anomaly detection and visualization  
- Demonstration of a mission-critical, military-grade network model  

---

## **9. Conclusion**

The project confirms that QKD-generated keys can be effectively integrated into a dynamic 6G-like network. By combining multi-protocol QKD, efficient post-processing, SDN-controlled classical communication, and a practical web interface, the system establishes a functional end-to-end secure communication pipeline suitable for mission-critical environments. This architecture provides a robust foundation for future research in quantum-secure communication and hybrid cryptographic models.

---

## **10. Limitations**

- Quantum simulations (SimulaQron) do not capture full physical-layer imperfections of real hardware.
- TF-QKD and MDI-QKD implementations are conceptual approximations lacking optical-channel fidelity.
- NS-3 simulation does not modify modulation at hardware PHY level (printed/logical switching only).
- Lack of decoy-state implementation in the actual QKD pipeline.
- Some classical simulations simplify mmWave/THz propagation dynamics.

These limitations stem from the scope of simulation-only work and can be extended in future studies. 

---

## **11. Future Works**

- Implement decoy-state TF-QKD and MDI-QKD  
- Incorporate high-fidelity quantum simulators (QuNetSim, NetSquid)  
- Develop PQC–QKD hybrid security  
- Add RL-based adaptive SDN modulation control  
- Integrate hardware-in-the-loop quantum modules  
- Expand dynamic inter-layer routing  

---

## **12. References**

[1] Shor, P. W. (1994). Algorithms for quantum computation: discrete logarithms and factoring. Proceedings 35th Annual Symposium on Foundations of Computer Science, 124–134. https://doi.org/10.1109/sfcs.1994.365700

[2] Gisin, N., Ribordy, G., Tittel, W., & Zbinden, H. (2002). Quantum cryptography. Reviews of Modern Physics, 74(1), 145–195. https://doi.org/10.1103/revmodphys.74.145

[3] Ekert, A. (1991). Quantum cryptography based on Bell’s theorem. Physical Review Letters, 67(6), 661–663. https://doi.org/10.1103/PhysRevLett.67.661

[4] Lucamarini, M., Yuan, Z. L., Dynes, J. F., & Shields, A. J. (2018). Overcoming the rate–distance limit of quantum key distribution without quantum repeaters. Nature, 557(7705), 400–403. https://doi.org/10.1038/s41586-018-0066-6

[5] Lo, H.-K., Curty, M., & Qi, B. (2012). Measurement-Device-Independent Quantum Key Distribution. Physical Review Letters, 108(13). https://doi.org/10.1103/physrevlett.108.130503

[6] Elkouss, David & Martínez Mateo, Jesús & Martin, Vicente. (2010). Information Reconciliation for Quantum Key Distribution. Quantum information & computation. 11. 

[7] Trevisan, L. (2001). Extractors and pseudorandom generators. Journal of the ACM, 48(4), 860-879.

[8] Krawczyk, H. (2010, August). Cryptographic extraction and key derivation: The HKDF scheme. In Annual Cryptology Conference (pp. 631-648). Berlin, Heidelberg: Springer Berlin Heidelberg.
