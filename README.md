# 🔐 OmniShield_AI

## 🎥 Project Demo

Watch the full working demo here:

👉 **[Click here to watch OmniShieldAI Demo]( https://1drv.ms/v/c/64673a201db65afa/IQD6D9ayiA_nS7scCtVRxrUWAS2Qr3IlQLZ8wGjLOcPPh6M?e=554Now
)**


## AI-Powered Smart Surveillance & Intrusion Detection System

OmniShieldAI is an intelligent, AI-driven real-time surveillance system designed to detect unauthorized access using deep learning and computer vision. Built with YOLOv8 and Flask, the system performs live object detection, captures breach evidence, logs events securely, and provides an administrative audit dashboard for monitoring and analysis.

This project demonstrates the integration of AI, backend engineering, database systems, and web-based security management into a production-style application.

---

## 🚀 Key Features

* 🎥 Real-Time Object Detection using YOLOv8
* 🚨 Intrusion Detection & Automated Alert Trigger
* 📸 Evidence Capture & Storage on Breach
* 🔐 Secure Login & Admin Authentication
* 📊 Web-Based Audit Dashboard
* 🗄 SQLite-Based Secure Event Logging
* 🔊 Alarm/Siren Trigger System
* 🧠 AI Engine + Flask Backend Integration
* 📁 Authorized User Verification Mechanism

---

## 🧠 AI & Detection Engine

OmniShieldAI integrates the **YOLOv8 (Small Variant)** model via the Ultralytics framework for high-speed real-time object detection.

Detection Pipeline:

1. Live video stream captured via OpenCV
2. Frame-by-frame AI inference using YOLOv8
3. Unauthorized detection logic applied
4. Evidence image captured
5. Event logged in SQLite database
6. Siren triggered for intrusion alert
7. Breach record displayed in audit dashboard

Model file required:

* `yolov8s.pt` (Download separately – not included due to size limits)

---

## 🛠 Tech Stack

### 🔹 Backend

* Python
* Flask

### 🔹 AI / Computer Vision

* Ultralytics YOLOv8
* OpenCV

### 🔹 Frontend

* HTML
* Jinja2 Templates
* CSS (Static Assets)

### 🔹 Database

* SQLite

### 🔹 System Utilities

* Batch Script Automation
* Media Alert System
* File-Based Evidence Storage

---

## 📂 Project Structure

```
OmniShield_AI/
│
├── dashboard.py              # Flask web server & routing
├── vision_engine.py          # AI detection engine
├── requirements.txt
├── README.md
├── run_system.bat
│
├── templates/                # Web templates
│   ├── index.html
│   ├── login.html
│   └── audit.html
│
├── static/                   # CSS, JS, media assets
│
├── authorized_users/         # Authorized user storage (excluded in repo)
├── breach_reports/           # Captured breach evidence (excluded in repo)
│
└── .gitignore
```

---

## ⚙ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/velapoojitha/OmniShield_AI.git
cd OmniShield_AI
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Download YOLOv8 Model

Download `yolov8s.pt` from:

[https://github.com/ultralytics/ultralytics](https://github.com/ultralytics/ultralytics)

Place the file inside the project root directory.

### 5️⃣ Run the Application

```bash
python dashboard.py
```

Open in browser:

```
http://127.0.0.1:5000
```

---

## 🔐 Security Workflow

1. System monitors live camera feed
2. Detects unauthorized individual
3. Captures evidence image
4. Logs timestamp & event in database
5. Stores evidence in breach_reports folder
6. Triggers siren alert
7. Displays event inside audit dashboard

---

## 📊 Database Structure

The SQLite database stores:

* Event ID
* Timestamp
* Detection Type
* Evidence Image Path
* Authorization Status

This ensures complete traceability of intrusion events.

---

## 📌 Future Enhancements

* Face Recognition Integration
* Email/SMS Real-Time Alert System
* Cloud Deployment (AWS / Azure)
* Docker Containerization
* Role-Based Multi-Admin Authentication
* Real-Time Analytics Dashboard
* Cloud Database Migration

---

## 🏆 Why This Project Matters

OmniShieldAI demonstrates:

* Real-time AI system design
* Deep learning model integration
* Backend + frontend system architecture
* Database-driven security logging
* Production-style application structure
* Practical AI deployment workflow

This project reflects strong capabilities in AI engineering, backend development, and intelligent system design.

---

## 👩‍💻 Author

**Vela Poojitha**
M.Tech Computer Science & Engineering
AI & Web Developer
Passionate about intelligent security systems and AI-driven automation.

---
