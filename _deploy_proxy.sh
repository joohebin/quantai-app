#!/bin/bash
cd /home/ubuntu/quantai-app

# Kill old frontend server
pkill -f "http.server 8080" 2>/dev/null || true
sleep 1

# Start new proxy server
nohup python3 /home/ubuntu/quantai-app/_proxy_server.py 8080 >> /home/ubuntu/quantai-app/frontend.log 2>&1 &

echo "Frontend proxy started"
sleep 2
ps aux | grep "_proxy_server" | grep -v grep
