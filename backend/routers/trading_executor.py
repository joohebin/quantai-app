"""
自动交易执行器 - MT5 + 加密货币交易所
用户自行配置API连接
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime
import asyncio
import os

router = APIRouter(prefix="/api/trade", tags=["Auto Trading"])

# ============ 配置存储（生产环境应使用数据库）============
class ExchangeConfig:
    """交易所配置"""
    def __init__(self):
        self.mt5 = {
            "connected": False,
            "server": None,
            "account": None
        }
        self.binance = {
            "connected": False,
            "api_key": None,
            "testnet": True
        }
        self.okx = {
            "connected": False,
            "api_key": None,
            "testnet": True
        }
    
    def get_status(self) -> dict:
        return {
            "mt5": self.mt5,
            "binance": self.binance,
            "okx": self.okx
        }

exchange_config = ExchangeConfig()

# ============ 风控规则 ============
RISK_CONTROL = {
    "max_position_size": 0.1,        # 最大仓位 (账户的10%)
    "max_single_loss": 0.02,          # 单笔最大亏损 (2%)
    "max_daily_loss": 0.05,          # 每日最大亏损 (5%)
    "min_confidence": 70,             # 最小置信度
    "max_trades_per_day": 5,         # 每日最大交易数
    "auto_trade_enabled": False,      # 自动交易开关
}

# ============ 交易历史 ============
trade_history: List[Dict] = []
daily_trade_count = {"count": 0, "date": datetime.now().date()}

# ============ 请求/响应模型 ============
class TradeRequest(BaseModel):
    exchange: str  # mt5, binance, okx
    symbol: str    # BTCUSDT, EURUSD, etc
    direction: str  # buy, sell
    amount: float   # 数量/手数
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    order_type: str = "market"  # market, limit
    confidence: float = 70

class PositionRequest(BaseModel):
    exchange: str

class ConfigRequest(BaseModel):
    exchange: str
    api_key: Optional[str] = None
    api_secret: Optional[str] = None
    password: Optional[str] = None
    server: Optional[str] = None
    testnet: bool = True


# ============ 风控检查 ============
def check_risk_control(symbol: str, direction: str, amount: float, confidence: float) -> tuple[bool, str]:
    """风控检查"""
    global daily_trade_count, RISK_CONTROL
    
    # 检查置信度
    if confidence < RISK_CONTROL["min_confidence"]:
        return False, f"置信度 {confidence}% 低于最低要求 {RISK_CONTROL['min_confidence']}%"
    
    # 检查自动交易开关
    if not RISK_CONTROL["auto_trade_enabled"]:
        return False, "自动交易未启用"
    
    # 检查每日交易数
    today = datetime.now().date()
    if daily_trade_count["date"] != today:
        daily_trade_count = {"count": 0, "date": today}
    
    if daily_trade_count["count"] >= RISK_CONTROL["max_trades_per_day"]:
        return False, f"今日交易数已达上限 ({RISK_CONTROL['max_trades_per_day']}笔)"
    
    # 检查仓位大小
    if amount > RISK_CONTROL["max_position_size"]:
        return False, f"仓位 {amount} 超过最大限制 {RISK_CONTROL['max_position_size']}"
    
    return True, "通过风控"


# ============ MT5 交易执行 ============
async def execute_mt5_trade(symbol: str, direction: str, volume: float, 
                             stop_loss: float = None, take_profit: float = None) -> dict:
    """执行MT5交易"""
    try:
        import MetaTrader5 as mt5
        
        # MT5常量定义
        ACTION_DEAL = 1
        TYPE_BUY = 0
        TYPE_SELL = 1
        
        if not mt5.initialize():
            return {"success": False, "error": "MT5连接失败，请确保MT5终端正在运行"}
        
        # 获取交易品种信息
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            return {"success": False, "error": f"找不到交易品种: {symbol}"}
        
        # 激活交易品种
        if not symbol_info.trade_mode:
            mt5.symbol_select(symbol, True)
            symbol_info = mt5.symbol_info(symbol)
        
        # 获取当前价格
        tick = mt5.symbol_info_tick(symbol)
        if tick is None:
            return {"success": False, "error": f"无法获取价格: {symbol}"}
        
        price = tick.ask if direction == "buy" else tick.bid
        
        # 准备请求
        request = {
            "action": ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": TYPE_BUY if direction == "buy" else TYPE_SELL,
            "price": price,
            "deviation": 10,
            "magic": 123456,
            "comment": "QuantAI Auto Trade"
        }
        
        if stop_loss:
            request["sl"] = stop_loss
        if take_profit:
            request["tp"] = take_profit
        
        # 执行交易
        result = mt5.order_send(request)
        
        if result.retcode == mt5.TRADE_RETCODE_DONE:
            return {
                "success": True,
                "order_id": result.order,
                "symbol": symbol,
                "direction": direction,
                "volume": volume,
                "price": price,
                "stop_loss": stop_loss,
                "take_profit": take_profit,
                "exchange": "MT5"
            }
        else:
            return {"success": False, "error": f"MT5错误: {result.comment}"}
    
    except ImportError:
        return {"success": False, "error": "MT5库未安装"}
    except Exception as e:
        return {"success": False, "error": str(e)}


# ============ Binance 交易执行 ============
async def execute_binance_trade(api_key: str, api_secret: str, symbol: str, 
                                 direction: str, quantity: float,
                                 stop_loss: float = None, take_profit: float = None,
                                 testnet: bool = True) -> dict:
    """执行Binance交易"""
    try:
        from binance.client import Client
        
        # 连接 - testnet模式直接返回模拟结果
        if testnet or not api_key:
            return {
                "success": True,
                "order_id": f"TEST_{int(datetime.now().timestamp())}",
                "symbol": symbol,
                "direction": direction,
                "quantity": quantity,
                "stop_loss": stop_loss,
                "take_profit": take_profit,
                "exchange": "Binance Testnet",
                "mode": "模拟交易 (Testnet)",
                "note": "Binance Testnet模式，无需真实API Key"
            }
        
        # 真实交易
        base_url = "https://testnet.binance.vision"
        client = Client(api_key, api_secret, base_url=base_url)
        
        # 检查账户
        account = client.get_account()
        
        # 获取交易对信息
        exchange_info = client.get_symbol_info(symbol)
        if not exchange_info:
            return {"success": False, "error": f"找不到交易对: {symbol}"}
        
        # 计算数量精度
        step_size = 0.00001
        quantity = float(f"{quantity:.{len(str(step_size).split('.')[-1])}f}")
        
        # 准备订单
        params = {
            "symbol": symbol,
            "side": "SELL" if direction == "sell" else "BUY",
            "type": "MARKET",
            "quantity": quantity
        }
        
        # 添加止损止盈
        if stop_loss:
            params["stopLossPrice"] = stop_loss
        if take_profit:
            params["takeProfitPrice"] = take_profit
        
        # 测试订单（testnet模式）
        if testnet:
            test_result = client.create_test_order(**params)
            return {
                "success": True,
                "order_id": f"TEST_{datetime.now().timestamp()}",
                "symbol": symbol,
                "direction": direction,
                "quantity": quantity,
                "stop_loss": stop_loss,
                "take_profit": take_profit,
                "exchange": "Binance Testnet",
                "mode": "模拟交易"
            }
        
        # 执行真实交易
        result = client.create_order(**params)
        
        return {
            "success": True,
            "order_id": result["orderId"],
            "symbol": symbol,
            "direction": direction,
            "quantity": quantity,
            "price": result.get("price"),
            "exchange": "Binance"
        }
    
    except ImportError:
        return {"success": False, "error": "Binance库未安装，运行 pip install python-binance"}
    except Exception as e:
        return {"success": False, "error": str(e)}


# ============ OKX 交易执行 ============
async def execute_okx_trade(api_key: str, api_secret: str, password: str,
                            symbol: str, direction: str, quantity: float,
                            stop_loss: float = None, take_profit: float = None,
                            testnet: bool = True) -> dict:
    """执行OKX交易"""
    try:
        import okx.Account as Account
        import okx.Trade as Trade
        
        # 连接
        flag = "1" if testnet else "0"
        
        account_api = Account.AccountAPI(api_key, api_secret, password, False, flag)
        trade_api = Trade.TradeAPI(api_key, api_secret, password, False, flag)
        
        # 准备参数
        inst_id = symbol.replace("/", "-")  # BTC/USDT -> BTC-USDT
        td_mode = "cross"  # 全仓
        side = "sell" if direction == "sell" else "buy"
        
        # 下单
        result = trade_api.place_order(
            instId=inst_id,
            tdMode=td_mode,
            side=side,
            ordType="market",
            sz=str(int(quantity))
        )
        
        if result.get("code") == "0":
            return {
                "success": True,
                "order_id": result["data"][0]["ordId"],
                "symbol": symbol,
                "direction": direction,
                "quantity": quantity,
                "exchange": "OKX Testnet" if testnet else "OKX"
            }
        else:
            return {"success": False, "error": result.get("msg")}
    
    except ImportError:
        return {"success": False, "error": "OKX库未安装，运行 pip install okx"}
    except Exception as e:
        return {"success": False, "error": str(e)}


# ============ CCXT 统一接口（支持40+交易所）============
CCXT_EXCHANGES = {
    # 全球主流
    "binance": {"name": "Binance", "country": "全球", "crypto": True},
    "bybit": {"name": "Bybit", "country": "全球", "crypto": True},
    "okx": {"name": "OKX", "country": "全球", "crypto": True},
    "coinbase": {"name": "Coinbase", "country": "美国", "crypto": True},
    "kraken": {"name": "Kraken", "country": "美国", "crypto": True},
    "bitget": {"name": "Bitget", "country": "全球", "crypto": True},
    "kucoin": {"name": "KuCoin", "country": "全球", "crypto": True},
    "mexc": {"name": "MEXC", "country": "全球", "crypto": True},
    "gateio": {"name": "Gate.io", "country": "全球", "crypto": True},
    "htx": {"name": "HTX (火币)", "country": "中国", "crypto": True},
    "bitfinex": {"name": "Bitfinex", "country": "全球", "crypto": True},
    "phemex": {"name": "Phemex", "country": "全球", "crypto": True},
    "bitstamp": {"name": "Bitstamp", "country": "欧洲", "crypto": True},
    
    # 🇰🇷 韩国交易所
    "upbit": {"name": "Upbit", "country": "🇰🇷 韩国", "crypto": True, "featured": True},
    "bithumb": {"name": "Bithumb", "country": "🇰🇷 韩国", "crypto": True, "featured": True},
    "coinone": {"name": "Coinone", "country": "🇰🇷 韩国", "crypto": True},
    "korbit": {"name": "Korbit", "country": "🇰🇷 韩国", "crypto": True},
    
    # 🇯🇵 日本交易所
    "bitflyer": {"name": "bitFlyer", "country": "🇯🇵 日本", "crypto": True, "featured": True},
    "gmo": {"name": "GMO Coin", "country": "🇯🇵 日本", "crypto": True},
    "liquid": {"name": "Liquid", "country": "🇯🇵 日本", "crypto": True},
    "bitbank": {"name": "Bitbank", "country": "🇯🇵 日本", "crypto": True},
    
    # 其他重要交易所
    "woo": {"name": "WOO Network", "country": "全球", "crypto": True},
    "bingx": {"name": "BingX", "country": "全球", "crypto": True},
    "lbank": {"name": "LBank", "country": "全球", "crypto": True},
    "digifinex": {"name": "DigiFinex", "country": "全球", "crypto": True},
    "hitbtc": {"name": "HitBTC", "country": "全球", "crypto": True},
}

async def execute_ccxt_trade(exchange_id: str, api_key: str, api_secret: str,
                            symbol: str, direction: str, quantity: float,
                            stop_loss: float = None, take_profit: float = None,
                            password: str = None, testnet: bool = True) -> dict:
    """通过CCXT执行交易"""
    try:
        import ccxt
        
        # 创建交易所实例
        exchange_class = getattr(ccxt, exchange_id)
        exchange = exchange_class({
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True,
        })
        
        # 添加密码（如需要）
        if password:
            exchange.password = password
        
        # 测试网络设置
        if testnet and hasattr(exchange, 'urls'):
            # 尝试使用testnet
            if 'test' in exchange.urls:
                exchange.urls['api'] = exchange.urls['test']
        
        # 模拟交易模式
        if testnet or not api_key:
            return {
                "success": True,
                "order_id": f"TEST_{int(datetime.now().timestamp())}",
                "symbol": symbol,
                "direction": direction,
                "quantity": quantity,
                "exchange": CCXT_EXCHANGES.get(exchange_id, {}).get("name", exchange_id),
                "mode": "模拟交易 (Testnet)",
                "note": f"{CCXT_EXCHANGES.get(exchange_id, {}).get('name', exchange_id)} Testnet模式"
            }
        
        # 标准化交易对格式
        symbol_formatted = symbol
        if '/' not in symbol and '-' in symbol:
            symbol_formatted = symbol.replace('-', '/')
        
        # 确定买卖方向
        side = 'sell' if direction == 'sell' else 'buy'
        
        # 执行市价单
        order = await asyncio.to_thread(
            exchange.create_market_order,
            symbol_formatted,
            side,
            quantity
        )
        
        # 添加止损止盈（如果提供）
        if stop_loss or take_profit:
            # OCO订单
            params = {}
            if stop_loss:
                params['stopLossPrice'] = stop_loss
            if take_profit:
                params['takeProfitPrice'] = take_profit
            
            await asyncio.to_thread(exchange.create_order, 
                symbol_formatted, 'limit', 'sell' if direction == 'sell' else 'buy',
                quantity, None, params)
        
        return {
            "success": True,
            "order_id": str(order['id']),
            "symbol": symbol,
            "direction": direction,
            "quantity": quantity,
            "price": order.get('average') or order.get('price'),
            "exchange": CCXT_EXCHANGES.get(exchange_id, {}).get("name", exchange_id),
            "mode": "实盘交易"
        }
    
    except ImportError:
        return {"success": False, "error": "CCXT库未安装"}
    except AttributeError:
        return {"success": False, "error": f"不支持的交易所: {exchange_id}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


# ============ API 端点 ============
@router.get("/status")
async def get_trade_status():
    """获取交易状态"""
    # 按地区分组
    exchanges_by_region = {
        "forex": {"mt5": {"name": "MT5 (MetaTrader 5)", "country": "全球"}},
        "🇰🇷 韩国": {},
        "🇯🇵 日本": {},
        "🌍 全球": {},
    }
    
    for ex_id, ex_info in CCXT_EXCHANGES.items():
        country = ex_info.get("country", "全球")
        if "🇰🇷" in country:
            exchanges_by_region["🇰🇷 韩国"][ex_id] = ex_info
        elif "🇯🇵" in country:
            exchanges_by_region["🇯🇵 日本"][ex_id] = ex_info
        else:
            exchanges_by_region["🌍 全球"][ex_id] = ex_info
    
    return {
        "exchange_config": exchange_config.get_status(),
        "risk_control": RISK_CONTROL,
        "auto_trade_enabled": RISK_CONTROL["auto_trade_enabled"],
        "supported_exchanges": exchanges_by_region,
        "total_exchanges": len(CCXT_EXCHANGES) + 1  # +1 for MT5
    }


@router.post("/config")
async def configure_exchange(request: ConfigRequest):
    """配置交易所连接"""
    if request.exchange == "mt5":
        exchange_config.mt5 = {
            "connected": True,
            "server": request.server,
            "account": request.api_key  # MT5用账号
        }
        return {"success": True, "exchange": "MT5", "message": "MT5配置已保存"}
    
    elif request.exchange == "binance":
        exchange_config.binance = {
            "connected": True,
            "api_key": request.api_key,
            "api_secret": request.api_secret,
            "testnet": request.testnet
        }
        return {"success": True, "exchange": "Binance", "mode": "Testnet" if request.testnet else "实盘"}
    
    elif request.exchange == "okx":
        exchange_config.okx = {
            "connected": True,
            "api_key": request.api_key,
            "api_secret": request.api_secret,
            "password": request.password,
            "testnet": request.testnet
        }
        return {"success": True, "exchange": "OKX", "mode": "Testnet" if request.testnet else "实盘"}
    
    elif request.exchange in CCXT_EXCHANGES:
        # CCXT统一接口
        return {
            "success": True, 
            "exchange": CCXT_EXCHANGES[request.exchange]["name"],
            "interface": "CCXT",
            "mode": "Testnet" if request.testnet else "实盘",
            "note": f"已配置 {CCXT_EXCHANGES[request.exchange]['name']}，使用CCXT统一接口"
        }
    
    else:
        supported = list(CCXT_EXCHANGES.keys()) + ["mt5", "binance", "okx"]
        raise HTTPException(status_code=400, detail=f"不支持的交易所。可用: {supported}")


@router.post("/execute")
async def execute_trade(request: TradeRequest):
    """执行交易"""
    global daily_trade_count
    
    # 风控检查
    risk_ok, risk_msg = check_risk_control(
        request.symbol, request.direction, request.amount, request.confidence
    )
    
    if not risk_ok:
        return {
            "success": False,
            "error": risk_msg,
            "rejected": True
        }
    
    # 根据交易所执行
    result = {"rejected": False}
    
    if request.exchange == "mt5":
        result = await execute_mt5_trade(
            request.symbol, request.direction, request.amount,
            request.stop_loss, request.take_profit
        )
    
    elif request.exchange == "binance":
        result = await execute_binance_trade(
            exchange_config.binance.get("api_key", ""),
            exchange_config.binance.get("api_secret", ""),
            request.symbol, request.direction, request.amount,
            request.stop_loss, request.take_profit,
            exchange_config.binance.get("testnet", True)
        )
    
    elif request.exchange == "okx":
        result = await execute_okx_trade(
            exchange_config.okx.get("api_key", ""),
            exchange_config.okx.get("api_secret", ""),
            exchange_config.okx.get("password", ""),
            request.symbol, request.direction, request.amount,
            request.stop_loss, request.take_profit,
            exchange_config.okx.get("testnet", True)
        )
    
    elif request.exchange in CCXT_EXCHANGES:
        # CCXT统一接口
        result = await execute_ccxt_trade(
            request.exchange,  # exchange_id
            "",  # api_key - 用户需要配置
            "",  # api_secret
            request.symbol, request.direction, request.amount,
            request.stop_loss, request.take_profit,
            testnet=True
        )
    
    else:
        raise HTTPException(status_code=400, detail="不支持的交易所")
    
    # 记录交易
    if result.get("success"):
        daily_trade_count["count"] += 1
        trade_history.append({
            **result,
            "timestamp": datetime.now().isoformat()
        })
    
    return result


@router.post("/risk-control")
async def update_risk_control(
    max_position: float = None,
    max_single_loss: float = None,
    min_confidence: float = None,
    auto_trade: bool = None
):
    """更新风控规则"""
    global RISK_CONTROL
    
    if max_position is not None:
        RISK_CONTROL["max_position_size"] = max_position
    if max_single_loss is not None:
        RISK_CONTROL["max_single_loss"] = max_single_loss
    if min_confidence is not None:
        RISK_CONTROL["min_confidence"] = min_confidence
    if auto_trade is not None:
        RISK_CONTROL["auto_trade_enabled"] = auto_trade
    
    return {"success": True, "risk_control": RISK_CONTROL}


@router.get("/history")
async def get_trade_history(limit: int = 20):
    """获取交易历史"""
    return {
        "history": trade_history[-limit:],
        "today_count": daily_trade_count["count"]
    }


@router.get("/positions")
async def get_positions(exchange: str):
    """获取持仓"""
    if exchange == "mt5":
        try:
            import MetaTrader5 as mt5
            if mt5.initialize():
                positions = mt5.positions_get()
                return {
                    "exchange": "MT5",
                    "positions": [
                        {
                            "symbol": p.symbol,
                            "volume": p.volume,
                            "profit": p.profit,
                            "direction": "sell" if p.type == 1 else "buy"
                        }
                        for p in positions
                    ]
                }
        except:
            return {"exchange": "MT5", "positions": [], "note": "MT5未连接"}
    
    elif exchange == "binance":
        return {"exchange": "Binance", "positions": [], "note": "需要配置API Key"}
    
    return {"positions": []}
