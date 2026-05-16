import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.stdout.reconfigure(encoding='utf-8')

from scapy.all import sniff, IP, TCP, UDP
from datetime import datetime
from ai_engine.analyzer import analyze_packet

LOG_FILE = "logs/packets.log"
os.makedirs("logs", exist_ok=True)

SUSPICIOUS_PORTS = [22, 23, 3389, 3306, 1433, 21, 4444, 8080]

def save_log(message):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(message + "\n")

def packet_handler(packet):
    if IP in packet:
        src_ip   = packet[IP].src
        dst_ip   = packet[IP].dst
        protocol = "TCP" if TCP in packet else "UDP" if UDP in packet else "OTHER"

        if TCP in packet:
            dst_port = packet[TCP].dport
        elif UDP in packet:
            dst_port = packet[UDP].dport
        else:
            dst_port = 0

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log = f"[{timestamp}] {protocol} | {src_ip} -> {dst_ip}:{dst_port}"

        if dst_port in SUSPICIOUS_PORTS:
            print(f"\033[91m[!] SUSPICIOUS: {log}\033[0m")
            print(f"\033[93m[*] Sending to AI...\033[0m")

            # AI Analysis
            ai_result = analyze_packet(src_ip, dst_ip, dst_port, protocol)

            alert = f"""
[AI ALERT] {timestamp}
{'-'*50}
Packet : {src_ip} -> {dst_ip}:{dst_port}
{ai_result}
{'-'*50}"""
            print(f"\033[96m{alert}\033[0m")
            save_log(alert)
        else:
            print(f"\033[92m{log}\033[0m")
            save_log(log)

print("[*] AI-SOC Monitor Started... (Ctrl+C to stop)")
print(f"[*] Watching for suspicious ports: {SUSPICIOUS_PORTS}")
print(f"[*] Logs saving to: {LOG_FILE}\n")
sniff(prn=packet_handler, store=False)