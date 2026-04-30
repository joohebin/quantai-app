# QuantAI × OpenClaw — 交接文档
> 生成时间：2026-04-19 18:25 | 负责人：蒜蓉 🧄

---

## 一、核心信息汇总

### AWS 伦敦服务器（主服务器）
| 项目 | 值 |
|------|-----|
| IP | `35.179.161.45` |
| SSH 密钥 | `C:\Users\Administrator\.ssh\quantai-key-london.pem` |
| 区域 | eu-west-2 (伦敦) |
| 实例 ID | `i-079002e614453ec04` |
| SSH 命令 | `ssh -i C:\Users\Administrator\.ssh\quantai-key-london.pem ubuntu@35.179.161.45` |
| 部署路径 | `/home/ubuntu/quantai-app/` |
| 前端 | http://35.179.161.45:8080/ |
| 后端 API | http://35.179.161.45:8001 |
| API Docs | http://35.179.161.45:8001/docs |

### OpenClaw Gateway
| 项目 | 值 |
|------|-----|
| 访问地址 | http://35.179.161.45:18789 |
| 配置文件 | `~/.openclaw/openclaw.json` |
| 日志 | `/tmp/openclaw/openclaw-YYYY-MM-DD.log` |
| Gateway token | `83e570091be2757b7c9faf842c3be56864fb8b778f44785f` |
| 当前状态 | ✅ 运行中 (PID: 需执行 `ps aux \| grep openclaw-gateway` 查看) |
| DeepSeek API Key | `sk-eb727437f0b64b0b8fbb3b8fb4554cc5` |
| DeepSeek 模型 | `deepseek/deepseek-chat` (via OpenClaw deepseek 插件) |
| EBS 存储 | 100GB gp3，挂载 `/data` |

### 其他 API Keys
| 服务 | Key |
|------|-----|
| DeepSeek API | `sk-eb727437f0b64b0b8fbb3b8fb4554cc5` |
| Groq API (客服 Widget) | `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` |
| Telegram Bot Token | `8226286731:AAHjjcN3pFgUkMEnIxbHWJ8T2HR7_m6CHZs` |
| Telegram Admin ID | `6665770176` |

### 启动脚本
```bash
# 启动 OpenClaw Gateway（已配置开机自启）
nohup openclaw gateway > /tmp/openclaw.log 2>&1 &

# 启动 QuantAI 后端
cd /home/ubuntu/quantai-app && ./start.sh

# 查看状态
curl -s http://localhost:18789/health
```

---

## 二、OpenClaw Skills 安装情况（2026-04-19）

### ✅ 已安装
| 技能 | 来源 | 用途 |
|------|------|------|
| `quantitative-research` | `omer-metin/skills-for-antigravity@quantitative-research` | 量化研究方法论、回测陷阱、因子验证 |
| `tradingview-quantitative` | `hypier/tradingview-quantitative-skills@tradingview-quantitative` | TradingView 数据分析（⚠️ Critical Risk 安全警告） |

### ⬜ 未安装但可用
```bash
# 安装命令
npx skills add <source>@<skill-name> -g -y

# 推荐备选技能
npx skills add hypier/hft-quant-expert@hft-quant-expert -g -y  # 高频量化（暂未找到正确包名）
npx skills add omer-metin/skills-for-antigravity@quantitative-research -g -y  # 已装
```

### ⚠️ 已知问题
- `tradingview-quantitative` 有 **Critical Risk** 安全警告（Gen 扫描），使用前建议审查源码
- `hft-quant-expert` 在 ClawHub 上找不到，GitHub 拉取失败

---

## 三、OpenClaw 正确配置方法（踩坑总结）

### ❌ 错误方式
- ❌ 用 `openai` provider + `baseUrl` → 返回 404
- ❌ 只填 `apiKey` 不填 `baseUrl/models` → 配置验证失败

### ✅ 正确方式
1. 用 `openclaw onboard --mode local --auth-choice deepseek-api-key --deepseek-api-key '<KEY>' --accept-risk --non-interactive` 自动配置
2. 或手动配置 `models.providers.deepseek`（参考 onboard 生成的格式）
3. Agent model 格式：`deepseek/deepseek-chat`（provider/model）

### 当前正确配置参考（`~/.openclaw/openclaw.json`）
```json
{
  "gateway": {
    "bind": "lan",
    "mode": "local",
    "port": 18789,
    "auth": {
      "mode": "token",
      "token": "83e570091be2757b7c9faf842c3be56864fb8b778f44785f"
    }
  },
  "models": {
    "mode": "merge",
    "providers": {
      "deepseek": {
        "baseUrl": "https://api.deepseek.com",
        "apiKey": "<DEEPSEEK_API_KEY>",
        "api": "openai-completions",
        "models": [
          {"id": "deepseek-chat", "name": "DeepSeek Chat", ...},
          {"id": "deepseek-reasoner", "name": "DeepSeek Reasoner", ...}
        ]
      }
    }
  },
  "agents": {
    "list": [
      {"id": "main", "model": "deepseek/deepseek-chat"}
    ]
  }
}
```

### Gateway 操作命令
```bash
# 查看状态
curl -s http://localhost:18789/health

# 重启 Gateway
kill $(ps aux | grep openclaw-gateway | grep -v grep | awk '{print $2}')
nohup openclaw gateway > /tmp/openclaw.log 2>&1 &
sleep 6
curl -s http://localhost:18789/health

# 测试 Agent
openclaw agent --agent main --message 'say hello'

# 测试 Skills
openclaw agent --agent main --message '用 quantitative-research 的方法告诉我什么是 alpha factor'

# 查看日志
tail -100 /tmp/openclaw/openclaw-2026-04-19.log

# 强制更新 config token（如果需要）
openclaw config set gateway.remote.token '<token>'
```

---

## 四、QuantAI 前端对接 OpenClaw 方案

### 方案 A：通过 CodeBuddy 间接调用（当前方案）✅
- 蒜蓉（CodeBuddy AI）SSH 到服务器执行 `openclaw agent` 命令
- 结果返回给用户
- **优点**：安全（用户才能操作），无额外开发量
- **缺点**：需要人工触发，不能自动执行

### 方案 B：QuantAI 后端路由 → OpenClaw CLI（推荐）
在 QuantAI 后端 `backend/routers/ai_trading.py` 或新建 `backend/routers/openclaw.py`：
```python
@router.post("/api/openclaw/chat")
async def openclaw_chat(message: str):
    result = subprocess.run(
        ["openclaw", "agent", "--agent", "main", "--message", message],
        capture_output=True, text=True, timeout=60
    )
    return {"response": result.stdout, "error": result.stderr}
```

### 方案 C：Webhook / MCP（高级，需额外开发）
通过 OpenClaw 的 ACP (Agent Control Protocol) 接入，详见 https://docs.openclaw.ai/

---

## 五、Github 仓库与部署

### 当前仓库
```bash
cd /home/ubuntu/quantai-app && git remote -v
# 查看当前 remote 地址（需在服务器上执行）
```

### 部署流程
```bash
# 1. 拉取最新代码
cd /home/ubuntu/quantai-app && git pull

# 2. 重启后端
./start.sh

# 3. 重启 OpenClaw（如需要）
pkill -f openclaw-gateway
nohup openclaw gateway > /tmp/openclaw.log 2>&1 &
```

---

## 六、测试账号
| 平台 | 账号 | 密码 |
|------|------|------|
| QuantAI App | joohebin220@gmail.com | Kc530220@ |
| Telegram Bot | @tg_support_bot | — |

---

## 七、AutoClaw 后续任务建议

### 高优先级
1. **OpenClaw Gateway 自启动配置** — 写 systemd service，确保服务器重启后自动拉起
2. **OpenClaw 后端路由对接** — 在 QuantAI 后端接入 OpenClaw CLI，让 AI Chat Tab 直接调用
3. **Telegram Bot 问题排查** — 网络连接超时，无法访问 Telegram API

### 中优先级
4. **量化策略模块完善** — 结合 `quantitative-research` skill 实现策略回测对话
5. **安全审查** — `tradingview-quantitative` 有 Critical Risk，需审查后决定是否保留

### 低优先级
6. **tradingview-quantitative 安全审计** — 审查源码，确认无恶意代码
7. **hft-quant-expert** — 确认正确包名并安装
8. **OpenClaw 更新** — 当前 v2026.4.14，v2026.4.15 已发布（需 sudo）

---

## 八、文件路径速查

| 用途 | 路径 |
|------|------|
| OpenClaw 配置 | `/home/ubuntu/.openclaw/openclaw.json` |
| OpenClaw 日志 | `/tmp/openclaw/openclaw-YYYY-MM-DD.log` |
| OpenClaw Skills | `~/.agents/skills/` |
| OpenClaw Workspace | `~/.openclaw/workspace/` |
| 知识库 | `/data/openclaw/knowledge/QUANTAI_KB.md` |
| QuantAI 后端 | `/home/ubuntu/quantai-app/backend/` |
| QuantAI 前端 | `/home/ubuntu/quantai-app/index.html` |
| EBS 存储 | `/data` |

---

*文档由蒜蓉 🧄 整理，如有问题请查阅对应 memory 文件*
