import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
import time
from datetime import datetime
from collections import Counter

# Page config
st.set_page_config(
    page_title="AI-SOC Monitor",
    page_icon="🛡️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1e2130; padding: 10px; border-radius: 8px; }
    .alert-high { background-color: #ff4444; padding: 10px; border-radius: 5px; color: white; }
    .alert-medium { background-color: #ff8800; padding: 10px; border-radius: 5px; color: white; }
    .alert-low { background-color: #00cc44; padding: 10px; border-radius: 5px; color: white; }
</style>
""", unsafe_allow_html=True)

LOG_FILE = "logs/packets.log"

def parse_logs():
    """Parse log file and return data."""
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

        # Normal packet log
        if "->" in line and "AI ALERT" not in line and "THREAT" not in line:
            try:
                parts = line.split("|")
                if len(parts) >= 2:
                    timestamp = parts[0].strip().strip("[]")
                    rest = parts[1].strip()
                    logs.append({
                        "timestamp": timestamp,
                        "info": rest
                    })
            except:
                pass

        # AI Alert
        if "THREAT_LEVEL:" in line:
            level = "HIGH" if "HIGH" in line else "MEDIUM" if "MEDIUM" in line else "LOW"
            alerts.append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "level": level,
                "detail": line
            })

    return logs, alerts

# ── Header ───────────────────────────────────
st.markdown("# 🛡️ AI-SOC Monitor Dashboard")
st.markdown(f"**Live Security Monitoring** | Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.divider()

# ── Auto Refresh ─────────────────────────────
refresh = st.sidebar.slider("Auto Refresh (seconds)", 2, 30, 5)
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔴 Suspicious Ports")
st.sidebar.code("22  - SSH\n23  - Telnet\n3389- RDP\n3306- MySQL\n1433- MSSQL\n21  - FTP\n4444- Metasploit\n8080- HTTP-Alt")

# ── Load Data ────────────────────────────────
logs, alerts = parse_logs()

# ── Metrics Row ──────────────────────────────
col1, col2, col3, col4 = st.columns(4)

high_alerts   = len([a for a in alerts if a["level"] == "HIGH"])
medium_alerts = len([a for a in alerts if a["level"] == "MEDIUM"])
low_alerts    = len([a for a in alerts if a["level"] == "LOW"])

with col1:
    st.metric("📦 Total Packets", len(logs), delta="Live")
with col2:
    st.metric("🔴 HIGH Alerts", high_alerts)
with col3:
    st.metric("🟡 MEDIUM Alerts", medium_alerts)
with col4:
    st.metric("🟢 LOW Alerts", low_alerts)

st.divider()

# ── Two Column Layout ─────────────────────────
left, right = st.columns([2, 1])

with left:
    st.markdown("### 📡 Live Packet Feed")
    if logs:
        df = pd.DataFrame(logs[-50:])
        st.dataframe(df, use_container_width=True, height=300)
    else:
        st.info("Waiting for packets... Run packet_capture.py first!")

with right:
    st.markdown("### 🚨 AI Alerts")
    if alerts:
        for alert in reversed(alerts[-10:]):
            if alert["level"] == "HIGH":
                st.error(f"🔴 HIGH | {alert['timestamp']}\n{alert['detail']}")
            elif alert["level"] == "MEDIUM":
                st.warning(f"🟡 MEDIUM | {alert['timestamp']}\n{alert['detail']}")
            else:
                st.success(f"🟢 LOW | {alert['timestamp']}\n{alert['detail']}")
    else:
        st.info("No alerts yet!")

st.divider()

# ── Alert Chart ───────────────────────────────
st.markdown("### 📊 Threat Distribution")
if alerts:
    alert_counts = Counter([a["level"] for a in alerts])
    chart_data = pd.DataFrame({
        "Threat Level": list(alert_counts.keys()),
        "Count": list(alert_counts.values())
    })
    st.bar_chart(chart_data.set_index("Threat Level"))
else:
    st.info("No threat data yet!")

# ── Auto Refresh ──────────────────────────────
time.sleep(refresh)
st.rerun()