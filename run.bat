@echo off
echo Starting AI-SOC Monitor...
start cmd /k "python capture/packet_capture.py"
timeout /t 2
start cmd /k "python -m streamlit run dashboard/soc_dashboard.py"
echo Dashboard starting at http://localhost:8501