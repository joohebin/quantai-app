"""
AI 交易路由 - DeepSeek 直连 + 自动交易
支持: DeepSeek V3
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import os
import httpx
import asyncio
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/api/ai", tags=["AI Trading"])

# ============ Groq API 配置（免费模型 - 客服对话）============
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Groq 免费模型
GROQ_MODELS = {
    "customer": "llama-3.3-70b-versatile",      # 客服对话（免费，推荐）
    "fast": "llama-3.1-8b-instant",              # 快速响应（免费）
    "vision": "llama-3.2-11b-vision-preview",   # 视觉理解（免费）
}

# ============ DeepSeek API 配置（直接调用）============
DEEPSEEK_API_KEY = "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"
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

# DeepSeek 模型配置
DEEPSEEK_MODELS = {
    "stable": "deepseek-chat",      # DeepSeek V3（主力）
    "coder": "deepseek-coder",     # 代码专用
}

# 当前活跃模型
current_model = {"id": "deepseek-chat", "name": "DeepSeek V3"}

# ============ 自动交易配置 ============
AUTO_TRADE_ENABLED = os.getenv("AUTO_TRADE_ENABLED", "false").lower() == "true"
TRADE_EXCHANGE = os.getenv("TRADE_EXCHANGE", "mt5")  # mt5, binance, okx

# 交易信号存储（供前端显示）
latest_signal = {
    "symbol": None,
    "direction": None,  # buy / sell
    "entry": None,
    "stop_loss": None,
    "take_profit": None,
    "confidence": None,
    "model": None,
    "timestamp": None
}


# ============ 请求/响应模型 ============
class ChatRequest(BaseModel):
    message: str
    symbol: Optional[str] = None
    auto_trade: Optional[bool] = False  # 是否启用自动交易


class AutoTradeRequest(BaseModel):
    symbol: str
    signal: str  # buy / sell / hold
    confidence: float  # 0-100
    entry_price: Optional[float] = None
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None


class SignalResponse(BaseModel):
    symbol: str
    direction: str
    entry: float
    stop_loss: float
    take_profit: float
    confidence: float
    model: str
    timestamp: str
    auto_executed: bool = False


# ============ Groq API 调用（客服对话 - 免费模型）============
async def call_groq(model: str, messages: list, max_tokens: int = 1000) -> dict:
    """调用Groq API（免费模型）"""
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": 0.5
    }
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        r = await client.post(GROQ_API_URL, headers=headers, json=payload)
        
        if r.status_code != 200:
            raise Exception(f"Groq API Error: {r.status_code} - {r.text}")
        
        return r.json()


# ============ DeepSeek API 调用（自动交易）============
async def call_deepseek(model: str, messages: list, max_tokens: int = 1000) -> dict:
    """调用DeepSeek API"""
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": 0.5
    }
    
    async with httpx.AsyncClient(timeout=90.0) as client:
        r = await client.post(DEEPSEEK_API_URL, headers=headers, json=payload)
        
        if r.status_code != 200:
            raise Exception(f"DeepSeek API Error: {r.status_code} - {r.text}")
        
        return r.json()


# ============ 自动交易执行 ============
async def execute_auto_trade(signal: dict) -> bool:
    """执行自动交易（模拟/真实）"""
    global latest_signal
    
    if not AUTO_TRADE_ENABLED:
        return False
    
    symbol = signal.get("symbol", "BTC")
    direction = signal.get("direction", "hold")
    entry = signal.get("entry", 0)
    stop_loss = signal.get("stop_loss", 0)
    take_profit = signal.get("take_profit", 0)
    
    # 更新最新信号
    latest_signal.update({
        "symbol": symbol,
        "direction": direction,
        "entry": entry,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "confidence": signal.get("confidence", 0),
        "model": current_model["name"],
        "timestamp": datetime.now().isoformat()
    })
    
    # TODO: 实现真实交易执行
    # 根据 TRADE_EXCHANGE 调用不同的API:
    # - mt5: 调用 MT5 Python API (mt5api)
    # - binance: 调用 Binance API
    # - okx: 调用 OKX API
    
    print(f"[自动交易] 信号: {symbol} {direction} @ {entry}")
    print(f"[自动交易] 止损: {stop_loss} | 止盈: {take_profit}")
    
    return True


# ============ 路由端点 ============
@router.get("/health")
async def health():
    """AI健康检查"""
    return {
        "status": "ok",
        "providers": {
            "customer_service": {"provider": "Groq", "model": GROQ_MODELS["customer"], "cost": "免费"},
            "auto_trading": {"provider": "DeepSeek", "model": DEEPSEEK_MODELS["stable"], "cost": "付费"}
        },
        "auto_trade": AUTO_TRADE_ENABLED
    }


@router.get("/models")
async def list_models():
    """可用模型列表"""
    return {
        "customer_service": {
            "provider": "Groq",
            "models": [
                {"id": GROQ_MODELS["customer"], "name": "Llama 3.3 70B", "use_case": "客服对话", "cost": "免费"},
                {"id": GROQ_MODELS["fast"], "name": "Llama 3.1 8B", "use_case": "快速响应", "cost": "免费"}
            ]
        },
        "auto_trading": {
            "provider": "DeepSeek",
            "models": [
                {"id": DEEPSEEK_MODELS["stable"], "name": "DeepSeek V3", "use_case": "稳定分析"}
            ]
        }
    }


@router.post("/chat")
async def chat(request: ChatRequest):
    """AI对话 + 自动交易信号生成（客服用Groq免费模型）"""
    symbol = request.symbol or detect_symbol(request.message)
    
    # 客服对话统一使用Groq免费模型
    model = GROQ_MODELS["customer"]
    
    current_model["id"] = model
    
    # 构建提示词
    system_prompt = f"""你是专业的量化交易AI助手。用中文简洁回答。

分析格式（用于交易信号）：
📊 【{symbol} 交易分析】
🎯 趋势：[上涨/下跌/震荡]
💰 关键位：阻力 XXXXX | 支撑 XXXXX
⚡ 操作建议：[做多/做空/观望]
🛡️ 止损：XXXXX
🎯 止盈：XXXXX
📈 盈亏比：X:1
🎯 置信度：XX%

如果启用自动交易，请生成完整交易信号。"""
    
    try:
        response = await call_groq(model, [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": request.message}
        ])
        
        message = response["choices"][0]["message"]["content"]
        
        # 解析信号
        signal = parse_trade_signal(message, symbol)
        
        # 自动交易
        auto_executed = False
        if request.auto_trade and signal and signal.get("direction") != "hold":
            auto_executed = await execute_auto_trade(signal)
        
        return {
            "success": True,
            "message": message,
            "symbol": symbol,
            "signal": signal,
            "model": model.split("/")[-1],
            "auto_executed": auto_executed,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"AI服务异常: {str(e)}",
            "model": model
        }


@router.post("/analyze")
async def analyze(symbol: str, timeframe: str = "1h"):
    """市场分析 + 生成交易信号（自动交易用DeepSeek）"""
    model = DEEPSEEK_MODELS["stable"]  # 使用DeepSeek进行市场分析
    current_model["id"] = model
    
    prompt = f"""分析 {symbol} 在 {timeframe} 时间框架的技术面和基本面：

请输出：
1. 趋势判断（上涨/下跌/震荡）
2. 关键支撑位和阻力位
3. 技术指标信号（MACD, RSI, MA）
4. 交易信号：做多/做空/观望
5. 具体入场点位、止损位、止盈位
6. 置信度评分（0-100%）

如果信号为做多或做空，必须包含具体数字。"""
    
    try:
        response = await call_deepseek(model, [
            {"role": "system", "content": "你是一名专业的量化交易分析师，擅长技术分析和风险管理。"},
            {"role": "user", "content": prompt}
        ])
        
        message = response["choices"][0]["message"]["content"]
        signal = parse_trade_signal(message, symbol)
        
        return {
            "success": True,
            "symbol": symbol,
            "timeframe": timeframe,
            "analysis": message,
            "signal": signal,
            "model": model.split("/")[-1],
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/signal")
async def generate_signal(request: AutoTradeRequest):
    """生成交易信号并可选执行"""
    signal = {
        "symbol": request.symbol,
        "direction": request.signal,
        "confidence": request.confidence,
        "entry": request.entry_price,
        "stop_loss": request.stop_loss,
        "take_profit": request.take_profit
    }
    
    auto_executed = False
    if request.signal in ["buy", "sell"] and request.confidence >= 70:
        auto_executed = await execute_auto_trade(signal)
    
    return SignalResponse(
        symbol=request.symbol,
        direction=request.signal,
        entry=request.entry_price or 0,
        stop_loss=request.stop_loss or 0,
        take_profit=request.take_profit or 0,
        confidence=request.confidence,
        model=current_model["name"],
        timestamp=datetime.now().isoformat(),
        auto_executed=auto_executed
    )


@router.get("/latest-signal")
async def get_latest_signal():
    """获取最新交易信号"""
    return latest_signal


@router.post("/auto-trade/enable")
async def enable_auto_trade(enable: bool = True):
    """启用/禁用自动交易"""
    global AUTO_TRADE_ENABLED
    AUTO_TRADE_ENABLED = enable
    return {"auto_trade": AUTO_TRADE_ENABLED, "message": "自动交易已启用" if enable else "已禁用"}


# ============ 辅助函数 ============
def detect_symbol(msg: str) -> str:
    """检测消息中的交易品种"""
    msg_lower = msg.lower()
    symbols = {
        "BTC": ["btc", "比特币", "bitcoin"],
        "ETH": ["eth", "以太坊", "ethereum"],
        "XAU": ["黄金", "gold", "xau", "伦敦金"],
        "EUR": ["欧元", "eur", "欧美"],
        "WTI": ["原油", "oil", "wti", "美原油"],
        "SPX": ["标普", "spx", "sp500", "纳斯达克"]
    }
    
    for symbol, keywords in symbols.items():
        if any(k in msg_lower for k in keywords):
            return symbol
    return "BTC"  # 默认BTC


def parse_trade_signal(message: str, symbol: str) -> dict:
    """从AI响应中解析交易信号"""
    import re
    
    signal = {
        "symbol": symbol,
        "direction": "hold",
        "entry": None,
        "stop_loss": None,
        "take_profit": None,
        "confidence": 50
    }
    
    msg_upper = message.upper()
    msg_lower = message.lower()
    
    # 检测方向
    if any(k in msg_lower for k in ["做多", "买入", "long", "buy", "多头", "上涨"]):
        signal["direction"] = "buy"
    elif any(k in msg_lower for k in ["做空", "卖出", "short", "sell", "空头", "下跌"]):
        signal["direction"] = "sell"
    
    # 提取数字
    numbers = re.findall(r'[\d,]+\.?\d*', message)
    prices = [float(n.replace(',', '')) for n in numbers if float(n.replace(',', '')) > 100]
    
    if prices:
        # 假设第一个高价是入场价
        signal["entry"] = prices[0] if prices else None
        
        # 找止损止盈
        for p in prices:
            if p < signal["entry"] and signal["stop_loss"] is None:
                signal["stop_loss"] = p
            elif p > signal["entry"] and signal["take_profit"] is None:
                signal["take_profit"] = p
    
    # 提取置信度
    conf_match = re.search(r'置信[度率][：:]?\s*(\d+)%?', message)
    if conf_match:
        signal["confidence"] = int(conf_match.group(1))
    
    return signal
