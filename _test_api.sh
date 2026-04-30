#!/bin/bash
# 获取 token
TOKEN=$(curl -s -X POST 'http://localhost:8001/api/auth/login' \
  -H 'Content-Type: application/json' \
  -d '{"email":"joohebin220@gmail.com","password":"Kc530220@"}' | python3 -c "import sys,json;print(json.load(sys.stdin)['access_token'])")

echo "Token: $TOKEN"
echo ""

# 测试 broker 连接
curl -s -X POST 'http://localhost:8001/api/brokers/forex/connect' \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"broker_name":"INFINOX","email":"87954362","password":"Kc530220@","server":"ECN Server","account_type":"real","broker_type":"forex"}'
