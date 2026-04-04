"""
AI Chat 路由 - 真正的Groq AI对接
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

router = APIRouter(prefix="/api/ai", tags=["AI"])

# Groq API 配置
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# 交易专家系统提示词
TRADE_EXPERT_PROMPT = """你是专业的量化交易AI助手。用中文简洁回答。
分析格式：
📊 【{symbol} 交易分析】
🎯 趋势：[上涨/下跌/震荡]
💰 关键位：阻力 XXXXX | 支撑 XXXXX
⚡ 操作建议：[做多/做空/观望]
🛡️ 止损：XXXXX
🎯 止盈：XXXXX
📈 盈亏比：X:1

注意：只提供分析建议，不构成投资建议。"""


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    symbol: Optional[str] = None
    direction: Optional[str] = None  # buy/sell
    amount: Optional[float] = None
    price: Optional[float] = None


class MarketAnalysisRequest(BaseModel):
    symbol: str
    timeframe: Optional[str] = "1h"  # 1m, 5m, 15m, 1h, 4h, 1d


class SignalRequest(BaseModel):
    symbol: str
    exchange: Optional[str] = None


# 交易专家系统提示
TRADING_EXPERT_PROMPT = """你是一个专业的量化交易AI助手，精通技术分析、风险管理和交易策略。

回答规则：
1. 用中文回答
2. 简洁专业，重点突出
3. 交易建议要包含入场位、止损位、止盈位
4. 风险提示要醒目

分析格式示例：
📊 【{symbol} 市场分析】
🎯 趋势：[上涨/下跌/震荡]
💰 关键位：阻力 {resistance} | 支撑 {support}
⚡ 操作建议：[做多/做空/观望]
🛡️ 风险管理：止损 {stop_loss} | 止盈 {take_profit}
📈 盈亏比：[比例]

如果是交易执行请求，格式：
🎯 【交易执行】
交易对：{symbol}
方向：{direction}
数量：{amount}
入场参考：{entry}
止损：{stop_loss}
止盈：{take_profit}
⚠️ 风险：{risk_level}"""


async def call_groq_ai(messages: List[dict], max_tokens: int = 800) -> str:
    """调用Groq AI API"""
    if not GROQ_API_KEY:
        return "❌ AI服务未配置API密钥"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": GROQ_MODEL,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": max_tokens
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(GROQ_API_URL, headers=headers, json=payload)

            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                error = response.json()
                return f"❌ AI响应错误: {error.get('error', {}).get('message', '未知错误')}"

    except httpx.TimeoutException:
        return "❌ AI响应超时，请稍后重试"
    except Exception as e:
        return f"❌ AI服务异常: {str(e)}"


@router.post("/chat")
async def chat(request: ChatRequest):
    """
    AI对话接口 - 通用聊天
    """
    # 构建消息
    messages = [
        {"role": "system", "content": TRADE_EXPERT_PROMPT.replace("{symbol}", request.symbol or "通用")
         .replace("{resistance}", "待分析").replace("{support}", "待分析")
         .replace("{stop_loss}", "待定").replace("{take_profit}", "待定")
         .replace("{direction}", request.direction or "分析中").replace("{amount}", str(request.amount or 0))
         .replace("{entry}", "待分析").replace("{risk_level}", "中等")},
        {"role": "user", "content": request.message}
    ]

    response = await call_groq_ai(messages)

    return {
        "success": True,
        "message": response,
        "symbol": request.symbol,
        "model": GROQ_MODEL,
        "timestamp": datetime.now().isoformat()
    }


@router.post("/analyze")
async def analyze_market(request: MarketAnalysisRequest):
    """
    AI市场分析接口 - 针对特定交易对
    """
    symbol = request.symbol.upper()
    timeframe = request.timeframe or "1h"

    # 模拟当前行情数据（实际应从交易所API获取）
    market_context = f"""
交易对：{symbol}
时间周期：{timeframe}
当前价格：$42,500 (模拟)
24h涨跌：+2.35%
成交量：1.2B USDT
市场情绪：偏多

请给出专业的技术分析和交易建议。
"""

    messages = [
        {"role": "system", "content": TRADE_EXPERT_PROMPT},
        {"role": "user", "content": f"请分析 {symbol} 的市场走势：\n{market_context}"}
    ]

    response = await call_groq_ai(messages, max_tokens=1000)

    return {
        "success": True,
        "symbol": symbol,
        "timeframe": timeframe,
        "analysis": response,
        "model": GROQ_MODEL,
        "timestamp": datetime.now().isoformat()
    }


@router.post("/signal")
async def generate_signal(request: SignalRequest):
    """
    AI交易信号接口 - 生成交易信号
    """
    symbol = request.symbol.upper()
    exchange = request.exchange or "Binance"

    signal_context = f"""
交易对：{symbol}
交易所：{exchange}
模式：信号生成模式

请生成一个具体的交易信号，包含：
1. 入场理由
2. 具体入场价格
3. 止损价格
4. 止盈价格
5. 建议仓位
6. 风险等级
"""

    messages = [
        {"role": "system", "content": TRADE_EXPERT_PROMPT},
        {"role": "user", "content": signal_context}
    ]

    response = await call_groq_ai(messages, max_tokens=1200)

    return {
        "success": True,
        "symbol": symbol,
        "exchange": exchange,
        "signal": response,
        "model": GROQ_MODEL,
        "timestamp": datetime.now().isoformat()
    }


@router.get("/models")
async def get_models():
    """获取当前使用的AI模型信息"""
    return {
        "provider": "Groq",
        "model": GROQ_MODEL,
        "status": "active" if GROQ_API_KEY else "inactive",
        "api_configured": bool(GROQ_API_KEY)
    }


@router.get("/health")
async def health_check():
    """AI服务健康检查"""
    if not GROQ_API_KEY:
        return {"status": "error", "message": "API密钥未配置"}

    # 简单测试
    messages = [{"role": "user", "content": "hi"}]
    response = await call_groq_ai(messages, max_tokens=10)

    if "❌" in response:
        return {"status": "error", "message": response}
    else:
        return {
            "status": "ok",
            "model": GROQ_MODEL,
            "message": "AI服务正常运行"
        }
