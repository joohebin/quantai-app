#!/bin/bash
cd /home/ubuntu/quantai-app
pkill -f uvicorn 2>/dev/null || true
sleep 1
export PYTHONPATH=/home/ubuntu/quantai-app/backend
nohup python3 -m uvicorn main:app --host 0.0.0.0 --port 8001 > /tmp/uvicorn.log 2>&1 &
sleep 3
echo "=== startup log ==="
tail -10 /tmp/uvicorn.log
echo "=== process ==="
ps aux | grep uvicorn | grep -v grep