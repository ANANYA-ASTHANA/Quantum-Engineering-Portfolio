# Future-Proofing 6G Networks: A Quantum Approach
**Author:** *Ananya Asthana*

This repository presents an end-to-end **quantum-secure 6G communication architecture**, integrating Quantum Key Distribution (QKD), classical key refinement, and AES-256–secured data transmission within an NS-3–simulated 6G network.

The system is engineered for **mission-critical environments**, particularly **government and military communication networks**, where high-assurance confidentiality, integrity, and future security are required.

---

## 1. Motivation and Problem Context

Emerging 6G systems—characterized by THz/mmWave communication, ultra-low latency, and massive device density—will operate in a threat landscape where conventional public-key cryptographic schemes (e.g., RSA, ECC) become vulnerable to quantum attacks (e.g., Shor’s algorithm).

This project develops a hybrid quantum-classical security architecture that:

- Employs **QKD** for forward secrecy
- Applies strong classical post-processing for key refinement
- Integrates quantum-derived keys into a 6G network (simulation) for secure communication

These requirements are especially critical in **national-level and defense communication infrastructures**, where long-term forward secrecy and resilience against quantum-enabled adversaries are essential.

---

## 2. System Architecture Overview

The system consists of four integrated layers:

### **Quantum Layer**
- End-to-end **E91 QKD** implementation for raw key generation  
- **Sifting + QBER testing**:  
  - 10% of the sifted bits are publicly disclosed for QBER estimation  
  - If QBER > **5%**, the entire raw key is discarded as insecure  
  - Otherwise, testing bits are discarded and the remaining sifted bits proceed to post-processing  
- **TF-QKD** central-node simulation using a Hamiltonian-based beamsplitter model 
- **MDI-QKD** central **Bell-State Measurement (BSM)** simulation at Charlie    

### **Post-Processing Layer**
- **LDPC-based key reconciliation**  
- **Trevisan’s extractor** for privacy amplification and session key derivation
- **HKDF-SHA256** to derive high-entropy AES-256 session keys (efficient alternative to Trevisan for KDF) 

### **Classical Network Layer**
- **NS-3 (≥3.43)** simulation of a 6G environment using mmWave/THz models  
- **SDN-driven adaptive modulation** (PSK $\leftrightarrow$ QAM based on real-time SNR)  
- AES-256–encrypted communication using quantum-derived keys  

### **User Interface Layer**
- Flask-based **web portal** with **Multi-Factor Authentication (MFA)**  
- Encrypted communication channels between authenticated users  
- Administrator dashboard providing **real-time network visualization**  

Across all layers, the architecture is designed for **high assurance**, **access control**, and **operational robustness**, reflecting the stringent requirements of **mission-critical government–military networks**.

For a complete methodological explanation, refer to: [`docs/project_summary.md`](docs/project_summary.md)

---

## 3. Key Experimental Results
### 3.1 Quantum Layer
- **E91 QKD (SimulaQron):**
  - Generated **7000 EPR pairs**, with **$ \approx 45–50% $ sifted-key retention** after sifting
  - QBER measured in 10% sifted key sample bits ranged **4–7%** (abort threshold > 5%)
  - Only keys with QBER $ \leq 5% $ were accepted
- **TF-QKD (Qiskit beamsplitter model):**
  - Achieved **> 95% interference visibility** in noise-free simulation
- **MDI-QKD (Qiskit BSM simulation):**
  - Bell-state measurement (BSM) fidelity: **> 97% ideal fidelity** under simulated conditions

### 3.2 Post-Processing Layer
- **Key Reconciliation (LDPC):**
  - Successfully reconciled sifted keys generated from noisy EPR pairs
  - Operated on keys with **< 5% QBER**
- **Privacy Amplification (Trevisan’s Extractor):**
  - Produced a **1792-bit high-entropy master key**
  - Represents **$ \approx 87% $ compression** from the reconciled key length
- **Session-Key Derivation (HKDF-SHA256):**
  - Multiple **AES-256 session keys** derived securely from compressed master key with **zero bit reuse**

### 3.3 Classical 6G Network Layer (NS-3)
- **Adaptive Modulation (SDN-controlled):**
  - Modulation change triggered by anomaly thresholds:
    - **SNR < 8 dB**
    - **BER > 0.15**
    - **Load > 80%**
    - **Packet loss rate > 3%**
- **Encrypted Communication:**
  - QKD $\rightarrow$ AES-256 integration enabled **real-time secure messaging** across hierarchical links (Cabinet $\leftrightarrow$ HQ $\leftrightarrow$ Regional Bases)

These results directly validate the correctness of quantum key generation, the integrity of the post-processing pipeline, and the robustness of AES-secured 6G communication under dynamic channel conditions.

---

## 4. Technical Contributions

- End-to-end **E91 QKD key generation pipeline**, complemented by **TF-QKD and MDI-QKD central-operation simulations** (Hamiltonian interference + BSM)
- High-integrity post-processing (LDPC-based key reconciliation, Trevisan's extractor, HKDF)  
- Realistic encrypted 6G communication using quantum-derived AES-256 session keys  
- Engineering of SDN control, hierarchical subnets, anomaly indicators, and access restrictions 
- Architecture designed specifically for **gov–military mission-critical communications**  

---

## 5. How to Navigate This Repository

The following summarizes the high-level repository layout:

```
proj_code/       # Quantum protocols, post-processing, AES, NS-3 logic, Flask UI
diagrams/        # System diagrams (mind-map, use-case)
docs/            # Long-form project summary 
requirements.txt # Python dependencies (bounded versions)
environment.yaml # Conda environment definition (bounded versions)
README.md        # Formal academic project overview
```

---

## 6. Reproducibility and Execution Instructions

This repository includes `requirements.txt` and `environment.yaml` for environment reconstruction. Internal modules (`PP_1.py`, `PP_2.py`, `session_keys.py`) are part of the source tree and are not listed as dependencies.

---

### 6.1 System Requirements (Install Separately)

- **NS-3 (≥ 3.43)** with Python bindings (`import ns`)
- **SimulaQron** (CQC backend for QKD protocols)
- CMake, C++17-compatible toolchain, OpenSSL development headers

---

### 6.2 Python Environment Setup

**Using Conda (recommended):**
```bash
conda env create -f environment.yaml
conda activate proj-repro-env
```

**Using pip:**
```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

### 6.3 Start the Quantum Backend

```bash
simulaqron reset
simulaqron start
```

---

### 6.4 Execute the Full System

**Quantum Layer (two terminals):**
```bash
python proj_code/quantum/user1_e91.py
python proj_code/quantum/user2_e91.py
```

**Post-Processing Layer (two terminals):**
```bash
python proj_code/classical/PP_1.py
python proj_code/classical/PP_2.py
```

**6G Network Simulation + Web Interface:**
```bash
python proj_code/classical/classical_network.py
```

Access the portal at: **http://localhost:5000/**

---
  
This repository accompanies the capstone project *“Future-Proofing 6G Networks: A Quantum Approach.”*
