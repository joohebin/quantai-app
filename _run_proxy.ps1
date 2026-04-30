# Kill old http.server on 8080
ssh -i "C:\Users\Administrator\.ssh\quantai-key-london.pem" ubuntu@35.179.161.45 "pkill -f 'http.server 8080' || true"
Start-Sleep -Seconds 2
# Start new proxy server
ssh -i "C:\Users\Administrator\.ssh\quantai-key-london.pem" ubuntu@35.179.161.45 "nohup python3 /home/ubuntu/quantai-app/_proxy_server.py 8080 >> /home/ubuntu/quantai-app/frontend.log 2>&1 &"
Start-Sleep -Seconds 2
# Test
ssh -i "C:\Users\Administrator\.ssh\quantai-key-london.pem" ubuntu@35.179.161.45 "curl -s -X POST http://localhost:8001/api/cs/chat -H 'Content-Type: application/json' -d '{\"message\":\"test\"}' --max-time 15"
