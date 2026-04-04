#!/usr/bin/env python3
"""
QuantAI Telegram 客服 Bot
功能：
  - 用户私聊 Bot → Groq AI 自动回复（携带知识库 prompt）
  - 检测到"转人工"关键词 → 通知老板 TG 并告知用户
  - 老板在通知消息上回复 → Bot 转发给用户
  - /start、/help、/plan、/contact 快捷命令
  - 多语言自动识别（langdetect）
  - 对话历史支持多轮上下文（每用户最近 10 条）

配置说明：
  1. 在下方 CONFIG 区填写 BOT_TOKEN（从 @BotFather 创建）和 GROQ_API_KEY
  2. ADMIN_CHAT_ID 填你自己的 Telegram 数字 ID（@userinfobot 可查）
  3. python tg_support_bot.py 运行
"""

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

import logging
import asyncio
import json
import re
from datetime import datetime
from groq import AsyncGroq
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup,
    BotCommand
)
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters
)

# ────────── 配置区 ──────────
CONFIG = {
    "BOT_TOKEN": "8226286731:AAHjjcN3pFgUkMEnIxbHWJ8T2HR7_m6CHZs",  # @QuantAI_CS_bot
    "GROQ_API_KEY": "YOUR_GROQ_API_KEY_HERE",  # 从 promo-bot/config.py
    "GROQ_MODEL": "llama-3.3-70b-versatile",
    "ADMIN_CHAT_ID": 6665770176,              # @umihama 的 TG ID
    "MAX_HISTORY": 10,                         # 每用户保留的对话轮数
    "MAX_TOKENS": 400,                         # AI 回复最大 token
}

HANDOFF_KEYWORDS = [
    "转人工", "人工客服", "真人", "客服", "投诉", "紧急",
    "human agent", "human support", "talk to human", "real person",
    "urgent", "complaint", "escalate",
]

# ────────── 知识库 System Prompt ──────────
SYSTEM_PROMPT = """你是 QuantAI 量化交易平台的专业客服助手（Telegram Bot）。

【平台功能】
- 仪表盘：总资产/今日盈亏/活跃策略/持仓概览 + K线图
- 行情：22个品种实时行情（加密/外汇/贵金属/能源/指数/国债）
- AI顾问：智能对话，策略建议、仓位分配、行情分析
- 持仓：管理当前持仓，一键平仓/修改/AI分析
- 策略：MACD/EMA/RSI/网格/布林带量化策略管理
- 回测：历史数据验证策略绩效（收益率/夏普/胜率等）
- 复制交易：跟随排行榜顶级交易者，实时信号同步
- 自动建仓（Elite专属）：策略触发/定投DCA/跟单同步
- 交易广场：社区分享观点、情绪标签（看多/看空/中性）
- 策略市场：发现/购买/发布量化策略（支持Pine Script）
- 信号广播：实时交易信号发布与订阅，可接入自动建仓
- FRED宏观数据：联邦基准利率/10Y国债/CPI/非农/GDP（来自美联储圣路易斯联储）

【支持品种】
加密货币：BTC/USDT、ETH/USDT、SOL/USDT、BNB、XRP
外汇：EUR/USD、GBP/USD、USD/JPY、USD/CHF、AUD/USD
贵金属：XAU/USD（黄金）、XAG/USD（白银）
能源：WTI/USD（美油）、BRENT（布油）
指数：NAS100（纳指）、SPX500（标普）、DOW（道指）、HSI（恒生）、SX5E（欧洲斯托克50）
国债：US10Y、US02Y

【订阅套餐】
- Basic: $29/月 — 全品种行情 + AI问答 + 2个策略 + 自动交易
- Pro: $79/月 — 无限策略 + AI自动交易 + 高级回测 + 多券商
- Elite: $199/月 — 自动建仓 + 复制交易无限跟单 + VIP客服 + 优先执行

【支持语言】中文 / English / 日本語 / 한국어 / Русский / العربية

【回复规则】
1. 简洁友好，不超过200字，重点用 **加粗**
2. 引导到具体页面（左侧菜单/导航）
3. 涉及支付/账号安全/系统异常 → 说明需要人工，引导用户说"转人工"
4. 语言跟随用户输入语言
5. 遇到平台之外的问题（股票选股、法律等）礼貌拒绝
"""

# ────────── 全局状态 ──────────
# key: user_id (int), value: list of {"role", "content"}
user_histories: dict[int, list] = {}

# 转人工记录：key: 通知消息ID(admin收到的), value: {user_id, username}
handoff_pending: dict[int, dict] = {}

# Groq 客户端（全局，懒加载）
groq_client: AsyncGroq | None = None

# ────────── 日志 ──────────
logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s — %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("quantai-cs-bot")


# ════════ 工具函数 ════════

def get_groq():
    global groq_client
    if groq_client is None:
        groq_client = AsyncGroq(api_key=CONFIG["GROQ_API_KEY"])
    return groq_client


def is_handoff_request(text: str) -> bool:
    t = text.lower()
    return any(kw.lower() in t for kw in HANDOFF_KEYWORDS)


def get_history(uid: int) -> list:
    return user_histories.setdefault(uid, [])


def trim_history(uid: int):
    h = user_histories.get(uid, [])
    if len(h) > CONFIG["MAX_HISTORY"] * 2:
        user_histories[uid] = h[-(CONFIG["MAX_HISTORY"] * 2):]


def user_tag(update: Update) -> str:
    u = update.effective_user
    return f"{u.full_name}(@{u.username or '无'}, id:{u.id})"


async def ai_reply(uid: int, user_msg: str) -> str:
    history = get_history(uid)
    history.append({"role": "user", "content": user_msg})
    trim_history(uid)

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history

    try:
        resp = await get_groq().chat.completions.create(
            model=CONFIG["GROQ_MODEL"],
            messages=messages,
            max_tokens=CONFIG["MAX_TOKENS"],
            temperature=0.5,
        )
        reply = resp.choices[0].message.content.strip()
        history.append({"role": "assistant", "content": reply})
        return reply
    except Exception as e:
        logger.error(f"Groq error: {e}")
        return "⚠️ AI 服务暂时不可用，请稍后再试，或说「转人工」联系人工客服。"


# ════════ 命令处理 ════════

WALLPAPER_PATH = r"c:\Users\Administrator\WorkBuddy\Claw\quantai-app\assets\Professional_fintech_Telegram__2026-03-29T18-51-52.png"

async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    kb = [
        [InlineKeyboardButton("💰 套餐价格", callback_data="plan"),
         InlineKeyboardButton("📚 功能介绍", callback_data="features")],
        [InlineKeyboardButton("🔧 故障排查", callback_data="troubleshoot"),
         InlineKeyboardButton("🙋 转人工", callback_data="handoff")],
    ]
    await update.message.reply_text(
        "👋 *欢迎来到 QuantAI 客服中心！*\n\n"
        "我是 QuantAI 智能客服助手，可以帮您：\n"
        "• 解答平台功能和使用方法\n"
        "• 套餐升级咨询\n"
        "• 故障排查\n"
        "• 账户相关问题\n\n"
        "直接发消息提问，或点击下方快捷按钮👇",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(kb)
    )
    # 发送官方聊天背景图
    import os
    if os.path.exists(WALLPAPER_PATH):
        try:
            with open(WALLPAPER_PATH, "rb") as f:
                await update.message.reply_photo(
                    photo=f,
                    caption=(
                        "🎨 *QuantAI 官方聊天背景*\n\n"
                        "长按图片 → *设为聊天背景*，获得更好的对话体验 ✨"
                    ),
                    parse_mode="Markdown"
                )
        except Exception:
            pass


async def cmd_help(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 *QuantAI Bot 命令列表*\n\n"
        "/start — 欢迎菜单\n"
        "/plan — 查看套餐价格\n"
        "/contact — 联系人工客服\n"
        "/clear — 清除对话历史\n\n"
        "直接发消息即可提问 😊",
        parse_mode="Markdown"
    )


async def cmd_plan(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💰 *QuantAI 订阅套餐*\n\n"
        "🔹 *Basic* — $29/月\n"
        "全品种行情、AI顾问问答、2个策略、自动交易\n\n"
        "🔸 *Pro* — $79/月\n"
        "无限策略、AI自动交易、高级回测、多券商支持\n\n"
        "💎 *Elite* — $199/月\n"
        "自动建仓（策略/定投/跟单）、复制交易无限跟单、VIP专属客服、优先执行通道\n\n"
        "升级方式：打开 QuantAI → 左侧菜单【我的账户】→【当前方案】",
        parse_mode="Markdown"
    )


async def cmd_contact(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    await do_handoff(update, ctx, uid, "用户通过 /contact 命令主动发起")


async def cmd_clear(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    user_histories.pop(uid, None)
    await update.message.reply_text("✅ 对话历史已清除，我们重新开始 😊")


# ════════ 回调按钮 ════════

async def on_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    uid = query.from_user.id

    if data == "plan":
        await ctx.bot.send_message(uid, (
            "💰 *QuantAI 套餐*\n\n"
            "Basic $29/月 | Pro $79/月 | Elite $199/月\n\n"
            "详细功能对比请问我，或直接升级：APP → 我的账户 → 当前方案"
        ), parse_mode="Markdown")

    elif data == "features":
        await ctx.bot.send_message(uid, (
            "🚀 *QuantAI 主要功能*\n\n"
            "• 📈 22个品种实时行情\n"
            "• 🤖 AI顾问（策略/仓位/分析）\n"
            "• ⚡ 量化策略（MACD/EMA/RSI等）\n"
            "• 🔬 策略回测\n"
            "• 🔁 复制交易（跟顶级交易者）\n"
            "• ⚙️ 自动建仓 *（Elite）*\n"
            "• 💬 交易广场 + 策略市场\n"
            "• 📡 信号广播\n"
            "• 🏛️ FRED美联储宏观数据\n\n"
            "有什么想深入了解的？直接问我 😊"
        ), parse_mode="Markdown")

    elif data == "troubleshoot":
        await ctx.bot.send_message(uid, (
            "🔧 *常见故障排查*\n\n"
            "❓ *K线图不显示*\n"
            "→ Ctrl+Shift+R 强制刷新，换 Chrome 浏览器试试\n\n"
            "❓ *FRED宏观数据 offline*\n"
            "→ 中国大陆网络无法直连 FRED，显示静态默认值，不影响其他功能\n\n"
            "❓ *行情停止跳动*\n"
            "→ 刷新页面即可，Binance WebSocket 偶有波动\n\n"
            "❓ *其他问题*\n"
            "→ 请描述具体症状发给我 🙏"
        ), parse_mode="Markdown")

    elif data == "handoff":
        await do_handoff(update, ctx, uid, "用户点击按钮主动发起转人工")


# ════════ 消息处理 ════════

async def on_message(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    """处理用户私聊消息"""
    if not update.message or not update.message.text:
        return

    uid = update.effective_user.id
    admin_id = CONFIG["ADMIN_CHAT_ID"]
    text = update.message.text.strip()

    # ── 老板回复转人工通知 → 转发给用户 ──
    if uid == admin_id and update.message.reply_to_message:
        replied_msg_id = update.message.reply_to_message.message_id
        if replied_msg_id in handoff_pending:
            target = handoff_pending[replied_msg_id]
            target_uid = target["user_id"]
            try:
                await ctx.bot.send_message(
                    target_uid,
                    f"👤 *人工客服回复：*\n\n{text}",
                    parse_mode="Markdown"
                )
                await update.message.reply_text(f"✅ 已转发给用户 {target['username']}")
            except Exception as e:
                logger.error(f"转发失败: {e}")
                await update.message.reply_text(f"❌ 转发失败：{e}")
            return

    # ── 转人工检测 ──
    if is_handoff_request(text):
        await do_handoff(update, ctx, uid, text)
        return

    # ── 正常 AI 回复 ──
    # 显示"正在输入"状态
    await ctx.bot.send_chat_action(uid, "typing")

    reply = await ai_reply(uid, text)
    await update.message.reply_text(reply, parse_mode="Markdown")


# ════════ 转人工逻辑 ════════

async def do_handoff(update: Update, ctx: ContextTypes.DEFAULT_TYPE, uid: int, trigger_text: str):
    """触发转人工流程：通知老板 + 告知用户"""
    user = update.effective_user
    username = f"@{user.username}" if user.username else user.full_name
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    admin_id = CONFIG["ADMIN_CHAT_ID"]

    # 通知老板
    notify_text = (
        f"🙋 *QuantAI 转人工请求*\n\n"
        f"👤 用户：{user.full_name}（{username}）\n"
        f"🔢 ID：`{uid}`\n"
        f"🕐 时间：{now}\n"
        f"💬 触发内容：{trigger_text[:100]}\n\n"
        f"*直接回复此消息即可转发给用户。*"
    )
    try:
        sent = await ctx.bot.send_message(admin_id, notify_text, parse_mode="Markdown")
        # 记录映射
        handoff_pending[sent.message_id] = {
            "user_id": uid,
            "username": username,
        }
        logger.info(f"转人工通知已发送，admin msg_id={sent.message_id}, user={username}")
    except Exception as e:
        logger.error(f"无法通知管理员: {e}")

    # 告知用户
    kb = [[InlineKeyboardButton("🤖 继续 AI 客服", callback_data="back_to_ai")]]
    if update.message:
        await update.message.reply_text(
            "🙋 *已为您转接人工客服*\n\n"
            "客服人员将在 *工作时间内* 尽快与您联系（UTC+8 9:00-18:00）。\n\n"
            "如果等待期间有其他问题，可以继续问 AI 助手 😊",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(kb)
        )
    elif update.callback_query:
        await ctx.bot.send_message(
            uid,
            "🙋 *已为您转接人工客服*\n\n"
            "客服人员将在工作时间内尽快与您联系（UTC+8 9:00-18:00）。\n\n"
            "如有其他问题，可以继续向 AI 助手提问 😊",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(kb)
        )


# ════════ 主程序 ════════

def main():
    token = CONFIG["BOT_TOKEN"]
    if token == "YOUR_QUANTAI_BOT_TOKEN":
        print("❌ 请先在 CONFIG 中填写 BOT_TOKEN 和 GROQ_API_KEY")
        return

    app = Application.builder().token(token).build()

    # 命令
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("plan", cmd_plan))
    app.add_handler(CommandHandler("contact", cmd_contact))
    app.add_handler(CommandHandler("clear", cmd_clear))

    # 回调按钮
    app.add_handler(CallbackQueryHandler(on_callback))

    # 私聊消息
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_message))

    # 设置 Bot 命令菜单
    async def post_init(app):
        await app.bot.set_my_commands([
            BotCommand("start", "开始 / 欢迎菜单"),
            BotCommand("plan", "查看套餐价格"),
            BotCommand("contact", "联系人工客服"),
            BotCommand("clear", "清除对话历史"),
            BotCommand("help", "帮助"),
        ])

    app.post_init = post_init

    print("✅ QuantAI 客服 Bot 启动中...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
