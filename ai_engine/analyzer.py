import sys
import os
sys.stdout.reconfigure(encoding='utf-8')

from groq import Groq

def analyze_packet(src_ip, dst_ip, dst_port, protocol):

    client = Groq(api_key = "YOUR_GROQ_API_KEY")

    prompt = f"""You are a SOC security analyst. Analyze this network packet.

Packet Info:
- Source IP: {src_ip}
- Destination IP: {dst_ip}
- Port: {dst_port}
- Protocol: {protocol}

Reply in this exact format only:
THREAT_LEVEL: HIGH or MEDIUM or LOW
ATTACK_TYPE: name of attack
EXPLANATION: one sentence
ACTION: what to do"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=300
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"ERROR: {str(e)}"


if __name__ == "__main__":
    print("[*] Testing AI Analyzer...")
    print("[*] Sending packet to Groq AI...\n")

    result = analyze_packet(
        src_ip="192.168.1.100",
        dst_ip="10.0.0.1",
        dst_port=22,
        protocol="TCP"
    )

    print("[AI Analysis Result]")
    print("-" * 40)
    print(result)
    print("-" * 40)