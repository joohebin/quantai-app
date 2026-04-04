"""
QuantAI - 行情路由（模拟 + 真实数据预留）
"""
from fastapi import APIRouter, Depends, Query
from typing import List, Optional
import random
import math
import time
from datetime import datetime
from schemas import MarketQuote
import auth
import models

router = APIRouter(prefix="/api/market", tags=["行情"])

# 基准价格（真实数据时替换为 CCXT 拉取）
BASE_PRICES = {
    # 加密货币
    "BTC/USDT":  {"price": 83250.0, "type": "crypto"},
    "ETH/USDT":  {"price": 1840.0,  "type": "crypto"},
    "SOL/USDT":  {"price": 128.5,   "type": "crypto"},
    "BNB/USDT":  {"price": 595.0,   "type": "crypto"},
    "XRP/USDT":  {"price": 2.15,    "type": "crypto"},
    # 外汇
    "EUR/USD":   {"price": 1.0831,  "type": "forex"},
    "GBP/USD":   {"price": 1.2645,  "type": "forex"},
    "USD/JPY":   {"price": 149.82,  "type": "forex"},
    "AUD/USD":   {"price": 0.6318,  "type": "forex"},
    "USD/CHF":   {"price": 0.8934,  "type": "forex"},
    # 贵金属
    "XAU/USD":   {"price": 2942.30, "type": "metal"},
    "XAG/USD":   {"price": 32.84,   "type": "metal"},
    # 能源
    "CL/USD":    {"price": 71.25,   "type": "energy"},
    "NG/USD":    {"price": 3.87,    "type": "energy"},
    "WTI/USD":   {"price": 71.25,   "type": "energy"},  # WTI = CL
    "BRENT":     {"price": 75.50,   "type": "energy"},
    # 指数
    "NQ/USD":    {"price": 19856.0, "type": "index"},
    "ES/USD":    {"price": 5512.0,  "type": "index"},
    "HSI/HKD":   {"price": 23418.0, "type": "index"},
    # 前端简化名称别名（映射到标准 symbol）
    "NAS100":    {"alias": "NQ/USD",   "price": 18240.0,  "type": "index"},
    "SPX500":    {"alias": "ES/USD",   "price": 5142.0,   "type": "index"},
    "DOW":       {"alias": "ES/USD",   "price": 38420.0,  "type": "index"},
    "HSI":       {"alias": "HSI/HKD",  "price": 17820.0,  "type": "index"},
    "WTI":       {"alias": "CL/USD",   "price": 71.25,    "type": "energy"},
}

# Symbol 别名映射表（用于查询）
SYMBOL_ALIASES = {
    "NAS100": "NQ/USD",
    "SPX500": "ES/USD",
    "DOW": "ES/USD",
    "HSI": "HSI/HKD",
    "WTI": "CL/USD",
    "BRENT": "BRENT",  # 保持原样
}

def _resolve_symbol(symbol: str) -> str:
    """解析 symbol 别名，返回标准 symbol"""
    return SYMBOL_ALIASES.get(symbol, symbol)

def _get_symbol_info(symbol: str) -> dict:
    """获取 symbol 信息，自动解析别名"""
    if symbol in BASE_PRICES:
        return BASE_PRICES[symbol]
    resolved = _resolve_symbol(symbol)
    if resolved in BASE_PRICES:
        return BASE_PRICES[resolved]
    return None

# 每次调用随机波动模拟
_price_state = {sym: {"price": d["price"], "change_pct": 0.0} for sym, d in BASE_PRICES.items()}


def _simulate_tick(symbol: str):
    """模拟价格波动，自动处理别名"""
    resolved = _resolve_symbol(symbol)
    # 别名独立维护状态
    if symbol != resolved and symbol not in _price_state:
        _price_state[symbol] = {"price": BASE_PRICES.get(symbol, {}).get("price", 1000.0), "change_pct": 0.0}
    state = _price_state.get(resolved, _price_state.get(symbol, _price_state.get(resolved, {"price": 1000.0, "change_pct": 0.0})))
    # 随机游走
    drift = random.gauss(0, 0.0008)
    state["price"] *= (1 + drift)
    state["change_pct"] += drift * 100
    return state


@router.get("/quotes", response_model=List[MarketQuote])
def get_quotes(
    category: Optional[str] = Query(None, description="crypto/forex/metal/energy/index"),
    symbols: Optional[str] = Query(None, description="逗号分隔，如 BTC/USDT,ETH/USDT")
):
    """获取所有行情（或筛选），支持前端简化的 symbol 名称"""
    result = []
    now_str = datetime.utcnow().isoformat() + "Z"

    # 获取所有标准 symbol + 别名
    all_symbols = set(BASE_PRICES.keys()) | set(SYMBOL_ALIASES.keys())
    target_symbols = list(all_symbols)
    
    if symbols:
        # 支持前端传入的简化名称
        target_symbols = []
        for s in symbols.split(","):
            s = s.strip()
            if s in all_symbols:
                target_symbols.append(s)
            elif s in SYMBOL_ALIASES and SYMBOL_ALIASES[s] in BASE_PRICES:
                target_symbols.append(s)
    
    if category:
        target_symbols = [s for s in target_symbols if _get_symbol_type(s) == category]

    for sym in target_symbols:
        info = _get_symbol_info(sym)
        if not info:
            continue
        state = _simulate_tick(sym)
        base = info["price"]
        price = state["price"]
        change_pct = state["change_pct"]
        change = price - base

        result.append(MarketQuote(
            symbol=sym,
            price=round(price, 4 if "/" in sym and "USD" in sym and price < 10 else 2),
            change=round(change, 4),
            change_pct=round(change_pct, 2),
            volume=round(random.uniform(1e6, 1e9), 0),
            high_24h=round(price * 1.02, 2),
            low_24h=round(price * 0.98, 2),
            updated_at=now_str
        ))

    return result


def _get_symbol_type(symbol: str) -> str:
    """获取 symbol 类型"""
    if symbol in BASE_PRICES:
        return BASE_PRICES[symbol].get("type", "")
    resolved = _resolve_symbol(symbol)
    if resolved in BASE_PRICES:
        return BASE_PRICES[resolved].get("type", "")
    return ""


@router.get("/kline/{symbol:path}")
def get_kline(
    symbol: str,
    timeframe: str = Query("1h", description="1m/5m/15m/1h/4h/1d"),
    limit: int = Query(200, ge=10, le=1000)
):
    """获取K线数据（模拟，真实环境对接 CCXT），支持前端简化的 symbol 名称"""
    info = _get_symbol_info(symbol)
    base_price = info["price"] if info else 1000.0
    candles = []
    now_ts = int(time.time())

    # 时间间隔（秒）
    tf_map = {"1m": 60, "5m": 300, "15m": 900, "1h": 3600, "4h": 14400, "1d": 86400}
    interval = tf_map.get(timeframe, 3600)

    price = base_price * 0.85
    for i in range(limit):
        ts = (now_ts - (limit - i) * interval) * 1000  # 毫秒
        open_ = price
        change = random.gauss(0, 0.008)
        close = open_ * (1 + change)
        high = max(open_, close) * (1 + abs(random.gauss(0, 0.004)))
        low = min(open_, close) * (1 - abs(random.gauss(0, 0.004)))
        volume = random.uniform(1000, 50000)

        candles.append({
            "time": ts // 1000,   # lightweight-charts 用秒级时间戳
            "open": round(open_, 4),
            "high": round(high, 4),
            "low": round(low, 4),
            "close": round(close, 4),
            "volume": round(volume, 2)
        })
        price = close

    return {"symbol": symbol, "timeframe": timeframe, "candles": candles}


@router.get("/symbols")
def get_symbols():
    """获取所有支持的交易对"""
    return [
        {"symbol": sym, "type": info["type"], "base_price": info["price"]}
        for sym, info in BASE_PRICES.items()
    ]
