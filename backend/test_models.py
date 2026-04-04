import sys, asyncio, httpx
sys.stdout.reconfigure(encoding='utf-8')

API_KEY = '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'

async def test():
    async with httpx.AsyncClient(timeout=60.0) as client:
        print('获取可用模型列表...')
        r = await client.get('https://openrouter.ai/api/v1/models',
            headers={'Authorization': f'Bearer {API_KEY}'}
        )
        if r.status_code == 200:
            models = r.json()['data']
            print(f'共有 {len(models)} 个模型可用')
            # 找相关模型
            targets = ['qwen', 'deepseek', 'yi', 'minimax']
            for t in targets:
                matches = [m for m in models if t in m['id'].lower()]
                if matches:
                    print(f'\n{t.upper()} 模型:')
                    for m in matches[:3]:
                        print(f"  - {m['id']}")

asyncio.run(test())
