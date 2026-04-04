"""测试Groq AI对接"""
import os, httpx, asyncio, json, sys
from dotenv import load_dotenv

# 修复Windows编码问题
sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
model = os.getenv("GROQ_MODEL")

system_prompt = """你是一个专业的量化交易AI助手。用中文回答，简洁专业。
分析格式：
📊 【BTC/USDT 分析】
🎯 趋势：[判断]
💰 关键位：阻力XXXXX | 支撑XXXXX
⚡ 建议：[做多/做空/观望]
🛡️ 风险提示：[止损位]"""

async def test():
    print(f"Testing Groq API with model: {model}")
    print("-" * 50)
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        r = await client.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            },
            json={
                'model': model,
                'messages': [
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': 'BTC现在怎么看？给个详细分析'}
                ],
                'temperature': 0.7,
                'max_tokens': 800
            }
        )
        
        if r.status_code == 200:
            result = r.json()
            response = result['choices'][0]['message']['content']
            print("✅ AI Response:")
            print(response)
        else:
            print("❌ Error:", r.json())

if __name__ == "__main__":
    asyncio.run(test())
