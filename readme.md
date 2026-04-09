# 🤖 Sypher: AI System Controller

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)

**Sypher** is an advanced, voice-driven AI assistant designed to bridge the gap between Large Language Models and local system execution. It doesn't just "chat"—it sees your screen, hears your voice, and controls your Windows environment to execute complex workflows autonomously.

---

## ✨ Core Features

Sypher is built to be a complete autonomous agent for Windows. Its current capabilities include:

- 🎙️ **Multi-Modal Interaction:** Seamlessly switch between voice and text commands with low-latency responses.
- 🖥️ **Vision Awareness:** Uses OCR and image analysis to "see" your active windows and webcam feed.
- 📂 **File Operations:** Create, move, delete, and organize files and directories through natural language.
- 🌐 **Web Intelligence:** Integrated Google Search, live weather reports, and YouTube playback control.
- 🛠️ **System Management:** Control system volume, brightness, launch any application, and execute shell commands.
- 🧠 **Contextual Memory:** Persistent storage for user preferences, allowing the AI to learn your habits over time.
- 📅 **Productivity Suite:** Manage reminders, send messages, and get coding assistance in real-time.
- 🔒 **Security-First Design:** Sensitive actions require user approval before execution.

---

## 🏗️ System Architecture

Sypher operates on a continuous **Agentic Loop** to ensure tasks are completed accurately:

1. **Perception:** Gathers raw data from the Microphone (Audio) and Screen/Webcam (Visuals).
2. **Reasoning:** Leverages **Gemini Pro** to analyze intent and choose the most effective tool.
3. **Execution:** Triggers specialized Python scripts in the `actions/` folder to perform system tasks.
4. **Memory:** Archives the task result to refine future logic and maintain conversation history.



---

## 🚀 Installation & Setup

### 1. Prerequisites
- **OS:** Windows 10 or 11 (required for system-level controls).
- **Python:** Version 3.10 or higher.
- **Hardware:** A working microphone and (optional) webcam.

### 2. Get an API Key
Sypher uses the Google Gemini API. You can get a free key here:
- [Google AI Studio](https://aistudio.google.com/)

### 3. Setup Instructions
Open your terminal (PowerShell or CMD) and run the following:

```powershell
# Clone the repository
git clone [https://github.com/amwanshul/Sypher.git](https://github.com/amwanshul/Sypher.git)
cd Sypher

# Create a virtual environment (Isolated Workspace)
python -m venv venv

# Activate the environment
.\venv\Scripts\activate

# Upgrade pip and install core dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# Run project-specific setup
python setup.py