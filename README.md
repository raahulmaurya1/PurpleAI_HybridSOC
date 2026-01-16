# 🛡️ PurpleSentinel Orchestrator  
### Autonomous Hybrid SOC & Threat Response Platform

![SOC](https://img.shields.io/badge/SOC-Autonomous-purple)
![SOAR](https://img.shields.io/badge/SOAR-Enabled-blue)
![AI](https://img.shields.io/badge/AI-Google%20Gemini-red)
![Python](https://img.shields.io/badge/Python-3.8+-yellow)
![License](https://img.shields.io/badge/License-MIT-green)

> **PurpleSentinel** is a next-generation **AI-driven SOAR platform** that autonomously detects, analyzes, and mitigates cyber threats using **live SIEM telemetry or simulated attack scenarios**.

---

## 📖 Overview

PurpleSentinel bridges the critical gap between **detection** and **remediation** in modern SOC environments.

It introduces a **Hybrid Data Engine** capable of:
- 📡 Monitoring **real-time Wazuh SIEM logs**
- 🧪 Generating **deterministic attack simulations** (Ransomware, SQLi, DDoS)

A **Context-Aware AI Analyst (Google Gemini)** evaluates threats in real time and triggers **zero-touch remediation** using **Ansible + iptables**.

---

## 🏗️ System Architecture



## ✨ Key Features

### ⚔️ Hybrid Threat Engine
- Live Wazuh monitoring
- Safe attack simulations (SQLi, Ransomware, DDoS)

### 🧠 AI Threat Analysis
- Google Gemini 1.5
- Context-aware decision making

### 🚀 Automated SOAR
- Zero-touch remediation
- Dynamic firewall rules

---

## 🛠️ Tech Stack

| Layer | Technology |
|-----|-----------|
| Backend | Python, FastAPI |
| Frontend | HTML, Bootstrap |
| SIEM | Wazuh |
| AI | Google Gemini |
| Automation | Ansible |
| Database | SQLite |

---

## ⚙️ Installation

```bash
git clone https://github.com/yourusername/PurpleSentinel.git
cd PurpleSentinel
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🚀 Run

```bash
uvicorn app.main:app --reload
```

---

## 📄 License

MIT License

---

**Built with ❤️ by Rahul Maurya**
