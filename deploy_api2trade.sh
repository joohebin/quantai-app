#!/bin/bash
# API2Trade 集成部署脚本
# 在 AWS 服务器上执行此脚本

set -e

echo "=========================================="
echo "API2Trade 集成部署"
echo "=========================================="

# 切换到项目目录
cd /home/ubuntu/quantai-app

# 拉取最新代码
echo "[1/5] 拉取最新代码..."
git pull origin main

# 安装 httpx (API2Trade 需要)
echo "[2/5] 安装 httpx..."
pip install httpx --quiet

# 重启后端服务
echo "[3/5] 重启 QuantAI 后端服务..."
pm2 restart quantai-backend || pm2 start "uvicorn backend.main:app --host 0.0.0.0 --port 8000" --name quantai-backend

# 等待服务启动
sleep 3

# 测试 API2Trade 端点
echo "[4/5] 测试 API2Trade 端点..."
curl -s http://localhost:8000/api/api2trade/status || echo "注意: 需要先配置 API Key"

# 检查服务状态
echo "[5/5] 检查服务状态..."
pm2 status

echo ""
echo "=========================================="
echo "部署完成!"
echo "=========================================="
echo ""
echo "下一步:"
echo "1. 配置 API2Trade API Key:"
echo "   curl -X POST http://localhost:8000/api/api2trade/connect \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"api_key\": \"your_key_here\"}'"
echo ""
echo "2. 添加 MT4/MT5 账户:"
echo "   curl -X POST http://localhost:8000/api/api2trade/accounts \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"server\": \"MetaQuotes-Demo\", \"login\": \"100112408\", \"password\": \"xxx\"}'"
echo ""
echo "3. 测试下单:"
echo "   curl -X POST http://localhost:8000/api/api2trade/trade \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"account_id\": \"xxx\", \"symbol\": \"EURUSD\", \"side\": \"buy\", \"lots\": 0.01}'"
