A **README.md** file is the face of my project. 

Since iam the **Lead Architect**, this file is written to showcase my skills and the advanced nature of **OmniShield AI**.


# OMNISHIELD AI: Advanced Security Ecosystem

**Lead Architect:** Vela Poojitha

**Version:** 1.0.0 (Production Ready)

OmniShield AI is a comprehensive, multi-threaded security solution that integrates **Real-Time Computer Vision** with a **Professional Web-Based Command Center**. It utilizes the YOLOv8 architecture for object detection and DeepFace for biometric verification, providing a seamless bridge between physical security and digital monitoring.


##  Core Features

**Intelligent Zone Monitoring**: Interactive setup allowing users to draw custom "Restricted Zones" on the live feed.
**Dual-Layer Biometric Auth**: Automatically distinguishes between authorized personnel (Vela Poojitha) and unknown intruders.
**Multi-Channel Alerts**: Instant notifications via **Telegram Bot API**, **Email (SMTP)**, and **Local Audio Siren**.
**Live Audit Dashboard**: A professional Flask-based web interface with real-time log updates and evidence viewing.
**Session-Based Security**: Protected login system with an icon-only professional PIN toggle.


## System Architecture

The project is split into two synchronized processes:

1. **Vision Engine**: Handles the camera feed, AI processing, and database writing.
2. **Command Center (Dashboard)**: A Flask server that reads from the database and serves the UI.



## Project Structure

OMNISHIELD_AI/
├── authorized_users/     # Reference photos for Face Recognition
├── static/
│   ├── captures/         # Real-time evidence snapshots
│   └── (images)          # Professional backgrounds (bg1, loginbg)
├── templates/
│   ├── login.html        # Secure Entry Portal
│   ├── index.html        # Main Command Center
│   └── audit.html        # Forensic Log Viewer
├── venv/                 # Python Virtual Environment
├── dashboard.py          # Flask Web Server Logic
├── vision_engine.py      # YOLOv8 & Alert Logic
├── security_archive.db   # Shared SQLite Database
├── run_system.bat        # Master One-Click Launcher
└── requirements.txt      # Dependency List



## Installation & Setup

### 1. Prerequisites

* Python 3.10 or 3.11 installed.
* A webcam connected to the system.

### 2. Environment Setup

Open the terminal in the project folder and run:

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate

# Install all dependencies
pip install -r requirements.txt


### 3. Configuration

* Update `TOKEN` and `CHAT_ID` in `vision_engine.py` with your Telegram Bot details.
* Update `SENDER_EMAIL` and `SENDER_PASSWORD` for Email alerts.
* Place a clear photo of yourself in the `authorized_users/` folder.



## Usage

1. **Launch**: Double-click the `run_system.bat` file on your desktop.
2. **Configure Zone**: Use the mouse to draw a box over the area you want to protect in the "SETUP" window. Press **'S'** to start.
3. **Access Dashboard**: Open your browser to `http://127.0.0.1:5000`.
4. **Monitor**: View the **Audit Center** to see live logs appearing as the AI detects activity.



## Security Disclaimer

This system is intended for educational and private monitoring purposes. Ensure compliance with local privacy laws regarding video surveillance.

**Developed by Vela Poojitha**


### **Final Project Checklist**

* AI Detection (YOLOv8)
* Face Verification (DeepFace)
* Database Logging (SQLite)
* Web Dashboard (Flask)
* Professional README
* One-Click Launcher

