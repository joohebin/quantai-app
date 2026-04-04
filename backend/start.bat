@echo off
cd /d %~dp0
echo Starting QuantAI Backend...
python -m uvicorn main:app --host 0.0.0.0 --port 8000
