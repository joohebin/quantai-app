#!/bin/bash
# QuantAI Backend Service — run on EC2
cd /home/ubuntu/quantai-backend
source venv/bin/activate 2>/dev/null || true
pip install -r requirements.txt -q
uvicorn main:app --host 0.0.0.0 --port 8002 --workers 2
