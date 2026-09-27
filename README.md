
# Q-SENTINEL
![Python](https://img.shields.io/badge/Python-3.12%2B-blue)
![Qiskit](https://img.shields.io/badge/Qiskit-Quantum-purple)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-success)
## Quantum-Enhanced Intelligent Security and Threat Monitoring System

Q-SENTINEL is a modular security system that integrates multiple authentication, threat detection, tamper monitoring, quantum security concepts, and security simulation capabilities into a unified platform.

The system is designed to demonstrate how multiple layers of security can work together to protect a system from unauthorized access, tampering, and simulated attacks.

---

## 🚀 Features

- 🔐 Face Verification
- 🪪 RFID Authentication
- 🛡️ Security Engine
- ⚛️ Quantum Security Module
- 🚨 Tamper Detection
- 🎛️ Security Controller
- 🧪 Attack Scenario Simulation
- 📋 Security Event Logging
- 📊 Security Dashboard
- 🔍 Security Testing Modules

---

## 🏗️ System Architecture

                         Q-SENTINEL
                              │
             ┌────────────────┼────────────────┐
             │                │                │
       Authentication      Security         Monitoring
             │              Engine              │
        ┌────┴────┐           │          ┌─────┴─────┐
        │         │           │          │           │
      FACE      RFID      Controller   TAMPER       LOGS
        │         │           │          │           │
        └─────────┴───────────┴──────────┴───────────┘
                              │
                       Quantum Security
                              │
                         Simulator
                              │
                         Dashboard
````

---

## 📁 Project Structure

Q-SENTINEL/
│
├── controller/
│   └── security_controller.py
│
├── face_verification/
│   ├── face_auth.py
│   ├── register_face.py
│   └── verify_face.py
│
├── quantum/
│   ├── __init__.py
│   └── challenge.py
│
├── rfid/
│   ├── __init__.py
│   └── rfid_auth.py
│
├── security/
│   ├── __init__.py
│   └── security_engine.py
│
├── simulator/
│   ├── __init__.py
│   ├── admin_recovery_test.py
│   ├── attack_scenarios.py
│   ├── camera_test.py
│   ├── controller_test.py
│   ├── face_detection.py
│   ├── logger_test.py
│   ├── main.py
│   ├── quantum_circuit_demo.py
│   ├── quantum_demo.py
│   ├── quantum_test.py
│   ├── security_test.py
│   ├── tamper_logger_test.py
│   └── tamper_test.py
│
├── tamper/
│   ├── __init__.py
│   └── tamper_monitor.py
│
├── logs/
│   └── security_logger.py
│
├── dashboard.py
├── requirements.txt
├── .gitignore
└── README.md

---

## 🔐 Core Security Modules

### 1. Face Verification

The face verification module provides biometric authentication capabilities.

It includes:

* Face registration
* Face detection
* Face verification
* Authentication processing

---

### 2. RFID Authentication

The RFID module provides an additional authentication mechanism using RFID-based identification.

This allows the system to combine different authentication factors instead of depending on a single security mechanism.

---

### 3. Security Engine

The security engine contains the core security logic of Q-SENTINEL.

It is responsible for processing security events and coordinating different security components.

---

### 4. Security Controller

The security controller coordinates system-level security operations and acts as an interface between security modules.

---

### 5. Tamper Detection

The tamper monitoring module is designed to detect potential tampering events and record security-related activity.

Detected events can be passed to the logging system for further analysis.

---

### 6. Quantum Security

The quantum module contains quantum-security concepts and experimental demonstrations.

The project explores the use of quantum computing concepts as an additional security layer.

> Note: The quantum components in this repository are intended for experimental and educational demonstration unless explicitly stated otherwise.

---

### 7. Security Simulator

The simulator provides controlled demonstrations and tests for different security scenarios.

It includes simulations related to:

* Attack scenarios
* Security tests
* Tamper events
* Controller behavior
* Quantum demonstrations
* Camera and face detection tests
* Logging tests

---

## 📊 Dashboard

Q-SENTINEL includes a Python-based dashboard for interacting with and monitoring the security system.

The dashboard provides a centralized interface for security operations and system monitoring.

Run the dashboard using:

python dashboard.py

---

## ⚙️ Installation

### Step 1: Clone the Repository

git clone https://github.com/YOUR-USERNAME/Q-SENTINEL.git

### Step 2: Enter the Project Directory

cd Q-SENTINEL
```

### Step 3: Create a Virtual Environment

python -m venv .venv
```

### Step 4: Activate the Virtual Environment

#### Windows

.venv\Scripts\activate
```

#### Linux / macOS

source .venv/bin/activate
```

### Step 5: Install Dependencies

pip install -r requirements.txt
```

---

## ▶️ Running the Project

Start the main dashboard:

python dashboard.py
```

Individual modules and demonstrations can be executed from their respective directories.

Example:

python simulator/main.py
```

---

## 🧪 Testing

The simulator directory contains different testing and demonstration scripts.

Examples:

python simulator/security_test.py
```

python simulator/tamper_test.py
```
python simulator/quantum_demo.py
```

---

## 🛡️ Security Approach

Q-SENTINEL follows a layered security architecture.

Authentication
      ↓
Security Validation
      ↓
Threat Monitoring
      ↓
Tamper Detection
      ↓
Quantum Security Layer
      ↓
Event Logging
      ↓
Security Response
```

The goal is to reduce dependency on a single security mechanism and provide multiple layers of protection and monitoring.

---

## 🔮 Future Scope

Future development may include:

* Advanced quantum key distribution demonstrations
* Hardware-based RFID integration
* Improved biometric authentication
* Real-time threat detection
* AI-based anomaly detection
* Hardware tamper sensors
* Secure communication protocols
* Cloud-based security monitoring
* Mobile security notifications
* Advanced security analytics
* Integration with physical security hardware

---

## ⚠️ Disclaimer

Q-SENTINEL is an experimental and educational security project.

The simulator and quantum components are intended for controlled testing, research, and demonstration purposes.

Do not use the system to access, attack, monitor, or interfere with systems without proper authorization.

---

## 👨‍💻 Project

Q-SENTINEL
Quantum-Enhanced Intelligent Security and Threat Monitoring System

Built for learning, experimentation, security research, and hardware/software security development.

---

## 📜 License

This project is intended to be released under the MIT License.
