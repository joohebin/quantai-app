"""
自动交易模块 - AI 分析市场并建议/执行交易
功能：
- AI 市场分析 + 交易信号生成
- 自动下单（需对接券商API）
- 交易历史记录
- 风险控制
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import os
import httpx
import asyncio
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/api/auto-trade", tags=["Auto Trade"])

# DeepSeek API 配置
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "sk-eb727437f0b64b0b8fbb3b8fb4554cc5")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1"
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

# 自动交易配置
AUTO_TRADE_ENABLED = os.getenv("AUTO_TRADE_ENABLED", "false").lower() == "true"
AUTO_TRADE_MIN_CONFIDENCE = float(os.getenv("AUTO_TRADE_MIN_CONFIDENCE", "70"))
TRADE_EXCHANGE = os.getenv("TRADE_EXCHANGE", "mt5")

# 交易信号存储
latest_signal = {
    "id": None,
    "symbol": None,
    "direction": None,  # buy / sell / hold
    "entry": None,
    "stop_loss": None,
    "take_profit": None,
    "confidence": 0,
    "reason": None,
    "model": None,
    "timestamp": None,
    "executed": False
}

# 交易历史
trade_history: List[dict] = []


# ============ 请求/响应模型 ============
class MarketAnalysisRequest(BaseModel):
    symbol: str
    exchange: Optional[str] = "MT5"
    timeframe: Optional[str] = "1h"  # 1m, 5m, 15m, 1h, 4h, 1d
    indicators: Optional[List[str]] = None  # MA, MACD, RSI, BB, KDJ


class TradeSignalRequest(BaseModel):
    symbol: str
    exchange: Optional[str] = "MT5"
    direction: Optional[str] = None  # buy / sell / hold
    confidence_threshold: Optional[float] = 70.0


class ExecuteTradeRequest(BaseModel):
    symbol: str
    direction: str  # buy / sell
    amount: float
    price: Optional[float] = None
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    comment: Optional[str] = None


class SignalResponse(BaseModel):
    id: str
    symbol: str
    direction: str
    entry: float
    stop_loss: float
    take_profit: float
    confidence: float
    reason: str
    timestamp: str
    executed: bool = False


# ============ 核心功能 ============
async def call_deepseek(messages: List[dict], max_tokens: int = 1200) -> dict:
    """调用 DeepSeek API"""
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": DEEPSEEK_MODEL,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": 0.3  # 较低温度，更稳定的分析
    }

    try:
        async with httpx.AsyncClient(timeout=90.0) as client:
            response = await client.post(DEEPSEEK_API_URL, headers=headers, json=payload)

            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"API Error: {response.status_code}")

    except httpx.TimeoutException:
        raise Exception("AI 响应超时")
    except Exception as e:
        raise Exception(f"AI 服务异常: {str(e)}")


def parse_signal_from_text(text: str, symbol: str) -> dict:
    """从 AI 响应中解析交易信号"""
    import re

    signal = {
        "id": f"{symbol}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "symbol": symbol,
        "direction": "hold",
        "entry": 0,
        "stop_loss": 0,
        "take_profit": 0,
        "confidence": 50,
        "reason": text[:200] + "..." if len(text) > 200 else text,
        "model": DEEPSEEK_MODEL,
        "timestamp": datetime.now().isoformat(),
        "executed": False
    }

    text_lower = text.lower()

    # 检测方向
    if any(k in text_lower for k in ["做多", "买入", "开多", "long", "buy", "多头", "看涨"]):
        signal["direction"] = "buy"
    elif any(k in text_lower for k in ["做空", "卖出", "开空", "short", "sell", "空头", "看跌"]):
        signal["direction"] = "sell"
    else:
        signal["direction"] = "hold"

    # 提取数字（价格、止损止盈）
    numbers = re.findall(r'[\d,]+\.?\d*', text)
    prices = []
    for n in numbers:
        try:
            val = float(n.replace(',', ''))
            if val > 0:
                prices.append(val)
        except:
            pass

    # 分配价格（根据方向判断）
    if signal["direction"] == "buy":
        # 多头：第一个价格是入场，后面可能有止损止盈
        if len(prices) >= 1:
            signal["entry"] = prices[0]
        if len(prices) >= 2:
            signal["stop_loss"] = min(prices[1:]) if prices[1:] else 0
            signal["take_profit"] = max(prices[1:]) if prices[1:] else 0
    elif signal["direction"] == "sell":
        # 空头：第一个价格是入场
        if len(prices) >= 1:
            signal["entry"] = prices[0]
        if len(prices) >= 2:
            signal["stop_loss"] = max(prices[1:]) if prices[1:] else 0
            signal["take_profit"] = min(prices[1:]) if prices[1:] else 0

    # 提取置信度
    conf_patterns = [
        r'置信[度率][：:\s]*(\d+)%?',
        r'置信[度率][为是]\s*(\d+)',
        r'信心[度]\s*(\d+)%?',
        r'推荐程度\s*(\d+)',
        r'评分\s*(\d+)/10'
    ]
    for pattern in conf_patterns:
        match = re.search(pattern, text)
        if match:
            val = int(match.group(1))
            if val <= 10:
                signal["confidence"] = val * 10  # 转换为百分比
            else:
                signal["confidence"] = min(val, 100)
            break

    return signal


async def execute_trade(signal: dict, amount: float = 0.01) -> dict:
    """执行交易（模拟/真实）"""
    global latest_signal, trade_history

    # 更新最新信号
    latest_signal.update(signal)
    latest_signal["executed"] = False

    # 模拟执行（TODO: 对接真实券商API）
    trade_record = {
        "id": signal["id"],
        "symbol": signal["symbol"],
        "direction": signal["direction"],
        "entry": signal["entry"],
        "stop_loss": signal["stop_loss"],
        "take_profit": signal["take_profit"],
        "amount": amount,
        "confidence": signal["confidence"],
        "timestamp": datetime.now().isoformat(),
        "status": "pending"
    }

    # TODO: 对接真实交易
    # if TRADE_EXCHANGE == "mt5":
    #     from MT5_API import execute_order
    #     execute_order(symbol, direction, amount, stop_loss, take_profit)
    # elif TRADE_EXCHANGE == "binance":
    #     from binance_api import place_order
    #     place_order(symbol, direction, amount)

    # 模拟成功
    trade_record["status"] = "simulated"
    latest_signal["executed"] = True
    trade_history.append(trade_record)

    return trade_record


# ============ 路由端点 ============
@router.get("/health")
async def health():
    """健康检查"""
    return {
        "status": "ok",
        "service": "Auto Trade",
        "enabled": AUTO_TRADE_ENABLED,
        "exchange": TRADE_EXCHANGE,
        "min_confidence": AUTO_TRADE_MIN_CONFIDENCE
    }


@router.get("/status")
async def get_status():
    """获取自动交易状态"""
    return {
        "enabled": AUTO_TRADE_ENABLED,
        "exchange": TRADE_EXCHANGE,
        "min_confidence": AUTO_TRADE_MIN_CONFIDENCE,
        "latest_signal": latest_signal,
        "history_count": len(trade_history)
    }


@router.post("/enable")
async def enable(auto: bool = True):
    """启用/禁用自动交易"""
    global AUTO_TRADE_ENABLED
    AUTO_TRADE_ENABLED = auto
    return {
        "enabled": AUTO_TRADE_ENABLED,
        "message": "自动交易已启用" if auto else "自动交易已禁用"
    }


@router.post("/analyze")
async def analyze_market(request: MarketAnalysisRequest):
    """
    AI 市场分析接口
    - 分析指定品种的技术面
    - 生成交易信号
    """
    indicators = request.indicators or ["MA", "MACD", "RSI"]

    prompt = f"""请对以下品种进行技术分析：

交易品种：{request.symbol}
交易所：{request.exchange}
时间周期：{request.timeframe}
关注指标：{', '.join(indicators)}

请输出：
1. 当前趋势（上涨/下跌/震荡）
2. 关键支撑位和阻力位
3. 指标解读（{'/'.join(indicators)}）
4. 综合交易信号：做多/做空/观望
5. 建议入场价格
6. 止损位和止盈位
7. 置信度（0-100%）

格式示例：
趋势：[]
支撑：[]
阻力：[]
信号：[做多/做空/观望]
入场：[价格]
止损：[价格]
止盈：[价格]
置信度：[XX%]"""

    messages = [
        {"role": "system", "content": "你是专业的量化交易分析师，擅长技术分析和风险评估。"},
        {"role": "user", "content": prompt}
    ]

    try:
        result = await call_deepseek(messages)
        content = result["choices"][0]["message"]["content"]

        # 解析信号
        signal = parse_signal_from_text(content, request.symbol)
        global latest_signal
        latest_signal.update(signal)

        return {
            "success": True,
            "symbol": request.symbol,
            "timeframe": request.timeframe,
            "analysis": content,
            "signal": signal,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"分析失败：{str(e)}",
            "symbol": request.symbol,
            "timestamp": datetime.now().isoformat()
        }


@router.post("/signal")
async def get_signal(request: TradeSignalRequest):
    """
    快速获取交易信号
    - 根据 AI 分析直接返回信号
    """
    prompt = f"""快速分析 {request.symbol} 并给出交易信号。

要求：
1. 只输出：信号方向、建议价格、止损、止盈、置信度
2. 格式简洁，便于程序解析
3. 如果没有明显机会，建议观望"""

    messages = [
        {"role": "system", "content": "你是一个简洁的交易信号生成器。"},
        {"role": "user", "content": prompt}
    ]

    try:
        result = await call_deepseek(messages)
        content = result["choices"][0]["message"]["content"]

        signal = parse_signal_from_text(content, request.symbol)

        # 检查置信度阈值
        if signal["confidence"] < (request.confidence_threshold or AUTO_TRADE_MIN_CONFIDENCE):
            signal["direction"] = "hold"
            signal["reason"] = f"置信度 {signal['confidence']}% 低于阈值，暂不推荐"

        global latest_signal
        latest_signal.update(signal)

        return {
            "success": True,
            "signal": signal,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"信号生成失败：{str(e)}",
            "timestamp": datetime.now().isoformat()
        }


@router.post("/execute")
async def execute(request: ExecuteTradeRequest):
    """
    执行交易
    - 手动指定参数执行交易
    - 或执行 AI 生成的信号
    """
    if not AUTO_TRADE_ENABLED:
        return {
            "success": False,
            "message": "自动交易未启用，请在设置中开启",
            "timestamp": datetime.now().isoformat()
        }

    signal = {
        "id": f"manual_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "symbol": request.symbol,
        "direction": request.direction,
        "entry": request.price or latest_signal.get("entry", 0),
        "stop_loss": request.stop_loss or latest_signal.get("stop_loss", 0),
        "take_profit": request.take_profit or latest_signal.get("take_profit", 0),
        "confidence": latest_signal.get("confidence", 50),
        "reason": request.comment or "手动执行",
        "model": "manual",
        "timestamp": datetime.now().isoformat(),
        "executed": False
    }

    try:
        result = await execute_trade(signal, request.amount)
        return {
            "success": True,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"交易执行失败：{str(e)}",
            "timestamp": datetime.now().isoformat()
        }


@router.get("/latest")
async def get_latest_signal():
    """获取最新交易信号"""
    return {
        "success": True,
        "signal": latest_signal,
        "timestamp": datetime.now().isoformat()
    }


@router.get("/history")
async def get_history(limit: int = 20):
    """获取交易历史"""
    history = trade_history[-limit:] if limit > 0 else trade_history
    return {
        "success": True,
        "history": history,
        "total": len(trade_history)
    }


@router.post("/history/clear")
async def clear_history():
    """清除交易历史"""
    global trade_history
    trade_history.clear()
    return {"success": True, "message": "交易历史已清除"}
