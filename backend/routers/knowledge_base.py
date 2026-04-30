"""
知识库 API - QuantAI 平台相关问答
功能：
- QuantAI 平台使用指南
- 功能介绍
- 常见问题解答
- API 接口说明
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import os
import httpx
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/api/kb", tags=["Knowledge Base"])

# DeepSeek API 配置
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "sk-eb727437f0b64b0b8fbb3b8fb4554cc5")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1"
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

# QuantAI 知识库内容
QUANTAI_KNOWLEDGE = """
# QuantAI 平台知识库

## 平台概述
QuantAI 是一个 AI 驱动的量化交易 SaaS 平台，支持：
- MT5 外汇/贵金属交易
- Binance/OKX 等加密货币交易所
- 多语言支持（18种语言）
- 策略回测与优化
- AI 智能分析与信号生成
- 自动交易执行

## 主要功能模块

### 1. 仪表盘 (Dashboard)
- 账户概览（余额、净值、盈亏）
- MT5 连接状态
- 实时持仓
- 风险指标

### 2. 市场 (Market)
- 实时行情查看
- 多交易所聚合
- 价格预警设置

### 3. AI 聊天 (AI Chat)
- AI 顾问对话
- 市场分析
- 策略建议
- 风险提示

### 4. 持仓 (Positions)
- 当前持仓列表
- 持仓详情（开仓价、现价、盈亏）
- 平仓操作

### 5. 策略 (Strategies)
- 策略创建与编辑
- 策略回测
- 策略市场（分享/购买）

### 6. 自动交易 (Auto Trade)
- AI 信号跟单
- 自动执行开关
- 交易历史

### 7. 跟单交易 (Copy Trading)
- 跟随高手策略
- 跟单管理
- 收益追踪

## 使用指南

### MT5 连接
1. 在 MT5 终端打开 EA 插件
2. 获取服务器地址和 Token
3. 在 QuantAI 的"账户"页面添加 MT5 连接

### 策略创建
1. 选择策略类型（趋势/网格/马丁/套利）
2. 设置参数（交易对、仓位、止盈止损）
3. 进行回测验证
4. 模拟盘测试
5. 开启实盘

### API 接口
基础 URL: http://35.179.161.45:8001
- POST /api/auth/login - 用户登录
- GET /api/positions/ - 获取持仓
- POST /api/orders/ - 创建订单
- GET /api/meta/dashboard - MT5 仪表盘
- POST /api/advisor/chat - AI 顾问对话
- POST /api/auto-trade/analyze - AI 市场分析

## 客服支持
- 邮箱: support@quantai.app
- Telegram Bot: @quantai_support_bot
- 文档: https://quantai.app/docs

## 常见问题

### Q: MT5 连接失败怎么办？
A: 检查 1) MT5 终端是否运行 2) EA 插件是否启用 3) Token 是否过期 4) 网络是否可达

### Q: 自动交易安全吗？
A: 建议先在模拟盘测试，确认策略有效后再开启实盘。同时设置合理的止损和仓位上限。

### Q: 如何提高 AI 分析准确性？
A: 1) 提供具体的交易品种和时间框架 2) 参考 AI 建议但结合自己的判断 3) 关注风险提示

### Q: 支持哪些交易所？
A: MT5（外汇/贵金属）、Binance（加密货币）、OKX（加密货币）

### Q: 手续费如何计算？
A: 手续费因交易所而异。MT5 通常有点差，Binance 有 Maker/Taker 费率。

## 风险提示
- 投资有风险，入市需谨慎
- 过去表现不代表未来收益
- 请根据自身风险承受能力合理配置
- AI 分析仅供参考，不构成投资建议
"""

# 常见问题快速回复
FAQ_ANSWERS = {
    "如何注册": "访问 quantai.app，点击注册按钮，填写邮箱和密码即可完成注册。",
    "如何连接MT5": "在 MT5 终端启用 EA 插件，获取服务器地址和 Token，然后在 QuantAI 的账户页面添加 MT5 连接。",
    "如何开始自动交易": "1. 确保已连接券商账户 2. 在自动交易页面开启自动交易开关 3. 设置最小置信度阈值 4. 系统将自动执行 AI 推荐的信号",
    "手续费多少": "QuantAI 平台不收取额外手续费。交易手续费由交易所收取（MT5 为点差，Binance 有 Maker/Taker 费率）。",
    "如何联系客服": "可以通过 support@quantai.app 邮箱联系我们，或在 Telegram 搜索 @quantai_support_bot",
    "支持哪些货币对": "MT5 支持外汇（EUR/USD, GBP/USD 等）和贵金属（XAU/USD）。Binance 支持主流加密货币对。",
    "如何设置止损止盈": "在创建策略时设置止损/止盈参数，或在持仓页面手动添加。推荐止损设置在入场价的 1-2%。",
    "账户安全": "我们使用 JWT Token 认证，所有数据传输使用 HTTPS 加密。请勿将账户信息透露给他人。"
}


# ============ 请求/响应模型 ============
class KBQuestion(BaseModel):
    question: str
    category: Optional[str] = None  # general / trading / technical / account


class SearchRequest(BaseModel):
    keyword: str
    limit: Optional[int] = 5


# ============ API 调用 ============
async def call_deepseek(messages: List[dict], max_tokens: int = 800) -> dict:
    """调用 DeepSeek API"""
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": DEEPSEEK_MODEL,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": 0.5
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(DEEPSEEK_API_URL, headers=headers, json=payload)

            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"API Error: {response.status_code}")

    except httpx.TimeoutException:
        raise Exception("AI 响应超时")
    except Exception as e:
        raise Exception(f"AI 服务异常: {str(e)}")


# ============ 路由端点 ============
@router.get("/health")
async def health():
    """健康检查"""
    return {
        "status": "ok",
        "service": "QuantAI Knowledge Base",
        "knowledge_loaded": True
    }


@router.get("/info")
async def get_platform_info():
    """获取平台基本信息"""
    return {
        "name": "QuantAI",
        "version": "1.0.0",
        "website": "https://quantai.app",
        "support_email": "support@quantai.app",
        "telegram": "@quantai_support_bot",
        "supported_exchanges": ["MT5", "Binance", "OKX"],
        "supported_markets": ["Forex", "Precious Metals", "Crypto"],
        "languages": 18
    }


@router.get("/modules")
async def get_modules():
    """获取所有功能模块"""
    return {
        "modules": [
            {
                "id": "dashboard",
                "name": "仪表盘",
                "name_en": "Dashboard",
                "description": "账户概览与风险指标"
            },
            {
                "id": "market",
                "name": "市场",
                "name_en": "Market",
                "description": "实时行情与价格监控"
            },
            {
                "id": "ai-chat",
                "name": "AI 顾问",
                "name_en": "AI Advisor",
                "description": "AI 对话与交易咨询"
            },
            {
                "id": "positions",
                "name": "持仓",
                "name_en": "Positions",
                "description": "当前持仓管理"
            },
            {
                "id": "strategies",
                "name": "策略",
                "name_en": "Strategies",
                "description": "量化策略创建与回测"
            },
            {
                "id": "auto-trade",
                "name": "自动交易",
                "name_en": "Auto Trade",
                "description": "AI 信号自动执行"
            },
            {
                "id": "copy-trading",
                "name": "跟单交易",
                "name_en": "Copy Trading",
                "description": "跟随高手策略"
            },
            {
                "id": "backtest",
                "name": "回测",
                "name_en": "Backtest",
                "description": "策略历史回测"
            }
        ]
    }


@router.get("/faq")
async def get_faq():
    """获取常见问题列表"""
    return {
        "success": True,
        "faq": [
            {"question": k, "answer": v}
            for k, v in FAQ_ANSWERS.items()
        ]
    }


@router.post("/faq/search")
async def search_faq(request: SearchRequest):
    """搜索常见问题"""
    keyword = request.keyword.lower()
    results = []

    for question, answer in FAQ_ANSWERS.items():
        if keyword in question.lower() or keyword in answer.lower():
            results.append({
                "question": question,
                "answer": answer
            })

    return {
        "success": True,
        "keyword": request.keyword,
        "results": results[:request.limit or 5],
        "total": len(results)
    }


@router.post("/ask")
async def ask_question(request: KBQuestion):
    """
    问答接口 - 基于知识库回答问题
    """
    prompt = f"""你是一个 QuantAI 平台的客服助手，基于以下知识库回答用户问题。

知识库：
{QUANTAI_KNOWLEDGE}

常见问答：
{chr(10).join([f"Q: {k}\\nA: {v}" for k, v in FAQ_ANSWERS.items()])}

用户问题：{request.question}

回答规则：
1. 首先在知识库中查找相关信息
2. 如果知识库有明确答案，优先使用
3. 如果没有，用你的理解给出合理建议
4. 回答要简洁、专业
5. 适当引导用户使用平台功能
6. 结尾加一句友好的提示"""

    messages = [
        {"role": "system", "content": "你是 QuantAI 平台的客服助手。"},
        {"role": "user", "content": prompt}
    ]

    try:
        result = await call_deepseek(messages)
        answer = result["choices"][0]["message"]["content"]

        return {
            "success": True,
            "question": request.question,
            "answer": answer,
            "category": request.category or "general",
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        # 降级到 FAQ 匹配
        keyword = request.question.lower()
        for q, a in FAQ_ANSWERS.items():
            if any(word in keyword for word in q.lower().split()):
                return {
                    "success": True,
                    "question": request.question,
                    "answer": f"找到相关回答：{a}",
                    "category": "faq",
                    "fallback": True,
                    "timestamp": datetime.now().isoformat()
                }

        return {
            "success": False,
            "question": request.question,
            "answer": f"抱歉，我暂时无法回答这个问题。建议您联系客服：support@quantai.app",
            "timestamp": datetime.now().isoformat()
        }


@router.get("/guide/{topic}")
async def get_guide(topic: str):
    """获取功能使用指南"""
    guides = {
        "mt5": {
            "title": "MT5 连接指南",
            "steps": [
                "打开 MT5 终端",
                "导航到 'EA交易' 面板",
                "启用 EA 插件",
                "获取服务器地址和 Token",
                "在 QuantAI 账户页面添加 MT5 连接"
            ]
        },
        "strategy": {
            "title": "策略创建指南",
            "steps": [
                "进入策略页面",
                "点击'创建策略'",
                "选择策略类型（趋势/网格/马丁/套利）",
                "设置交易参数",
                "进行回测验证",
                "模拟盘测试",
                "开启实盘"
            ]
        },
        "auto-trade": {
            "title": "自动交易设置指南",
            "steps": [
                "确保已连接券商账户",
                "进入自动交易页面",
                "开启自动交易开关",
                "设置最小置信度阈值（推荐70%）",
                "设置单笔最大仓位",
                "系统将自动执行 AI 推荐的信号"
            ]
        },
        "api": {
            "title": "API 使用指南",
            "endpoints": [
                "POST /api/auth/login - 用户登录",
                "GET /api/positions/ - 获取持仓",
                "POST /api/orders/ - 创建订单",
                "GET /api/meta/dashboard - MT5 仪表盘",
                "POST /api/advisor/chat - AI 顾问对话",
                "POST /api/auto-trade/analyze - AI 市场分析",
                "GET /api/kb/ask - 知识库问答"
            ]
        }
    }

    if topic in guides:
        return {
            "success": True,
            "guide": guides[topic]
        }
    else:
        return {
            "success": False,
            "message": f"未找到 '{topic}' 的指南，可用的指南：{', '.join(guides.keys())}"
        }


@router.get("/knowledge")
async def get_knowledge():
    """获取完整知识库（用于同步到本地）"""
    return {
        "success": True,
        "knowledge": QUANTAI_KNOWLEDGE,
        "faq": FAQ_ANSWERS,
        "updated_at": datetime.now().isoformat()
    }
