# 👾 AI-SOC Monitor

<div align="center">

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Groq](https://img.shields.io/badge/AI-Groq%20LLaMA-orange?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-red?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

### Real-Time AI-Powered Security Operations Center

</div>

---

## 📸 Dashboard Preview

<div align="center">

![Dashboard](screenshots/dashboard_terminal.png)

</div>

---

## 🔥 What This Does

This tool monitors your network in **real-time** and uses
**Groq AI (LLaMA 3.3)** to automatically analyze suspicious
traffic — just like a real SOC analyst, but fully automated!

```
Live Network Traffic
       ↓
 Scapy Capture
       ↓
Suspicious Detection
       ↓
  Groq AI Analysis
       ↓
Real-Time SOC Alert
```

---

## ✨ Features

- 📡 **Live Packet Capture** — Real-time network monitoring
- 🤖 **AI Threat Analysis** — Groq LLaMA analyzes each threat
- 🚨 **Auto Classification** — HIGH / MEDIUM / LOW severity
- 🖥️ **SOC Dashboard** — Alien theme, live graphs, alerts
- 🔍 **Attack Detection** — Port Scan, SYN Flood, Brute Force
- 📝 **Alert Logging** — All threats saved to log files

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.x | Core language |
| Scapy | Live packet capture |
| Groq API (LLaMA 3.3) | AI threat analysis |
| Streamlit | SOC Dashboard UI |
| Npcap | Windows packet driver |

---

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/vasanth18-bad/AI-SOC-Monitor.git
cd AI-SOC-Monitor
```

### 2. Install Dependencies
```bash
pip install scapy groq streamlit python-dotenv
```

### 3. Install Npcap (Windows Only)
👉 [npcap.com/#download](https://npcap.com/#download)

### 4. Add API Key
Create `.env` file:
```
GROQ_API_KEY=your_groq_api_key_here
```
Get FREE API key: [console.groq.com](https://console.groq.com)

### 5. Run Project
```bash
# Easy way - double click!
run.bat

# Terminal 1
python capture/packet_capture.py

# Terminal 2
python -m streamlit run dashboard/soc_dashboard.py
```

### 6. Open Dashboard
```
http://localhost:8501
```

---

## 📁 Project Structure

```
AI-SOC-Monitor/
├── capture/
│   └── packet_capture.py    # Live packet capture
├── ai_engine/
│   └── analyzer.py          # Groq AI analysis
├── dashboard/
│   └── soc_dashboard.py     # Streamlit dashboard
├── logs/
│   └── packets.log          # Alert logs
├── screenshots/             # Portfolio screenshots
├── run.bat                  # One-click launcher
├── .env                     # API keys (not in GitHub)
└── README.md
```

---

## 🎯 Detected Threats

| Attack Type | Port | Severity |
|------------|------|---------|
| SSH Brute Force | 22 | 🔴 HIGH |
| Telnet Attack | 23 | 🔴 HIGH |
| RDP Attack | 3389 | 🔴 HIGH |
| MySQL Attack | 3306 | 🟡 MEDIUM |
| FTP Attack | 21 | 🟡 MEDIUM |
| Metasploit | 4444 | 🔴 HIGH |
| HTTP-Alt | 8080 | 🟡 MEDIUM |

---

## ⚠️ Legal Notice

> This tool is for **educational purposes only**.
> Use only on networks you **own or have permission** to monitor.
> Unauthorized network monitoring is **illegal**.

---

## 👨‍💻 Author

<div align="center">

**V** | Cybersecurity Portfolio Project

[![GitHub](https://img.shields.io/badge/GitHub-vasanth18--bad-black?style=for-the-badge&logo=github)](https://github.com/vasanth18-bad)

*Built with 💚 and lots of packets*

</div>
