"""
QuantAI - MetaApi MT5 市场数据路由
通过 MetaApi REST API 获取 INFINOX MT5 的实时行情
覆盖：外汇、贵金属、能源、指数、国债
"""
from fastapi import APIRouter
from typing import Optional, List
from pydantic import BaseModel
import httpx
import os

router = APIRouter(prefix="/api/meta-market", tags=["MT5行情"])

# MetaApi Account Token（INFINOX MT5 ECN - 3791ec3f-4ef6-493f-b460-4cdbc40e33e4）(2026-04-22 更新)
METAAPI_TOKEN = (
    "eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI3MTI1Mzc1MTA0YjcwNjVkNzliNDMwMDRiMjMwYjkyYyIsImFjY2Vzc1J1bGVzIjpbeyJpZCI6InRyYWRpbmctYWNjb3VudC1tYW5hZ2VtZW50LWFwaSIsIm1ldGhvZHMiOlsidHJhZGluZy1hY2NvdW50LW1hbmFnZW1lbnQtYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiXSwicmVzb3VyY2VzIjpbImFjY291bnQ6JFVTRVJfSUQkOjM3OTFlYzNmLTRlZjYtNDkzZi1iNDYwLTRjZGJjNDBlMzNlNCJdfSx7ImlkIjoibWV0YWFwaS1yZXN0LWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiYWNjb3VudDokVVNFUl9JRCQ6Mzc5MWVjM2YtNGVmNi00OTNmLWI0NjAtNGNkYmM0MGUzM2U0Il19LHsiaWQiOiJtZXRhYXBpLXJwYy1hcGkiLCJtZXRob2RzIjpbIm1ldGFhcGktYXBpOndzOnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyJhY2NvdW50OiRVU0VSX0lEJDozNzkxZWMzZi00ZWY2LTQ5M2YtYjQ2MC00Y2RiYzQwZTMzZTQiXX0seyJpZCI6Im1ldGFhcGktcmVhbC10aW1lLXN0cmVhbWluZy1hcGkiLCJtZXRob2RzIjpbIm1ldGFhcGktYXBpOndzOnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyJhY2NvdW50OiRVU0VSX0lEJDozNzkxZWMzZi00ZWY2LTQ5M2YtYjQ2MC00Y2RiYzQwZTMzZTQiXX0seyJpZCI6Im1ldGFzdGF0cy1hcGkiLCJtZXRob2RzIjpbIm1ldGFzdGF0cy1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciJdLCJyZXNvdXJjZXMiOlsiYWNjb3VudDokVVNFUl9JRCQ6Mzc5MWVjM2YtNGVmNi00OTNmLWI0NjAtNGNkYmM0MGUzM2U0Il19LHsiaWQiOiJyaXNrLW1hbmFnZW1lbnQtYXBpIiwibWV0aG9kcyI6WyJyaXNrLW1hbmFnZW1lbnQtYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiXSwicmVzb3VyY2VzIjpbImFjY291bnQ6JFVTRVJfSUQkOjM3OTFlYzNmLTRlZjYtNDkzZi1iNDYwLTRjZGJjNDBlMzNlNCJdfSx7ImlkIjoiY29weWZhY3RvcnktYXBpIiwibWV0aG9kcyI6WyJjb3B5ZmFjdG9yeS1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiYWNjb3VudDokVVNFUl9JRCQ6KjM3OTFlYzNmLTRlZjYtNDkzZi1iNDYwLTRjZGJjNDBlMzNlNCIsIio6JFVTRVJfSUQkOjM3OTFlYzNmLTRlZjYtNDkzZi1iNDYwLTRjZGJjNDBlMzNlNCIsInN0cmF0ZWd5OiRVU0VSX0lEJDozNzkxZWMzZi00ZWY2LTQ5M2YtYjQ2MC00Y2RiYzQwZTMzZTQiLCJwb3J0Zm9saW86JFVTRVJfSUQkOjM3OTFlYzNmLTRlZjYtNDkzZi1iNDYwLTRjZGJjNDBlMzNlNCIsInN1YnNjcmliZXI6JFVTRVJfSUQkOjM3OTFlYzNmLTRlZjYtNDkzZi1iNDYwLTRjZGJjNDBlMzNlNCJdfSx7ImlkIjoibXQtbWFuYWdlci1hcGkiLCJtZXRob2RzIjpbIm10LW1hbmFnZXItYXBpOnJlc3Q6ZGVhbGluZzoqOioiLCJtdC1tYW5hZ2VyLWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqMzc5MWVjM2YtNGVmNi00OTNmLWI0NjAtNGNkYmM0MGUzM2U0IiwibXQtbWFuYWdlcjokVVNFUl9JRCQ6Mzc5MWVjM2YtNGVmNi00OTNmLWI0NjAtNGNkYmM0MGUzM2U0IiwibXQtYWNjb3VudDokVVNFUl9JRCQ6Mzc5MWVjM2YtNGVmNi00OTNmLWI0NjAtNGNkYmM0MGUzM2U0IiwibXQtZ3JvdXA6JFVTRVJfSUQkOjM3OTFlYzNmLTRlZjYtNDkzZi1iNDYwLTRjZGJjNDBlMzNlNCJdfSx7ImlkIjoiYmlsbGluZy1hcGkiLCJtZXRob2RzIjpbImJpbGxpbmctYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOiozNzkxZWMzZi00ZWY2LTQ5M2YtYjQ2MC00Y2RiYzQwZTMzZTQiXX1dLCJpZ25vcmVSYXRlTGltaXRzIjpmYWxzZSwidG9rZW5JZCI6IjIwMjEwMjEzIiwiaW1wZXJzb25hdGVkIjpmYWxzZSwicmVhbFVzZXJJZCI6IjcxMjUzNzUxMDRiNzA2NWQ3OWI0MzAwNGIyMzBiOTJjIiwiaWF0IjoxNzc2MjY3OTUyfQ.WcqTOYOXcgH81r-UdLyWzUSZjVq2fwnE98HVC6fahDcikYavgTHm4AgdQqytBeYMUcSvxg_7qcjtpvTi6TpRq7TEMFpnwMu8A3jQLzJREkOtxipvrJKG7S8I3M1IWrInkBUodZ1RHKwZl86r9M3WPYhvtPtRnvDrEvBJhLKimYgssPNLVvLsCjX5-9J22H7A0TRQunsCmLt_idHKXBp7wW-zjv2z9agOXEHAsnijpgOy_tg3rDTVVRq6d6T4rxT7uVyJX5WNh4U4AsvN2hO5zAKfWYRN2xqrAw_b_C5YWXzguZ3GvUjkme31MfATBjmVl0IvUlKlUbqEuD_cey0D6IGjKmXW6A9gOckoGkWMFhUKngLlH08j0qAqTfP5sMtCFB8mqGyjHJsg0_wemP0wLafGbM_1n_LXV-2Iu90YBl_Zexv9wTzW1dtUsfNJnxc6F4Ip0zZf1A5ljo26w0rNuh_MQvpw_8j3Hun-YsBcqz1S_tURSFZ4oiUC43xhLO4DV3Uf4hX9CSwLWruRBn8uWMMWc_JcllJmX1YGJP48_1-8HjETuvwrzdw5kYfwbMvR_tfUnENjdgBT4XNDl7CL8ioIyowAGJGbGZ7l2RSF1um-OMBmPkgJ6gX4JPq1cBag1FTZYJLCcyy2z8AmbUrKSbUPlBMjobcs7srD8eRtR5c"
)
ACCOUNT_ID = "3791ec3f-4ef6-493f-b460-4cdbc40e33e4"  # INFINOX_MT5_ECN

# MetaApi API 端点（cloud-g2，伦敦节点）
MT5_BASE = "https://mt-client-api-v1.agiliumtrade.agiliumtrade.ai"
PROVISION_BASE = "https://mt-provisioning-api-v1.agiliumtrade.agiliumtrade.ai"
RPC_BASE = "https://mt-rpc-api-v1.agiliumtrade.agiliumtrade.ai"

HEADERS = {"auth-token": METAAPI_TOKEN}
VERIFY_SSL = False  # London AWS 服务器 SSL 证书问题

# 符号映射：前端符号 → MT5 符号
MT5_SYMBOLS = {
    # 外汇
    "EUR/USD": "EURUSD",
    "GBP/USD": "GBPUSD",
    "USD/JPY": "USDJPY",
    "AUD/USD": "AUDUSD",
    "USD/CHF": "USDCHF",
    "USD/CAD": "USDCAD",
    "NZD/USD": "NZDUSD",
    "EUR/GBP": "EURGBP",
    "EUR/JPY": "EURJPY",
    "GBP/JPY": "GBPJPY",
    # 贵金属
    "XAU/USD": "XAUUSD",  # 黄金
    "XAG/USD": "XAGUSD",  # 白银
    "XPT/USD": "XPTUSD",  # 铂金
    "XPD/USD": "XPDUSD",  # 钯金
    # 能源
    "USOIL": "USOIL",     # WTI 原油
    "UKOIL": "UKOIL",     # 布伦特原油
    "NATGAS": "NATGAS",   # 天然气
    # 指数
    "US100": "US100",
    "US500": "US500",
    "US30": "US30",
    "GER40": "GER40",
    "UK100": "UK100",
    "JPN225": "JPN225",
    "NAS100": "NAS100",
    "SPX500": "SPX500",
    "DOW": "DOW",
    "HSI": "HSI",
    "NSX": "NSX",
    "CAC40": "CAC40",
    "AEX": "AEX",
    "STOXX50": "STOXX50",
    # 国债
    "US10YT": "US10YT",   # 美10年期国债
    "US5YT": "US5YT",     # 美5年期国债
    "US2YT": "US2YT",     # 美2年期国债
    "DE10YT": "DE10YT",   # 德10年期国债
    "UK10YT": "UK10YT",   # 英10年期国债
}

# 反向报价符号（USD/JPY 这种，1 USD = X JPY）
REVERSE_QUOTE_SYMBOLS = {"USD/JPY", "USD/CHF", "EUR/JPY", "GBP/JPY"}


def _parse_mt5_price(symbol: str, price_str: str) -> Optional[float]:
    """解析 MT5 价格字符串为浮点数"""
    try:
        if not price_str or price_str == "null":
            return None
        return float(price_str)
    except:
        return None


def _convert_to_ui_symbol(symbol: str, mt5_price: float) -> dict:
    """将 MT5 行情转为前端统一格式"""
    # 处理反向报价：1 USD = X JPY → 1 JPY = 1/X USD
    if symbol in REVERSE_QUOTE_SYMBOLS:
        if mt5_price and mt5_price > 0:
            ui_price = round(1 / mt5_price, 4)
        else:
            ui_price = mt5_price
    else:
        ui_price = mt5_price

    # 判断类型
    if symbol in ["XAU/USD"]:
        stype = "metal"
    elif symbol in ["XAG/USD", "XPT/USD", "XPD/USD"]:
        stype = "metal"
    elif symbol in ["USOIL", "UKOIL", "NATGAS"]:
        stype = "energy"
    elif symbol in ["US100", "US500", "US30", "NAS100", "SPX500", "DOW",
                    "GER40", "UK100", "JPN225", "HSI", "CAC40", "AEX", "STOXX50"]:
        stype = "index"
    elif symbol in ["US10YT", "US5YT", "US2YT", "DE10YT", "UK10YT"]:
        stype = "bond"
    elif "/" in symbol:
        stype = "forex"
    else:
        stype = "unknown"

    return {
        "symbol": symbol,
        "price": ui_price,
        "type": stype,
        "change_pct": 0.0,  # current-tick 不包含涨跌幅，用 0
    }


async def _fetch_mt5_tick(symbol: str) -> Optional[dict]:
    """从 MetaApi MT5 获取单个品种的实时报价"""
    mt5_sym = MT5_SYMBOLS.get(symbol)
    if not mt5_sym:
        return None

    url = f"{MT5_BASE}/users/current/accounts/{ACCOUNT_ID}/symbols/{mt5_sym}/current-tick"

    try:
        async with httpx.AsyncClient(timeout=15.0, verify=VERIFY_SSL) as client:
            r = await client.get(url, headers=HEADERS)
            if r.status_code == 401:
                print(f"[MetaApi] 401 Unauthorized for {symbol} - Token可能已失效")
                return None
            if r.status_code == 404:
                print(f"[MetaApi] {symbol} not found on MT5 account")
                return None
            if r.status_code != 200:
                print(f"[MetaApi] HTTP {r.status_code}: {r.text[:100]}")
                return None

            d = r.json()
            price = _parse_mt5_price(symbol, d.get("bid", "") or d.get("ask", ""))
            return _convert_to_ui_symbol(symbol, price)

    except Exception as e:
        print(f"[MetaApi] Failed {symbol}: {e}")
        return None


@router.get("/quotes")
async def get_mt5_quotes():
    """
    获取所有 MT5 品种的实时报价
    GET /api/meta-market/quotes
    """
    symbols = list(MT5_SYMBOLS.keys())
    results = []

    import asyncio
    tasks = [_fetch_mt5_tick(sym) for sym in symbols]
    fetched = await asyncio.gather(*tasks, return_exceptions=True)

    for sym, result in zip(symbols, fetched):
        if result and isinstance(result, dict) and result.get("price"):
            results.append(result)
        else:
            # 标记无法获取的品种（不显示，不降级）
            print(f"[MetaApi] No data for {sym}")

    return {
        "source": "mt5",
        "account": ACCOUNT_ID,
        "quotes": results,
        "count": len(results),
    }


@router.get("/quote/{symbol}")
async def get_single_quote(symbol: str):
    """
    获取单个品种的实时报价
    GET /api/meta-market/quote/{symbol}
    """
    # 符号规范化（EURUSD → EUR/USD）
    normalized = symbol
    if symbol not in MT5_SYMBOLS:
        # 尝试标准化格式（EURUSD → EUR/USD）
        for q in ["USD", "JPY", "CHF", "AUD", "CAD", "NZD"]:
            if symbol.endswith(q) and len(symbol) > 3:
                base = symbol[:-len(q)]
                candidate = f"{base}/{q}"
                if candidate in MT5_SYMBOLS:
                    normalized = candidate
                    break

    result = await _fetch_mt5_tick(normalized)
    if not result:
        return {"error": f"Symbol {symbol} not available on MT5 account", "price": None}
    return result


@router.get("/symbols")
async def get_available_symbols():
    """
    获取 MT5 账户上所有可用的交易品种
    GET /api/meta-market/symbols
    """
    url = f"{MT5_BASE}/users/current/accounts/{ACCOUNT_ID}/symbols"

    try:
        async with httpx.AsyncClient(timeout=15.0, verify=VERIFY_SSL) as client:
            r = await client.get(url, headers=HEADERS)
            if r.status_code != 200:
                return {"error": r.text, "symbols": []}
            symbols = r.json()
            return {
                "account": ACCOUNT_ID,
                "symbols": symbols,
                "count": len(symbols),
            }
    except Exception as e:
        return {"error": str(e), "symbols": []}