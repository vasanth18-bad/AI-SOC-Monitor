import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import time
from datetime import datetime
from collections import Counter

st.set_page_config(
    page_title="AI-SOC Monitor",
    page_icon="🛸",
    layout="wide"
)

# Alien Theme CSS
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #000000;
        background-image: 
            radial-gradient(ellipse at top, #001a00 0%, #000000 70%);
    }
    
    /* Text colors */
    .stMarkdown, p, label { color: #00ff41 !important; }
    
    /* Glowing title */
    .alien-title {
        font-size: 3em;
        font-weight: 900;
        color: #00ff41;
        text-shadow: 0 0 10px #00ff41, 0 0 20px #00ff41, 0 0 40px #00ff41;
        letter-spacing: 5px;
        text-align: center;
        font-family: 'Courier New', monospace;
    }
    
    /* Subtitle */
    .alien-sub {
        color: #00aa2a;
        text-align: center;
        font-family: 'Courier New', monospace;
        letter-spacing: 3px;
        font-size: 0.9em;
    }

    /* Metric boxes */
    div[data-testid="metric-container"] {
        background: #001a00;
        border: 1px solid #00ff41;
        border-radius: 5px;
        padding: 15px;
        box-shadow: 0 0 15px #00ff4133;
    }
    div[data-testid="metric-container"] label {
        color: #00aa2a !important;
        font-family: 'Courier New', monospace;
    }
    div[data-testid="metric-container"] div {
        color: #00ff41 !important;
        font-size: 2em !important;
        font-weight: bold;
        text-shadow: 0 0 10px #00ff41;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #000d00;
        border-right: 1px solid #00ff41;
    }
    section[data-testid="stSidebar"] * {
        color: #00ff41 !important;
    }

    /* Alert boxes */
    div[data-testid="stAlert"] {
        border-radius: 5px;
        font-family: 'Courier New', monospace;
        font-size: 0.85em;
    }

    /* Code blocks - packet feed */
    .stCode {
        background: #001a00 !important;
        border: 1px solid #00ff4133 !important;
        color: #00ff41 !important;
        font-family: 'Courier New', monospace !important;
    }

    /* Divider */
    hr { border-color: #00ff41 !important; opacity: 0.3; }

    /* Headers */
    h1, h2, h3 {
        color: #00ff41 !important;
        font-family: 'Courier New', monospace !important;
        text-shadow: 0 0 8px #00ff4166;
    }

    /* Bar chart */
    .stBarChart { filter: hue-rotate(90deg) saturate(2); }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: #000; }
    ::-webkit-scrollbar-thumb { background: #00ff41; border-radius: 5px; }

    /* Blink animation */
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
    }
    .blink { animation: blink 1.5s infinite; }
</style>
""", unsafe_allow_html=True)

LOG_FILE = "logs/packets.log"

def parse_logs():
    logs = []
    alerts = []
    if not os.path.exists(LOG_FILE):
        return logs, alerts
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if "->" in line and "THREAT" not in line and "AI ALERT" not in line:
            logs.append(line)
        if "THREAT_LEVEL:" in line:
            level = "HIGH" if "HIGH" in line else "MEDIUM" if "MEDIUM" in line else "LOW"
            alerts.append({"level": level, "detail": line})
    return logs, alerts

# ── HEADER ───────────────────────────────────
st.markdown('<div class="alien-title">👾 AI-SOC MONITOR 👾</div>', unsafe_allow_html=True)
st.markdown(f'<div class="alien-sub">[ SYSTEM: ONLINE ] [ {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} ] [ STATUS: MONITORING ]</div>', unsafe_allow_html=True)
st.markdown("---")

# ── SIDEBAR ──────────────────────────────────
st.sidebar.markdown("## ⚙️ CONTROL PANEL")
refresh = st.sidebar.slider("REFRESH RATE (sec)", 2, 30, 5)
st.sidebar.markdown("---")
st.sidebar.markdown("## 🎯 TARGET PORTS")
st.sidebar.code(
    "PORT 22   → SSH\n"
    "PORT 23   → TELNET\n"
    "PORT 3389 → RDP\n"
    "PORT 3306 → MYSQL\n"
    "PORT 1433 → MSSQL\n"
    "PORT 21   → FTP\n"
    "PORT 4444 → METASPLOIT\n"
    "PORT 8080 → HTTP-ALT"
)
st.sidebar.markdown("---")
st.sidebar.markdown("## 📡 SYSTEM STATUS")
st.sidebar.success("● CAPTURE: ACTIVE")
st.sidebar.success("● AI ENGINE: ONLINE")
st.sidebar.success("● DASHBOARD: LIVE")

# ── LOAD DATA ────────────────────────────────
logs, alerts = parse_logs()
high   = len([a for a in alerts if a["level"] == "HIGH"])
medium = len([a for a in alerts if a["level"] == "MEDIUM"])
low    = len([a for a in alerts if a["level"] == "LOW"])

# ── METRICS ──────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("📦 TOTAL PACKETS", len(logs), delta="LIVE")
with col2:
    st.metric("🔴 HIGH THREATS", high)
with col3:
    st.metric("🟡 MEDIUM THREATS", medium)
with col4:
    st.metric("🟢 LOW THREATS", low)

st.markdown("---")

# ── MAIN CONTENT ─────────────────────────────
left, right = st.columns([2, 1])

with left:
    st.markdown("### 📡 LIVE PACKET FEED")
    if logs:
        for log in reversed(logs[-15:]):
            if "[!]" in log:
                st.markdown(f'<p style="color:#ff0000;font-family:Courier New;font-size:0.85em;">⚠ {log}</p>', unsafe_allow_html=True)
            else:
                st.markdown(f'<p style="color:#00ff41;font-family:Courier New;font-size:0.8em;">▶ {log}</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p style="color:#00aa2a;font-family:Courier New;">[ WAITING FOR PACKETS... RUN packet_capture.py ]</p>', unsafe_allow_html=True)

with right:
    st.markdown("### 🚨 AI THREAT ALERTS")
    if alerts:
        for alert in reversed(alerts[-8:]):
            if alert["level"] == "HIGH":
                st.error(f"🔴 CRITICAL | {alert['detail']}")
            elif alert["level"] == "MEDIUM":
                st.warning(f"🟡 WARNING | {alert['detail']}")
            else:
                st.success(f"🟢 INFO | {alert['detail']}")
    else:
        st.markdown('<p style="color:#00aa2a;font-family:Courier New;">[ NO THREATS DETECTED ]</p>', unsafe_allow_html=True)

st.markdown("---")

# ── THREAT CHART ─────────────────────────────
st.markdown("### 📊 THREAT DISTRIBUTION MATRIX")
if alerts:
    counts = Counter([a["level"] for a in alerts])
    st.bar_chart(counts)
else:
    st.markdown('<p style="color:#00aa2a;font-family:Courier New;">[ AWAITING THREAT DATA... ]</p>', unsafe_allow_html=True)

# ── FOOTER ───────────────────────────────────
st.markdown("---")
st.markdown(
    '<p style="color:#005500;font-family:Courier New;text-align:center;font-size:0.8em;">'
    '[ AI-SOC MONITOR v1.0 ] [ POWERED BY GROQ AI + SCAPY ] [ ALL SYSTEMS NOMINAL ]'
    '</p>',
    unsafe_allow_html=True
)

# Auto refresh
time.sleep(refresh)
st.rerun()