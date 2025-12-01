# Quantum Systems and Engineering Portfolio  
**Author:** *Ananya Asthana* 

---

## Overview  
This repository documents a structured body of work uniting **quantum computing**, **quantum communication**, and **hybrid cryptographic engineering**.  
It integrates simulation, algorithmic modeling, and analytical investigation, presenting a progression from theoretical principles to reproducible implementations.  
The collection emphasizes system design, measurement accuracy, and cross-disciplinary synthesis between classical computation and quantum technologies.
This portfolio reflects a research-driven, execution-aware approach to quantum systems, focusing on architectures, noise models, and hybrid quantum–classical coordination principles relevant to scalable quantum technologies.

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
- Neglecton-based braiding mechanisms for universal topological quantum computation (TQC)
- Hybrid PQC–Quantum architectures for scalable long-term security  

Each entry synthesizes relevant research literature, critically evaluates open challenges, and articulates implementation pathways grounded in current quantum information research.

---

## Purpose  
This portfolio represents a systematic progression from **foundational learning to applied research** in quantum systems engineering.  
It emphasizes rigor, reproducibility, and conceptual clarity, aligning computational models with secure and scalable architectures.  
Collectively, the works establish a framework for integrating quantum computation, communication, and cryptography within unified system design.
These works are analyzed in the context of realistic noise models, connectivity limits, and the coordination requirements of hybrid quantum–classical systems, reflecting an execution-aware perspective aligned with practical NISQ-era constraints.

---

## Reproducibility and Execution Instructions

This repository includes `requirements.txt` and `environment.yaml` for environment reconstruction. Do note that these are primarily for notebooks in the `1_Foundations_Qiskit/` and `2_Simulations_and_Models/` modules. The `Project/` module contains its own code reproducibility files. 

Follow these steps to set up the repository and run notebooks locally:

### 1. Clone the repository

    git clone https://github.com/ANANYA-ASTHANA/Quantum-Engineering-Portfolio.git

### 2. Navigate into the repo folder

    cd Quantum-Engineering-Portfolio

### 3. Option A — Reproduce using pip (recommended for lightweight usage)
#### 3.1 Create and activate a virtual environment

    python -m venv .venv
    # macOS/Linux:
    source .venv/bin/activate
    # Windows (PowerShell):
    # .venv\Scripts\Activate.ps1

#### 3.2 Install dependencies

    pip install -r requirements.txt

#### 3.3 Register the environment as a Jupyter kernel (recommended)

    python -m ipykernel install --user --name qe-portfolio

#### 3.4 Launch Jupyter from the repository root

    jupyter lab    # or: jupyter notebook

### 4. Option B — Reproduce using Conda (full environment recreation)

To recreate the same environment used in this project:

#### 4.1. Create the environment from the provided YAML file

    conda env create -f environment.yaml

#### 4.2. Activate the environment
    
    conda activate foundations-simulations-env   

#### 4.3 (Optional) Register the environment as a Jupyter kernel

    python -m ipykernel install --user --name foundations-simulations-env

#### 4.4. Launch Jupyter from the repository root

    jupyter lab    # or: jupyter notebook
    

**Notes:** 
- JupyterLab, notebook, and ipykernel are already included in `requirements.txt` and `environment.yaml`, so no additional installation is required.
- VS Code users may open .ipynb files directly; the environments created above will appear in the Jupyter kernel selector.
- The `Project/` folder has its own reproducibility files for the quantum-classical integrated system.


