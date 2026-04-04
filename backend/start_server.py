"""QuantAI 后端启动脚本"""
import sys
import os

# 设置输出编码
sys.stdout.reconfigure(encoding='utf-8')

print("=" * 50)
print("🚀 QuantAI Backend Starting...")
print("=" * 50)

# 导入并启动
import uvicorn
from dotenv import load_dotenv

load_dotenv()
print("✅ Environment loaded")

# 检查Groq API
groq_key = os.getenv("GROQ_API_KEY", "")
if groq_key:
    print(f"✅ Groq API Key: {groq_key[:10]}...")
else:
    print("⚠️ Groq API Key not found!")

print("✅ Starting server on http://localhost:8001")
print("=" * 50)

uvicorn.run(
    "main:app",
    host="0.0.0.0",
    port=8001,
    reload=False,
    log_level="info"
)