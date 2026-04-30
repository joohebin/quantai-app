"""
客服 AI 路由 - 走服务器 DeepSeek Key，绕过浏览器 CORS 限制
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import os
import httpx
import asyncio
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/api/cs", tags=["CustomerService"])

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "sk-6fd3a4a562e14d7d8885f74d44b2b730")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1"
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

CS_SYSTEM_PROMPT = """你是 QuantAI 量化交易平台的 AI 客服助手，熟悉平台所有功能，可回答用户关于使用方法的任何问题。

【平台功能模块】
• 仪表盘：资产总览、实时行情
• 行情：22个交易品种K线（BTC/ETH/SOL/BNB/XRP外汇/黄金/原油/纳指/标普/恒生等）
• AI顾问：行情分析、仓位建议、策略推荐、指标解读
• 持仓：查看当前持仓、AI分析按钮
• 策略管理：MACD/EMA/RSI/网格/布林带策略创建和启动
• 回测：历史数据验证策略（日期范围/品种/仓位比例可配置）
• 复制交易：跟随交易者、自动同步开仓
• 自动建仓（Elite专属）：策略触发/定时定投(DCA)/跟单同步
• 交易广场：分享观点、情绪标签
• 策略市场：发现/购买/发布量化策略
• 信号广播：发布交易信号供他人订阅
• 我的账户：券商连接（币安/OKX/INFINOX MT5）、套餐升级、风控设置
• FRED宏观数据：美联储利率/CPI/非农/GDP（offline时显示静态默认值）
• 法律文档：隐私政策/服务条款/Cookie政策/社区准则（在"我的账户"底部）

【订阅套餐】
| 套餐 | 价格 | 核心功能 |
| Basic | $29/月 | 全品种行情、AI顾问、2个策略、自动交易 |
| Pro | $79/月 | 无限策略、AI自动交易、高级回测、多券商 |
| Elite | $199/月 | 自动建仓(策略/定投/跟单)、复制交易无限跟单、VIP客服、优先通道 |

【支持语言】中文/English/日本語/한국어/Русский/العربية，右上角切换，实时生效

【常见问题】
Q:K线不显示？→ Ctrl+Shift+R强制刷新/换浏览器/关AdBlock
Q:FRED offline？→ 中国大陆网络无法访问，显示静态默认值不影响使用
Q:连接券商？→ 我的账户→已连接券商→添加新券商
Q:自动建仓？→ Elite专属，策略触发/定时定投/跟单同步3种模式
Q:API Key安全？→ 存本地localStorage，不上传；建议不开提现权限+IP白名单

【回复规则】
1.简洁友好，不超过200字，**加粗重点**
2.涉及支付/账户安全 → "需要人工客服协助，请说【转人工】"
3.功能问题 → 告知【具体页面和操作步骤】
4.语言跟随用户
5.不确定 → 转人工，不胡乱回答"""


class ChatRequest(BaseModel):
    message: str
    history: Optional[list] = []  # [{"role":"user"|"assistant","content":"..."}]


async def call_deepseek(messages: list, max_tokens: int = 300) -> str:
    """调用 DeepSeek API"""
    if not DEEPSEEK_API_KEY:
        return None
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": DEEPSEEK_MODEL,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": 0.7,
    }
    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.post(DEEPSEEK_API_URL, headers=headers, json=payload)
        if not r.is_success:
            return None
        data = r.json()
        return data["choices"][0]["message"]["content"] if data.get("choices") else None


@router.post("/chat")
async def cs_chat(request: ChatRequest):
    """客服对话接口"""
    if not DEEPSEEK_API_KEY:
        return {"success": False, "error": "DeepSeek API not configured on server"}

    # 构建消息
    msgs = [{"role": "system", "content": CS_SYSTEM_PROMPT}]
    # 加入历史（最近6条）
    history = request.history[-12:] if request.history else []
    msgs.extend(history)
    msgs.append({"role": "user", "content": request.message})

    reply = await call_deepseek(msgs)
    if not reply:
        return {"success": False, "error": "DeepSeek API call failed"}

    return {"success": True, "reply": reply}
