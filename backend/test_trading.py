import httpx, asyncio
import sys
sys.stdout.reconfigure(encoding='utf-8')

async def test():
    async with httpx.AsyncClient(timeout=120.0, base_url='http://localhost:8000') as client:
        print('=' * 60)
        print('🧪 OpenRouter AI 交易系统测试')
        print('=' * 60)
        
        # 1. 健康检查
        print('\n1️⃣ 健康检查')
        r = await client.get('/api/ai/health')
        print(f'Status: {r.status_code}')
        if r.status_code == 200:
            data = r.json()
            print(f'   Provider: {data["provider"]}')
            print(f'   Model: {data["current_model"]}')
            print(f'   Auto Trade: {data["auto_trade"]}')
        
        # 2. 可用模型
        print('\n2️⃣ 可用模型')
        r = await client.get('/api/ai/models')
        if r.status_code == 200:
            for m in r.json()['models']:
                print(f'   - {m["name"]}: {m["use_case"]}')
        
        # 3. AI对话（DeepSeek）
        print('\n3️⃣ AI对话 (DeepSeek V3.2)')
        r = await client.post('/api/ai/chat', 
            json={'message': 'BTC现在怎么看？可以做多吗？', 'symbol': 'BTC'}
        )
        print(f'Status: {r.status_code}')
        if r.status_code == 200:
            data = r.json()
            print(f'Model: {data.get("model")}')
            print(f'Signal: {data.get("signal")}')
            print(f'\nAI响应:\n{data.get("message", "")[:400]}')
        
        # 4. 市场分析
        print('\n4️⃣ 市场分析')
        r = await client.post('/api/ai/analyze', 
            params={'symbol': 'ETH', 'timeframe': '1h'}
        )
        print(f'Status: {r.status_code}')
        if r.status_code == 200:
            data = r.json()
            print(f'Model: {data.get("model")}')
            print(f'Signal: {data.get("signal")}')
        
        # 5. 启用自动交易
        print('\n5️⃣ 启用自动交易')
        r = await client.post('/api/ai/auto-trade/enable', params={'enable': True})
        print(f'Status: {r.status_code}')
        print(r.json())
        
        print('\n' + '=' * 60)
        print('✅ 所有测试完成!')
        print('=' * 60)

asyncio.run(test())
