"""
跨交易所聚合引擎 API
提供多交易所价格聚合和套利机会扫描
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, List
import random
import time

router = APIRouter(prefix="/api/arbitrage", tags=["arbitrage"])

# 模拟各交易所价格
SIMULATED_PRICES = {
    "BTC/USDT": {
        "binance": 67500.0,
        "okx": 67520.0,
        "bybit": 67510.0,
        "kucoin": 67480.0,
        "gate": 67530.0,
        "huobi": 67490.0,
        "bitget": 67500.0,
    },
    "ETH/USDT": {
        "binance": 3450.0,
        "okx": 3455.0,
        "bybit": 3452.0,
        "kucoin": 3448.0,
        "gate": 3458.0,
    },
    "SOL/USDT": {
        "binance": 185.0,
        "okx": 185.5,
        "bybit": 185.2,
        "kucoin": 184.8,
    },
    "XRP/USDT": {
        "binance": 0.52,
        "okx": 0.521,
        "bybit": 0.519,
        "kucoin": 0.518,
    },
}

@router.get("/prices/{symbol}")
async def get_prices(symbol: str):
    """获取指定交易对的各交易所价格"""
    prices = SIMULATED_PRICES.get(symbol.upper())
    if not prices:
        # 返回默认价格
        prices = {
            "binance": 100.0 + random.randint(-50, 50),
            "okx": 100.0 + random.randint(-50, 50),
            "bybit": 100.0 + random.randint(-50, 50),
            "kucoin": 100.0 + random.randint(-50, 50),
        }
    
    # 添加小幅波动模拟实时价格
    for ex in prices:
        prices[ex] = prices[ex] * (1 + random.uniform(-0.001, 0.001))
    
    return {"symbol": symbol.upper(), "prices": prices}

class ScanRequest(BaseModel):
    symbol: str
    amount: float = 1000.0
    min_spread: float = 0.5
    auto_execute: bool = False

@router.post("/scan")
async def scan_arbitrage(req: ScanRequest):
    """扫描套利机会"""
    symbol = req.symbol.upper()
    prices = SIMULATED_PRICES.get(symbol, {})
    
    if len(prices) < 2:
        return {"success": False, "message": "价格数据不足"}
    
    # 找出最低价和最高价
    sorted_prices = sorted(prices.items(), key=lambda x: x[1])
    buy_exchange, buy_price = sorted_prices[0]
    sell_exchange, sell_price = sorted_prices[-1]
    
    # 计算价差
    spread_percent = ((sell_price - buy_price) / buy_price) * 100
    
    # 估算收益
    amount = req.amount
    estimated_profit = (sell_price - buy_price) * (amount / buy_price)
    
    signal = {
        "symbol": symbol,
        "buy_exchange": buy_exchange,
        "sell_exchange": sell_exchange,
        "buy_price": buy_price,
        "sell_price": sell_price,
        "spread_percent": round(spread_percent, 3),
        "estimated_profit": round(estimated_profit, 2),
        "auto_execute": req.auto_execute,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    
    return {
        "success": True,
        "signal": signal,
        "spread_percent": round(spread_percent, 3),
    }

@router.get("/exchanges")
async def get_supported_exchanges():
    """获取支持的交易所列表"""
    return {
        "exchanges": [
            {"id": "binance", "name": "Binance", "region": "🌏 亚太"},
            {"id": "okx", "name": "OKX", "region": "🌏 ��太"},
            {"id": "bybit", "name": "Bybit", "region": "🌏 亚太"},
            {"id": "kucoin", "name": "KuCoin", "region": "🌏 亚太"},
            {"id": "gate", "name": "Gate.io", "region": "🌏 亚太"},
            {"id": "huobi", "name": "Huobi", "region": "🌏 亚太"},
            {"id": "bitget", "name": "Bitget", "region": "🌏 亚太"},
            {"id": "bitflyer", "name": "bitFlyer", "region": "🇯🇵 日本"},
            {"id": "coincheck", "name": "Coincheck", "region": "🇯🇵 日本"},
            {"id": "upbit", "name": "Upbit", "region": "🇰🇷 韩国"},
            {"id": "bithumb", "name": "Bithumb", "region": "🇰🇷 韩国"},
            {"id": "coinbase", "name": "Coinbase", "region": "🇺🇸 美国"},
            {"id": "kraken", "name": "Kraken", "region": "🇺🇸 美国"},
            {"id": "gemini", "name": "Gemini", "region": "🇺🇸 美国"},
            {"id": "bitstamp", "name": "Bitstamp", "region": "🇪🇺 欧洲"},
        ]
    }