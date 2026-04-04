# MEMORY.md — QuantAI Project Long-Term Memory

## Project Overview
- **Project**: QuantAI — AI-powered trading platform
- **Domain**: quantai.app
- **Sister Brand**: KITOKITO (kitokito-eth.com) — cyberpunk lifestyle store
- **Style**: Cyberpunk/tech dark theme (bg:#030712, cyan:#00f5ff, purple:#a000ff)

## Website (landing/)
- `preview.html` — Main landing page, cyberpunk style
- Language count: **17 languages** (zh, en, zh-tw, ja, ko, yue, de, fr, es, pt, ru, ar, hi, ms, id, vi, th)
- Language dropdown in nav works (UI only, content not yet translated)
- Nav links have smooth scroll anchor (#features, #pricing, #hero)

## Legal/Compliance Documents (landing/)
- `privacy-policy.html` — Privacy Policy
- `terms-of-service.html` — Terms of Service  
- `cookie-policy.html` — Cookie Policy
- `community-guidelines.html` — Community Guidelines
- All linked from both landing page footer and App "My Account" settings
- i18n keys added for all 6 app languages (zh, en, ja, ko, ru, ar)

## App (index.html)
- Main app is a single-page HTML with multi-tab navigation
- i18n built-in with 6 languages (zh, en, ja, ko, ru, ar)
- Legal docs section added under "My Account" → between AI Config and Trading Log
- Key modules: Dashboard, Market, AI Chat, Positions, Strategies, Backtest, Account, Copy Trading, Auto Open, Trading Square, Strategy Market, Signal Broadcast

## User Preferences
- User is based in 大连, does cross-border e-commerce
- Prefers direct, no-nonsense communication
- Predefined email addresses for legal: privacy@quantai.app, legal@quantai.app, report@quantai.app

## Systems & Automation
- TG Bot (tg_support_bot.py)：QuantAI客服Telegram Bot
- 自动化配置：每小时检查TG Bot运行状态
- 当前问题：网络连接超时，无法连接到Telegram API
- Bot Token：8226286731:AAHjjcN3pFgUkMEnIxbHWJ8T2HR7_m6CHZs
- Admin ID：6665770176
