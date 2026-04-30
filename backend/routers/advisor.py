"""
AI 顾问路由 - DeepSeek 直连
功能：用户可以在 App 里跟 DeepSeek 聊天
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import os
import httpx
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/api/advisor", tags=["AI Advisor"])

# DeepSeek API 配置
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "sk-eb727437f0b64b0b8fbb3b8fb4554cc5")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1"
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

# 系统提示词 - QuantAI 金融顾问
ADVISOR_SYSTEM_PROMPT = """你是一个专业的量化交易与金融投资顾问 AI 助手，名叫 QuantAI Advisor。

你的专长：
- 量化交易策略分析
- 技术分析与指标解读（MA, MACD, RSI, Bollinger Bands 等）
- 风险管理建议
- 市场趋势研判
- 投资组合优化建议
- 风险警示与合规提示

回答规则：
1. 用用户使用的语言回答（检测 message 内容）
2. 专业但易懂，避免过度技术术语
3. 重要风险提示要醒目
4. 不确定性时要诚实说明
5. 不预测具体价格，但可以分析支撑阻力区间
6. 免责声明：投资有风险，决策需谨慎

关于 QuantAI 平台：
- 支持 MT5 外汇/贵金属交易
- 支持 Binance/OKX 等主流交易所
- 提供策略回测、信号生成、自动交易等功能
- 客服邮箱：support@quantai.app"""

# 对话历史（内存存储，生产环境建议用 Redis）
chat_history: List[dict] = []


# ============ 请求/响应模型 ============
class Message(BaseModel):
    role: str  # system / user / assistant
    content: str


class AdvisorRequest(BaseModel):
    message: str
    symbol: Optional[str] = None
    mode: Optional[str] = "advisor"  # advisor / technical / strategy / risk


class AdvisorResponse(BaseModel):
    success: bool
    message: str
    symbol: Optional[str] = None
    mode: str
    timestamp: str


# ============ API 调用 ============
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
        "temperature": 0.7
    }

    try:
        async with httpx.AsyncClient(timeout=90.0) as client:
            response = await client.post(DEEPSEEK_API_URL, headers=headers, json=payload)

            if response.status_code == 200:
                return response.json()
            else:
                error_data = response.json()
                raise Exception(f"DeepSeek API Error: {error_data.get('error', {}).get('message', response.text)}")

    except httpx.TimeoutException:
        raise Exception("AI 响应超时，请稍后重试")
    except Exception as e:
        raise Exception(f"AI 服务异常: {str(e)}")


# ============ 路由端点 ============
@router.get("/health")
async def health():
    """健康检查"""
    return {
        "status": "ok",
        "service": "QuantAI Advisor",
        "model": DEEPSEEK_MODEL,
        "provider": "DeepSeek"
    }


@router.get("/models")
async def list_models():
    """可用模型"""
    return {
        "models": [
            {
                "id": DEEPSEEK_MODEL,
                "name": "DeepSeek V3",
                "provider": "DeepSeek",
                "use_case": "金融分析与交易策略"
            }
        ]
    }


@router.post("/chat")
async def chat(request: AdvisorRequest):
    """
    AI 顾问对话接口
    - 用户发送消息
    - DeepSeek 回复
    - 支持多种模式（顾问/技术/策略/风险）
    """
    # 根据模式调整系统提示
    mode_prompts = {
        "advisor": "作为金融投资顾问回答",
        "technical": "作为技术分析专家回答，重点关注K线、均线、MACD、RSI等技术指标",
        "strategy": "作为量化策略分析师回答，提供具体的交易策略和参数",
        "risk": "作为风险管理专家回答，重点分析潜在风险和仓位管理建议"
    }

    mode_instruction = mode_prompts.get(request.mode, mode_prompts["advisor"])

    messages = [
        {"role": "system", "content": f"{ADVISOR_SYSTEM_PROMPT}\n\n当前模式：{mode_instruction}"}
    ]

    # 添加上下文（如果有指定交易品种）
    if request.symbol:
        messages.append({
            "role": "system",
            "content": f"当前关注品种：{request.symbol}，用户可能想了解这个品种的分析"
        })

    # 添加历史对话（最近5轮）
    for msg in chat_history[-10:]:
        messages.append(msg)

    # 添加当前消息
    messages.append({"role": "user", "content": request.message})

    try:
        result = await call_deepseek(messages)
        reply = result["choices"][0]["message"]["content"]

        # 保存到历史
        chat_history.append({"role": "user", "content": request.message})
        chat_history.append({"role": "assistant", "content": reply})

        # 限制历史长度
        if len(chat_history) > 50:
            chat_history[:] = chat_history[-50:]

        return {
            "success": True,
            "message": reply,
            "symbol": request.symbol,
            "mode": request.mode or "advisor",
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"抱歉，AI 顾问暂时无法响应：{str(e)}",
            "symbol": request.symbol,
            "mode": request.mode or "advisor",
            "timestamp": datetime.now().isoformat()
        }


@router.post("/clear")
async def clear_history():
    """清除对话历史"""
    chat_history.clear()
    return {"success": True, "message": "对话历史已清除"}


@router.get("/history")
async def get_history(limit: int = 10):
    """获取对话历史"""
    history = chat_history[-limit:] if limit > 0 else chat_history
    return {
        "success": True,
        "history": history,
        "total": len(chat_history)
    }


@router.post("/analyze")
async def analyze(
    symbol: str,
    direction: Optional[str] = None,
    amount: Optional[float] = None,
    price: Optional[float] = None
):
    """
    快速分析接口 - 针对特定交易信号分析
    """
    analysis_prompt = f"""请分析以下交易建议：

交易品种：{symbol}
交易方向：{direction or "待定"}
交易数量：{amount or "待定"}
入场价格：{price or "待定"}

请从以下角度分析：
1. 这个交易是否合理？
2. 风险有多大？
3. 建议的止损/止盈位？
4. 仓位管理建议？
5. 综合评分（1-10分）"""

    messages = [
        {"role": "system", "content": ADVISOR_SYSTEM_PROMPT},
        {"role": "user", "content": analysis_prompt}
    ]

    try:
        result = await call_deepseek(messages)
        reply = result["choices"][0]["message"]["content"]

        return {
            "success": True,
            "symbol": symbol,
            "analysis": reply,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "success": False,
            "analysis": f"分析失败：{str(e)}",
            "symbol": symbol,
            "timestamp": datetime.now().isoformat()
        }
