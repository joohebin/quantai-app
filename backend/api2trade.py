"""
API2Trade MT4/MT5 交易接口
无EA、无终端的直连方案
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, List
from datetime import datetime
import httpx
import os
import asyncio

router = APIRouter(prefix="/api/api2trade", tags=["API2Trade"])

# ============ 配置 ============
API2TRADE_CONFIG = {
    "api_key": None,  # 待配置
    "base_url": "https://api.metatraderapi.dev",
    "connected": False,
    "accounts": {},  # {account_id: {server, login, name}}
}

# 账户映射 - 用于QuantAI多券商管理
# 格式: {"metaquotes_demo": "uuid-from-api2trade"}
ACCOUNT_MAPPING = {}

# ============ 请求模型 ============
class AccountAddRequest(BaseModel):
    server: str       # 如 "MetaQuotes-Demo"
    login: str        # MT4/MT5 账号
    password: str     # MT4/MT5 密码
    name: Optional[str] = None  # 账户别名，如 "MetaQuotes Demo"

class TradeRequest(BaseModel):
    account_id: str           # API2Trade 分配的 account_id
    symbol: str               # 如 "EURUSD"
    side: str                 # "buy" 或 "sell"
    lots: float               # 手数
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    comment: Optional[str] = "QuantAI Auto Trade"

class ModifyOrderRequest(BaseModel):
    account_id: str
    order_id: int
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None

class ClosePositionRequest(BaseModel):
    account_id: str
    order_id: int
    lots: Optional[float] = None  # 平仓手数，默认全部


# ============ API2Trade 客户端 ============
class API2TradeClient:
    def __init__(self, api_key: str, base_url: str = "https://api.metatraderapi.dev"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json"
        }
    
    async def _request(self, method: str, endpoint: str, data: dict = None) -> dict:
        """发送HTTP请求"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            url = f"{self.base_url}{endpoint}"
            
            if method == "GET":
                response = await client.get(url, headers=self.headers)
            elif method == "POST":
                response = await client.post(url, headers=self.headers, json=data)
            elif method == "PUT":
                response = await client.put(url, headers=self.headers, json=data)
            elif method == "DELETE":
                response = await client.delete(url, headers=self.headers)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "error": True,
                    "status_code": response.status_code,
                    "message": response.text
                }
    
    # ============ 账户管理 ============
    async def get_accounts(self) -> dict:
        """获取所有已连接账户"""
        return await self._request("GET", "/accounts")
    
    async def add_account(self, server: str, login: str, password: str) -> dict:
        """添加交易账户"""
        return await self._request("POST", "/accounts", {
            "server": server,
            "login": login,
            "password": password
        })
    
    async def get_account_summary(self, account_id: str) -> dict:
        """获取账户摘要"""
        return await self._request("GET", f"/accounts/{account_id}/summary")
    
    async def get_account_positions(self, account_id: str) -> dict:
        """获取持仓"""
        return await self._request("GET", f"/accounts/{account_id}/positions")
    
    async def get_account_orders(self, account_id: str) -> dict:
        """获取挂单"""
        return await self._request("GET", f"/accounts/{account_id}/orders")
    
    # ============ 交易执行 ============
    async def place_order(self, account_id: str, symbol: str, side: str, 
                          lots: float, stop_loss: float = None,
                          take_profit: float = None, comment: str = None) -> dict:
        """下单（市价单）"""
        data = {
            "symbol": symbol,
            "side": side.upper(),  # BUY or SELL
            "volume": lots,
            "type": "MARKET"
        }
        
        if stop_loss:
            data["stop_loss"] = stop_loss
        if take_profit:
            data["take_profit"] = take_profit
        if comment:
            data["comment"] = comment
        
        return await self._request("POST", f"/accounts/{account_id}/orders", data)
    
    async def place_pending_order(self, account_id: str, symbol: str, side: str,
                                   lots: float, price: float, order_type: str,
                                   stop_loss: float = None, take_profit: float = None,
                                   comment: str = None) -> dict:
        """下单（挂单：限价/止损）"""
        data = {
            "symbol": symbol,
            "side": side.upper(),
            "volume": lots,
            "price": price,
            "type": order_type.upper(),  # LIMIT, STOP, BUY_STOP, SELL_STOP, etc.
        }
        
        if stop_loss:
            data["stop_loss"] = stop_loss
        if take_profit:
            data["take_profit"] = take_profit
        if comment:
            data["comment"] = comment
        
        return await self._request("POST", f"/accounts/{account_id}/orders", data)
    
    async def close_position(self, account_id: str, order_id: int, 
                            lots: float = None) -> dict:
        """平仓"""
        data = {"order_id": order_id}
        if lots:
            data["volume"] = lots
        
        return await self._request("POST", f"/accounts/{account_id}/positions/close", data)
    
    async def modify_order(self, account_id: str, order_id: int,
                          stop_loss: float = None, take_profit: float = None,
                          price: float = None) -> dict:
        """修改订单/持仓"""
        data = {"order_id": order_id}
        if stop_loss is not None:
            data["stop_loss"] = stop_loss
        if take_profit is not None:
            data["take_profit"] = take_profit
        if price is not None:
            data["price"] = price
        
        return await self._request("PUT", f"/accounts/{account_id}/orders/{order_id}", data)
    
    async def cancel_order(self, account_id: str, order_id: int) -> dict:
        """取消挂单"""
        return await self._request("DELETE", f"/accounts/{account_id}/orders/{order_id}")
    
    # ============ 市场数据 ============
    async def get_symbols(self, account_id: str) -> dict:
        """获取交易品种列表"""
        return await self._request("GET", f"/accounts/{account_id}/symbols")
    
    async def get_quote(self, account_id: str, symbol: str) -> dict:
        """获取实时报价"""
        return await self._request("GET", f"/accounts/{account_id}/quotes/{symbol}")
    
    async def get_candles(self, account_id: str, symbol: str, 
                          timeframe: str = "H1", count: int = 100) -> dict:
        """获取K线数据"""
        return await self._request("GET", 
            f"/accounts/{account_id}/candles/{symbol}?timeframe={timeframe}&count={count}")


# ============ 全局客户端实例 ============
_client: Optional[API2TradeClient] = None

def get_client() -> Optional[API2TradeClient]:
    """获取API2Trade客户端"""
    global _client
    if _client and API2TRADE_CONFIG["api_key"]:
        return _client
    return None

def init_client(api_key: str):
    """初始化API2Trade客户端"""
    global _client
    if api_key:
        _client = API2TradeClient(api_key)
        API2TRADE_CONFIG["api_key"] = api_key
        API2TRADE_CONFIG["connected"] = True
        return True
    return False


# ============ API 端点 ============
@router.get("/status")
async def get_status():
    """获取API2Trade连接状态"""
    return {
        "connected": API2TRADE_CONFIG["connected"],
        "api_key_configured": bool(API2TRADE_CONFIG["api_key"]),
        "accounts_count": len(API2TRADE_CONFIG["accounts"]),
        "accounts": API2TRADE_CONFIG["accounts"]
    }


@router.post("/connect")
async def connect(api_key: str):
    """连接API2Trade"""
    global _client
    
    if not api_key:
        raise HTTPException(status_code=400, detail="API Key不能为空")
    
    # 测试连接
    _client = API2TradeClient(api_key)
    result = await _client.get_accounts()
    
    if result.get("error"):
        return {
            "success": False,
            "error": result.get("message", "连接失败")
        }
    
    # 保存配置
    API2TRADE_CONFIG["api_key"] = api_key
    API2TRADE_CONFIG["connected"] = True
    
    return {
        "success": True,
        "message": "API2Trade连接成功",
        "accounts": result
    }


@router.post("/accounts")
async def add_account(request: AccountAddRequest):
    """添加交易账户"""
    client = get_client()
    if not client:
        raise HTTPException(status_code=400, detail="请先调用 /api/api2trade/connect 配置API Key")
    
    result = await client.add_account(
        server=request.server,
        login=request.login,
        password=request.password
    )
    
    if result.get("error"):
        return {
            "success": False,
            "error": result.get("message", "添加账户失败")
        }
    
    # 保存账户信息
    account_id = result.get("id", result.get("account_id"))
    API2TRADE_CONFIG["accounts"][account_id] = {
        "server": request.server,
        "login": request.login,
        "name": request.name or f"{request.server} - {request.login}"
    }
    
    return {
        "success": True,
        "account_id": account_id,
        "message": f"账户 {request.name or request.login} 添加成功"
    }


@router.get("/accounts")
async def list_accounts():
    """获取所有账户"""
    client = get_client()
    if not client:
        raise HTTPException(status_code=400, detail="请先调用 /api/api2trade/connect")
    
    result = await client.get_accounts()
    return result


@router.get("/accounts/{account_id}/summary")
async def get_account_summary(account_id: str):
    """获取账户摘要"""
    client = get_client()
    if not client:
        raise HTTPException(status_code=400, detail="请先调用 /api/api2trade/connect")
    
    result = await client.get_account_summary(account_id)
    return result


@router.get("/accounts/{account_id}/positions")
async def get_positions(account_id: str):
    """获取持仓"""
    client = get_client()
    if not client:
        raise HTTPException(status_code=400, detail="请先调用 /api/api2trade/connect")
    
    result = await client.get_account_positions(account_id)
    return result


@router.post("/trade")
async def trade(request: TradeRequest):
    """执行交易"""
    client = get_client()
    if not client:
        raise HTTPException(status_code=400, detail="请先调用 /api/api2trade/connect")
    
    result = await client.place_order(
        account_id=request.account_id,
        symbol=request.symbol,
        side=request.side,
        lots=request.lots,
        stop_loss=request.stop_loss,
        take_profit=request.take_profit,
        comment=request.comment
    )
    
    if result.get("error"):
        return {
            "success": False,
            "error": result.get("message", "交易失败")
        }
    
    return {
        "success": True,
        "order_id": result.get("order_id", result.get("id")),
        "symbol": request.symbol,
        "side": request.side,
        "lots": request.lots,
        "exchange": "API2Trade",
        "result": result
    }


@router.post("/trade/pending")
async def trade_pending(account_id: str, symbol: str, side: str, lots: float,
                        price: float, order_type: str = "LIMIT",
                        stop_loss: float = None, take_profit: float = None,
                        comment: str = "QuantAI"):
    """执行挂单"""
    client = get_client()
    if not client:
        raise HTTPException(status_code=400, detail="请先调用 /api/api2trade/connect")
    
    result = await client.place_pending_order(
        account_id=account_id,
        symbol=symbol,
        side=side,
        lots=lots,
        price=price,
        order_type=order_type,
        stop_loss=stop_loss,
        take_profit=take_profit,
        comment=comment
    )
    
    if result.get("error"):
        return {
            "success": False,
            "error": result.get("message", "挂单失败")
        }
    
    return {
        "success": True,
        "order_id": result.get("order_id", result.get("id")),
        "symbol": symbol,
        "type": order_type,
        "result": result
    }


@router.post("/close")
async def close_position(request: ClosePositionRequest):
    """平仓"""
    client = get_client()
    if not client:
        raise HTTPException(status_code=400, detail="请先调用 /api/api2trade/connect")
    
    result = await client.close_position(
        account_id=request.account_id,
        order_id=request.order_id,
        lots=request.lots
    )
    
    if result.get("error"):
        return {
            "success": False,
            "error": result.get("message", "平仓失败")
        }
    
    return {
        "success": True,
        "message": f"订单 {request.order_id} 平仓成功",
        "result": result
    }


@router.put("/modify")
async def modify_order(request: ModifyOrderRequest):
    """修改订单（止损/止盈）"""
    client = get_client()
    if not client:
        raise HTTPException(status_code=400, detail="请先调用 /api/api2trade/connect")
    
    result = await client.modify_order(
        account_id=request.account_id,
        order_id=request.order_id,
        stop_loss=request.stop_loss,
        take_profit=request.take_profit
    )
    
    if result.get("error"):
        return {
            "success": False,
            "error": result.get("message", "修改失败")
        }
    
    return {
        "success": True,
        "message": f"订单 {request.order_id} 修改成功",
        "result": result
    }


@router.delete("/orders/{account_id}/{order_id}")
async def cancel_order(account_id: str, order_id: int):
    """取消挂单"""
    client = get_client()
    if not client:
        raise HTTPException(status_code=400, detail="请先调用 /api/api2trade/connect")
    
    result = await client.cancel_order(account_id, order_id)
    
    if result.get("error"):
        return {
            "success": False,
            "error": result.get("message", "取消失败")
        }
    
    return {
        "success": True,
        "message": f"挂单 {order_id} 已取消"
    }


@router.get("/quotes/{account_id}/{symbol}")
async def get_quote(account_id: str, symbol: str):
    """获取实时报价"""
    client = get_client()
    if not client:
        raise HTTPException(status_code=400, detail="请先调用 /api/api2trade/connect")
    
    result = await client.get_quote(account_id, symbol)
    return result


@router.get("/candles/{account_id}/{symbol}")
async def get_candles(account_id: str, symbol: str, 
                      timeframe: str = "H1", count: int = 100):
    """获取K线数据"""
    client = get_client()
    if not client:
        raise HTTPException(status_code=400, detail="请先调用 /api/api2trade/connect")
    
    result = await client.get_candles(account_id, symbol, timeframe, count)
    return result
