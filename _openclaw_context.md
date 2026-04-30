# QuantAI 运营上下文 (Operations Context)

> 此文件包含 QuantAI 项目全部技术/运营信息，每次任务执行前请先读取。

## 1. 项目文件位置

| 环境 | 路径 |
|------|------|
| **Windows 本地开发** | `C:\Users\Administrator\WorkBuddy\Claw\quantai-app\` |
| **AWS 生产服务器** | `/home/ubuntu/quantai-app/` |

### AWS 生产目录结构
```
/home/ubuntu/quantai-app/
├── index.html          # 主应用 (18语言i18n)
├── console.html        # 运营中控台
├── mobile-app/www/     # 移动端 (18语言)
├── landing/            # 落地页
├── backend/            # FastAPI后端
│   ├── main.py
│   ├── auth.py
│   ├── models.py
│   ├── schemas.py
│   ├── quantai.db
│   ├── routers/
│   │   ├── ai_trading.py
│   │   ├── positions.py
│   │   ├── orders.py
│   │   ├── strategies.py
│   │   ├── users.py
│   │   ├── broker.py
│   │   └── market.py
│   └── backend/
│       └── .env          # API Keys 配置
└── tg_support_bot.py    # 旧客服Bot (已停用)
```

---

## 2. AWS 服务器节点

### 伦敦区域 (主服务器 - MetaApi 可用)
| 项目 | 值 |
|------|-----|
| **IP** | `35.179.161.45` |
| **SSH Key** | `quantai-key-london.pem` |
| **SSH 命令** | `ssh -i ~/.ssh/quantai-key-london.pem ubuntu@35.179.161.45` |
| **区域** | eu-west-2 |
| **SSH端口** | 22, 80, 443, 8080, 8001 |
| **前端** | http://35.179.161.45:8080/ |
| **控制台** | http://35.179.161.45:8080/console.html |
| **后端API** | http://35.179.161.45:8001 |
| **API Docs** | http://35.179.161.45:8001/docs |
| **OpenClaw GW** | http://35.179.161.45:18789 |
| **状态** | ✅ 运行中 |

### 新加坡区域 (保留待扩展)
| 项目 | 值 |
|------|-----|
| **IP** | `54.151.143.233` |
| **SSH Key** | `quantai-key.pem` |
| **状态** | ❌ MetaApi 被封锁 |

### 美东区域 (保留待扩展)
| 项目 | 值 |
|------|-----|
| **IP** | `3.234.241.57` |
| **SSH Key** | `quantai-key-us.pem` |
| **状态** | ❌ MetaApi 被封锁 |

---

## 3. API Keys 与凭证

### DeepSeek (OpenClaw Gateway 使用)
- **API Key**: `sk-eb727437f0b64b0b8fbb3b8fb4554cc5`
- **存储位置**: `/home/ubuntu/.openclaw/agents/main/agent/auth-profiles.json`
- **用途**: OpenClaw Agent 的默认模型 `deepseek/deepseek-chat`

### OpenRouter (QuantAI 后端 AI Trading 使用)
- **API Key**: `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`
- **Base URL**: `https://openrouter.ai/api/v1`
- **存储位置**: `/home/ubuntu/quantai-app/backend/backend/.env`
- **用途**: 后端 AI 量化交易 (Qwen3 + DeepSeek3.2)

### Groq (客服 Widget 使用)
- **API Key**: `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`
- **模型**: `llama-3.3-70b-versatile`
- **路由端点**: `POST http://35.179.161.45:8001/api/cs/chat`

### Tavily (OpenClaw 联网搜索使用)
- **API Key**: `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`
- **存储位置**: `/home/ubuntu/.openclaw/.env`

### MetaApi (MT5 交易)
| 项目 | 值 |
|------|-----|
| **Token** | `eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9...` (JWT,很长) |
| **Account ID** | `3791ec3f-4ef6-493f-b460-4cdbc40e33e4` |
| **Server** | `INFINOXMT5` |
| **API Base** | `https://mt-client-api-v1.london.agiliumtrade.ai` |
| **WebSocket** | `wss://mt-client-api-v1.london.agiliumtrade.ai` |
| **存储位置** | `/home/ubuntu/quantai-app/backend/backend/.env` |
| **状态** | ✅ 伦敦区域可用 |

---

## 4. OpenClaw Gateway 配置

| 项目 | 值 |
|------|-----|
| **版本** | 2026.4.14 |
| **端口** | 18789 |
| **访问地址** | ws://35.179.161.45:18789 |
| **Gateway Token** | `83e570091be2757b7c9faf842c3be56864fb8b778f44785f` |
| **配置文件** | `/home/ubuntu/.openclaw/openclaw.json` |
| **Agent 模型** | `deepseek/deepseek-chat` |
| **Agent ID** | `main` |
| **日志文件** | `/tmp/openclaw/openclaw-YYYY-MM-DD.log` |
| **Gateway 日志** | `/tmp/openclaw-gw.log` |

### OpenClaw Telegram Bot
| 项目 | 值 |
|------|-----|
| **Bot** | @QuantAI_CS_bot |
| **Bot Token** | `8226286731:AAHjjcN3pFgUkMEnIxbHWJ8T2HR7_m6CHZs` |
| **Admin ID** | `tg:6665770176` |
| **dmPolicy** | `allowlist` (仅白名单用户可用) |
| **状态** | ✅ polling 模式运行中 |

### OpenClaw 已安装 Skills
- `quantitative-research` - 量化研究方法论
- `tradingview-quantitative` - TradingView数据分析
- `Code` (1.0.4) - 编码工作流
- `Self-Improving` (1.2.16) - 自我反思/错误纠正
- `fluid-memory` (1.0.9) - 艾宾浩斯遗忘曲线
- `feishu-toolkit` (1.0.0) - 飞书集成
- `feishu-sheets-skill` (1.0.0) - 飞书表格
- `websearch` (0.1.1) - 多引擎联网搜索
- `skill-vetter` - 安全审计
- `find-skills` - 技能搜索
- `summarize-pro` - 内容总结
- `agent-memory` (1.0.0) - 跨会话记忆
- `agent-browser` - 浏览器自动化
- `tavily-search` - AI优化联网搜索

### OpenClaw Workspace
- **路径**: `/home/ubuntu/.openclaw/workspace/`
- **知识库**: `QUANTAI_KB.md`, `SOUL.md`, `IDENTITY.md`, `USER.md`, `TOOLS.md`
- **策略代码**: `metaapi_trading_system.py`, `ma_cross_backtest.py`, `btc_analysis.py`

---

## 5. QuantAI 后端 API

| 端点 | 说明 |
|------|------|
| `http://35.179.161.45:8001` | 主API |
| `http://35.179.161.45:8001/docs` | Swagger文档 |
| `http://35.179.161.45:8001/api/cs/chat` | 客服Widget (Groq) |
| `http://35.179.161.45:8001/api/positions/` | 持仓查询 |
| `http://35.179.161.45:8001/api/meta/dashboard` | MT5 Equity/Balance |
| `http://35.179.161.45:8001/api/brokers/` | 券商余额 |

---

## 6. GitHub 仓库

| 项目 | 值 |
|------|-----|
| **仓库** | https://github.com/joohebin/quantai-app (推测) |
| **本地无Git凭证** | 需从用户机器操作 |

---

## 7. 用户信息

| 项目 | 值 |
|------|-----|
| **Telegram ID** | `6665770176` |
| **城市** | 大连 |
| **职业** | 跨境电商 + QuantAI 运营 |
| **偏好** | 直接、不废话、实用主义 |

---

## 8. 当前状态

- ✅ OpenClaw Gateway 运行正常 (35.179.161.45:18789)
- ✅ Telegram Bot @QuantAI_CS_bot polling 中
- ✅ DeepSeek 模型可用
- ✅ 伦敦 MetaApi 可用 (INFINOX MT5)
- ❌ 新加坡/美东 MetaApi 不可用
- ⏳ MetaApi 对接待完成
