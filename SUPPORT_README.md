# QuantAI 客服系统 · 使用说明

## 一、文件清单

| 文件 | 说明 |
|------|------|
| `SUPPORT_KB.md` | 产品知识库（29条 FAQ + 客服规范），供 Groq Bot 作为 system prompt |
| `index.html` | 主应用（内嵌了右下角客服 Widget） |
| `tg_support_bot.py` | Telegram 客服 Bot（独立部署） |

---

## 二、App 内嵌客服 Widget

**已内置在 index.html，无需额外操作。**

### 功能
- 右下角 💬 悬浮按钮（3秒后显示红点提示）
- 点击展开聊天框，支持快捷问题按钮
- **离线模式**：本地知识库关键词匹配（无需 API Key）
- **在线模式**：接入 Groq AI（填写 API Key 后自动启用）
- **转人工**：检测关键词（"转人工"/"human"等）→ 弹出 Telegram 链接

### 配置 Groq API Key（可选，免费注册）

在 `index.html` 搜索 `CS_CONFIG`，填入 Key：

```javascript
const CS_CONFIG = {
  groqKey: 'gsk_xxxxxxxxxxxxxxxxxx',  // ← 填这里
  tgLink: 'https://t.me/你的客服Bot',   // ← 改成你的 TG Bot 链接
  ...
};
```

Groq 注册：https://console.groq.com（免费，llama-3.3-70b）

---

## 三、Telegram 客服 Bot

### 安装依赖

```bash
pip install groq python-telegram-bot
```

### 配置

编辑 `tg_support_bot.py` 顶部 CONFIG：

```python
CONFIG = {
    "BOT_TOKEN": "从 @BotFather 创建 Bot 后获取",
    "GROQ_API_KEY": "gsk_你的Key",
    "ADMIN_CHAT_ID": 你的TG数字ID,  # @userinfobot 可查询
    ...
}
```

### 运行

```bash
cd quantai-app
python tg_support_bot.py
```

### Bot 功能

| 命令 | 作用 |
|------|------|
| `/start` | 欢迎菜单 + 快捷按钮 |
| `/plan` | 显示套餐价格 |
| `/contact` | 直接转人工 |
| `/clear` | 清除对话历史 |
| `/help` | 帮助列表 |

### 转人工流程

```
用户说"转人工" / "human" / 点击转人工按钮
         ↓
你的 Telegram 收到通知（含用户名+触发内容）
         ↓
你直接回复那条通知消息
         ↓
Bot 自动将你的回复转发给用户
```

---

## 四、客服规范（速览）

1. **引导到功能**：告知用户在哪个页面/按钮操作
2. **语言匹配**：用户用什么语言发来就用什么语言回
3. **转人工条件**：支付问题 / 账号安全 / 数据异常
4. **升级引导**：温和引导，不强推

详细 FAQ 见 `SUPPORT_KB.md`。

---

## 五、三层客服架构

```
用户提问
  ↓
[Layer 1] App 内嵌 Widget（即时）
  本地知识库匹配 → Groq AI回复 → 转人工按钮
  ↓（点击转人工）
[Layer 2] Telegram Bot（自动 + 转接）
  Groq AI多轮对话 → 检测转人工关键词 → 通知老板
  ↓（老板回复通知）
[Layer 3] 人工客服（你）
  在 Telegram 直接回复，Bot 自动转发给用户
```

---

*最后更新：2026-03-30*
