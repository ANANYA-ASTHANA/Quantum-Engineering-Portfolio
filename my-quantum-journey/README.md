# Quantum Systems and Engineering Portfolio  
**Ananya Asthana**  
*MSc in Quantum Science and Engineering*  

---

## Overview  
This repository documents a structured body of work uniting **quantum computing**, **quantum communication**, and **hybrid cryptographic engineering**.  
It integrates simulation, algorithmic modeling, and analytical investigation, presenting a progression from theoretical principles to reproducible implementations.  
The collection emphasizes system design, measurement accuracy, and cross-disciplinary synthesis between classical computation and quantum technologies.

---

## Repository Structure  

### 1. Foundations_Qiskit/  
Conceptual and computational groundwork developed from the [IBM Qiskit Textbook](https://github.com/Qiskit/textbook).  
Includes notebooks on qubit operations, gate logic, measurement processes, and statevector representation- establishing fluency in Qiskit syntax and quantum-state analysis.

### 2. Simulations_and_Models/  
Canonical and exploratory circuit models, including:  
- Bell state generation and verification  
- Quantum teleportation
- Grover’s search
- Quantum Fourier Transform (QFT)
- Variational Quantum Eigensolver (VQE) 

Each notebook links theoretical constructs with experimental outcomes through visualization and measurement analysis.

### 3. Project/  
Applied system bridging quantum and classical cryptography, with the following primary functions:  
- Design and simulate a mission-critical, government–military-style 6G-like network secured via E91-based QKD, with TF- and MDI-inspired central interference models for realistic quantum operations.
- Integrate distilled quantum keys into an AES-256 encryption pipeline to secure hierarchical classical subnets, illustrating a practical hybrid quantum–classical security stack.
- Demonstrate an end-to-end workflow from quantum key generation and QBER-based key acceptance to encrypted classical communication in a structured multi-layer network setting.


### 4. Research_Analyses/  
Analytical reviews addressing frontier topics in quantum information science:  
- Quantum Neural Networks (QNNs) for encoding and optimization  
- Neglecton-based braiding mechanisms for fault-tolerant computation  
- Hybrid PQC–Quantum architectures for scalable long-term security  

Each entry synthesizes literature insights, identifies open challenges, and outlines pathways for implementation.

---

## Purpose  
This portfolio represents a systematic progression from **foundational learning to applied research** in quantum systems engineering.  
It emphasizes rigor, reproducibility, and conceptual clarity, aligning computational models with secure and scalable architectures.  
Collectively, the works establish a framework for integrating quantum computation, communication, and cryptography within unified system design.

---

## Reproducibility and Execution Instructions

This repository includes `requirements.txt` and `environment.yaml` for environment reconstruction. Do note that these are primarily for notebooks in the `1_Foundations_Qiskit/` and `2_Simulations_and_Models/` modules. The `Project/` module contains its own code reproducibility files. 

Follow these steps to set up the repository and run notebooks locally:

### 1. Clone the repository

    git clone https://github.com/ANANYA-ASTHANA/Quantum-Engineering-Portfolio.git

### 2. Navigate into the repo folder

    cd my-quantum-journey

### 3. Install dependencies

    pip install -r requirements.txt

### 4. Launch Jupyter Lab or Notebook
#### Launch Jupyter Lab
    jupyter lab

#### OR launch Jupyter Notebook
    jupyter notebook

### 5. Reproducing the Environment (optional)

To recreate the same environment used in this project:

#### 1. Create the environment from the provided YAML file
    conda env create -f environment.yml

#### 2. Activate the environment
    conda activate qiskit-env

#### 3. Launch Jupyter Lab inside the repo folder
    jupyter lab

---

## Reference Document  
A comprehensive overview of the research objectives, methodologies, and outcomes underlying this portfolio is provided in the accompanying document below.  
The summary consolidates theoretical, computational, and engineering aspects of the work presented in this repository.

[Research Summary (PDF)](./Research_Summary_EPFL_v3.pdf)

---
