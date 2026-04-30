"""
TradeMux MT5 API 集成路由
通过 TradeMux EA 获取 MT5 账户数据、实时价格、持仓信息
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/api/trademux", tags=["TradeMux"])

TRADEMUX_API_KEY = os.getenv("TRADEMUX_API_KEY", "")
TRADEMUX_BASE_URL = os.getenv("TRADEMUX_BASE_URL", "https://mux.skybluefin.tech")

# ============ 请求/响应模型 ============

class PriceRequest(BaseModel):
    symbol: str

class OHLCRequest(BaseModel):
    symbol: str
    timeframe: str = "1h"
    from_date: Optional[int] = None
    to_date: Optional[int] = None

class OrderRequest(BaseModel):
    symbol: str
    volume: float
    order_type: str  # BUY or SELL
    price: Optional[float] = None  # 限价单价格，挂单时需要
    comment: Optional[str] = None
    magic: Optional[int] = None

class ClosePositionRequest(BaseModel):
    ticket: int

class CloseByMagicRequest(BaseModel):
    magic: int

# ============ 辅助函数 ============

async def trademux_request(method: str, endpoint: str, json_data: dict = None):
    """TradeMux API 请求封装"""
    url = f"{TRADEMUX_BASE_URL}/{endpoint.lstrip('/')}"
    headers = {
        "x-api-key": TRADEMUX_API_KEY,
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        if method.upper() == "GET":
            response = await client.get(url, headers=headers)
        else:
            response = await client.post(url, headers=headers, json=json_data)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 422:
            # 参数验证错误
            raise HTTPException(status_code=422, detail=response.json())
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"TradeMux API Error: {response.text}"
            )

# ============ API 端点 ============

@router.get("/health")
async def health_check():
    """TradeMux 服务健康检查"""
    try:
        data = await trademux_request("GET", "v1/health")
        return {"status": "ok", "trademux": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.get("/key-info")
async def get_key_info():
    """获取 API Key 信息"""
    try:
        data = await trademux_request("GET", "v1/key-info")
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/account")
async def get_account():
    """获取 MT5 账户信息"""
    try:
        data = await trademux_request("GET", "v1/account")
        return {
            "balance": data.get("balance"),
            "equity": data.get("equity"),
            "account_number": data.get("account_number"),
            "server": data.get("server"),
            "open_positions": data.get("open_positions"),
            "open_trades": data.get("open_trades"),
            "pending_orders": data.get("pending_orders"),
            "floating_pnl": data.get("floating_pnl"),
            "updated_at": data.get("updated_at")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/positions")
async def get_positions():
    """获取当前持仓"""
    try:
        data = await trademux_request("GET", "v1/positions")
        return {
            "total_count": data.get("total_count"),
            "positions": data.get("positions", []),
            "status": data.get("status")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/orders")
async def get_orders():
    """获取挂单（待成交订单）"""
    try:
        data = await trademux_request("GET", "v1/orders")
        return {
            "total_count": data.get("total_count"),
            "orders": data.get("orders", []),
            "status": data.get("status")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/instruments")
async def get_instruments():
    """获取可交易品种列表"""
    try:
        data = await trademux_request("GET", "v1/instruments")
        return {
            "instruments": data.get("instruments", []),
            "count": data.get("count")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/price")
async def get_price(request: PriceRequest):
    """获取实时价格"""
    try:
        data = await trademux_request("POST", "v1/data", {"symbol": request.symbol.upper()})
        return {
            "symbol": data.get("symbol"),
            "bid": data.get("bid"),
            "ask": data.get("ask"),
            "mid": data.get("mid"),
            "price": data.get("price"),
            "type": data.get("type"),
            "timestamp": data.get("server_response_received_at")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/prices")
async def get_prices(symbols: List[str]):
    """批量获取多个品种价格"""
    results = []
    for symbol in symbols:
        try:
            data = await trademux_request("POST", "v1/data", {"symbol": symbol.upper()})
            results.append({
                "symbol": data.get("symbol"),
                "bid": data.get("bid"),
                "ask": data.get("ask"),
                "mid": data.get("mid"),
                "type": data.get("type")
            })
        except Exception:
            results.append({"symbol": symbol, "error": "failed to fetch"})
    return {"prices": results}

@router.post("/ohlc")
async def get_ohlc(request: OHLCRequest):
    """获取 K 线数据"""
    try:
        payload = {
            "symbol": request.symbol.upper(),
            "timeframe": request.timeframe,
        }
        if request.from_date:
            payload["from_date"] = request.from_date
        if request.to_date:
            payload["to_date"] = request.to_date

        data = await trademux_request("POST", "v1/ohlc", payload)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/symbol-specs")
async def get_symbol_specs(request: PriceRequest):
    """获取交易品种规格"""
    try:
        data = await trademux_request("POST", "v1/symbol_specs", {"symbol": request.symbol.upper()})
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/history")
async def get_history(request: OHLCRequest):
    """获取交易历史"""
    try:
        payload = {
            "symbol": request.symbol.upper(),
            "timeframe": request.timeframe,
        }
        if request.from_date:
            payload["from_date"] = request.from_date
        if request.to_date:
            payload["to_date"] = request.to_date

        data = await trademux_request("POST", "v1/history", payload)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============ 交易功能 ============

@router.post("/order")
async def place_order(request: OrderRequest):
    """下单"""
    try:
        payload = {
            "symbol": request.symbol.upper(),
            "volume": request.volume,
            "order_type": request.order_type.upper(),
        }
        if request.price:
            payload["price"] = request.price
        if request.comment:
            payload["comment"] = request.comment
        if request.magic:
            payload["magic"] = request.magic

        data = await trademux_request("POST", "v1/order", payload)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/close-position")
async def close_position(request: ClosePositionRequest):
    """平仓"""
    try:
        data = await trademux_request("POST", "v1/close", {"ticket": request.ticket})
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/close-by-magic")
async def close_by_magic(request: CloseByMagicRequest):
    """按 Magic Number 平仓"""
    try:
        data = await trademux_request("POST", "v1/close_magic", {"magic": request.magic})
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/close-all")
async def close_all_positions():
    """平掉所有持仓"""
    try:
        data = await trademux_request("POST", "v1/close_all", {})
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/kill-switch")
async def kill_switch():
    """紧急平仓（Kill Switch）"""
    try:
        data = await trademux_request("POST", "v1/kill_switch", {})
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============ 仪表盘汇总 ============

@router.get("/dashboard")
async def get_dashboard():
    """获取完整仪表盘数据（账户 + 持仓 + 主要品种价格）"""
    try:
        # 并行获取多个数据
        async with httpx.AsyncClient(timeout=30.0) as client:
            headers = {
                "x-api-key": TRADEMUX_API_KEY,
                "Content-Type": "application/json"
            }

            # 获取账户信息
            account_resp = await client.get(
                f"{TRADEMUX_BASE_URL}/v1/account",
                headers=headers
            )
            account = account_resp.json() if account_resp.status_code == 200 else {}

            # 获取持仓
            positions_resp = await client.get(
                f"{TRADEMUX_BASE_URL}/v1/positions",
                headers=headers
            )
            positions = positions_resp.json() if positions_resp.status_code == 200 else {}

            # 获取品种列表
            instruments_resp = await client.get(
                f"{TRADEMUX_BASE_URL}/v1/instruments",
                headers=headers
            )
            instruments = instruments_resp.json() if instruments_resp.status_code == 200 else {}

            # 获取主要货币对价格
            symbols = ["EURUSD", "GBPUSD", "USDJPY", "XAUUSD", "BTCUSD"]
            prices = {}
            for sym in symbols:
                try:
                    price_resp = await client.post(
                        f"{TRADEMUX_BASE_URL}/v1/data",
                        headers=headers,
                        json={"symbol": sym}
                    )
                    if price_resp.status_code == 200:
                        prices[sym] = price_resp.json()
                except:
                    pass

        return {
            "account": {
                "balance": account.get("balance"),
                "equity": account.get("equity"),
                "account_number": account.get("account_number"),
                "server": account.get("server"),
                "open_positions": account.get("open_positions"),
                "floating_pnl": account.get("floating_pnl")
            },
            "positions": positions.get("positions", []),
            "positions_count": positions.get("total_count", 0),
            "instruments": instruments.get("instruments", []),
            "prices": prices,
            "status": "ok"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
