# QuantAI 项目交接文档

> 交接日期：2026-04-30  
> 交接人：蒜蓉 → OpenClaw  

---

## 一、项目概述

**QuantAI** - AI驱动的量化交易平台，包含Web前端、后端API、TG客服Bot。

### 核心功能模块
1. **仪表盘** - 资产概览、实时行情、盈亏统计
2. **行情中心** - K线图表（LightweightCharts）、多数据源（Binance/Yahoo Finance）
3. **AI顾问** - 智能交易建议（DeepSeek模型）
4. **持仓管理** - 仓位追踪、盈亏计算
5. **策略中心** - 策略创建、回测、复制交易
6. **自动建仓** - 条件单、自动开仓
7. **跨交易所聚合引擎** - 套利监控（arb_相关功能）
8. **账户系统** - JWT认证、多语言支持（18种语言）

---

## 二、技术架构

### 前端
- **技术栈**：纯HTML/CSS/JS单页应用（无框架）
- **图表库**：LightweightCharts v5
- **主题**：Cyberpunk暗色风格（bg:#030712, cyan:#00f5ff, purple:#a000ff）
- **i18n**：原生实现，18种语言（zh, en, zh-tw, yue, ja, ko, de, fr, es, pt, ru, ar, hi, ms, id, vi, th, tr）
- **文件**：`index.html`（单文件，~680KB）

### 后端
- **框架**：FastAPI (Python)
- **数据库**：SQLite (`backend/quantai.db`)
- **认证**：JWT (PyJWT)
- **API文档**：自动Swagger UI
- **MT4/MT5对接**：
  - API2Trade（主用，INFINOX实时账户）
  - MetaApi（备用）

### AI层
- **模型**：DeepSeek `deepseek-chat`（全部统一使用）
- **Gateway**：OpenClaw（端口18789）
- **知识库**：`/data/openclaw/knowledge/` 目录

---

## 三、服务器信息

### AWS 伦敦主服务器（唯一在用）
| 项目 | 信息 |
|------|------|
| **IP** | 35.179.161.45 |
| **区域** | eu-west-2 |
| **SSH Key** | `quantai-key-london.pem` |
| **用户** | ubuntu |

#### 服务端口
| 服务 | 端口 | 状态 |
|------|------|------|
| 前端HTTP | 8080 | Python http.server |
| 后端API | 8001 | FastAPI (uvicorn) |
| OpenClaw Gateway | 18789 | openclaw-gateway |

#### 部署路径
```
/home/ubuntu/quantai-app/
├── index.html          # 前端
├── backend/            # 后端代码
│   ├── main.py
│   ├── auth.py
│   ├── models.py
│   ├── schemas.py
│   ├── quantai.db      # SQLite数据库
│   └── routers/        # API路由
│       ├── ai_trading.py
│       ├── broker.py
│       ├── market.py
│       ├── orders.py
│       ├── positions.py
│       ├── strategies.py
│       └── users.py
├── start.sh            # 启动脚本
└── frontend.log        # 前端日志
```

#### OpenClaw配置
```
~/.openclaw/openclaw.json
/data/openclaw/knowledge/   # 知识库目录
```

### AWS 其他区域（保留待扩展）
| 区域 | IP | 状态 |
|------|-----|------|
| 新加坡 | 54.151.143.233 | ❌ MetaApi被封锁 |
| 美国 | 3.234.241.57 | ❌ MetaApi被封锁 |

---

## 四、GitHub仓库

### 仓库地址
```
https://github.com/joohebin220/quantai-app
```

### 本地路径
```
c:\Users\Administrator\WorkBuddy\Claw\quantai-app
```

### 分支
- `main` - 主分支

### 关键文件
```
quantai-app/
├── index.html              # 前端（单文件应用）
├── backend/                # 后端
│   ├── main.py            # FastAPI入口
│   ├── auth.py            # JWT认证
│   ├── models.py          # SQLAlchemy模型
│   ├── schemas.py         # Pydantic模型
│   ├── api2trade.py       # API2Trade对接
│   └── routers/           # API路由
├── console.html           # 管理控制台
└── .workbuddy/memory/     # 工作记忆
    └── MEMORY.md          # 项目长期记忆
```

---

## 五、关键配置信息

### DeepSeek API
```
Key: sk-6fd3a4a562e14d7d8885f74d44b2b730
模型: deepseek-chat
```

### OpenClaw Gateway
```
版本: 2026.4.14
端口: 18789
Token: 83e570091be2757b7c9faf842c3be56864fb8b778f44785f
模型: deepseek/deepseek-chat
```

### API2Trade（MT5对接）
```
API Key: a915ec00-8a72-4df2-9fc1-1caf13d6b6e2
API URL: https://api.metatraderapi.dev
账户UUID: ff982e56-23b0-4e3d-b6f6-7f7b8c40679e
MT5账号: 87954362
券商: INFINOX
服务器: InfinoxLimited-MT5Live
```

### MetaApi（备用）
```
账户ID: 3791ec3f-4ef6-493f-b460-4cdbc40e33e4
MT5账号: MT5-87954362N
服务器: london.agiliumtrade.ai
注意: SSL需verify=False
```

### TG Bot
```
Bot: @QuantAI_CS_bot
Token: 8226286731:AAHjjcN3pFgUkMEnIxbHWJ8T2HR7_m6CHZs
Admin: 6665770176
模式: 白名单
本地脚本: tg_support_bot.py（Windows运行）
```

### 测试账号
```
邮箱: joohebin220@gmail.com
密码: Kc530220@
```

---

## 六、AI自动量化交易逻辑

### 当前实现

#### 1. AI顾问模块 (`backend/routers/ai_trading.py`)
- 接收用户交易问题
- 调用DeepSeek模型分析
- 返回交易建议（买入/卖出/持仓）
- 支持多轮对话上下文

#### 2. 自动建仓逻辑
- 条件单设置（价格触发、指标触发）
- 定时检查条件
- 满足条件时调用API2Trade下单

#### 3. 策略回测
- 历史数据回测
- 策略性能评估
- 可视化回测结果

### 待实现/优化方向

#### 1. 实时信号系统
- 技术指标实时监控（MA交叉、RSI超买超卖等）
- 多时间框架信号聚合
- 信号置信度评分

#### 2. 智能仓位管理
- 基于风险偏好的仓位计算
- 凯利公式/固定比例仓位
- 多品种资金分配

#### 3. 风控系统
- 最大回撤控制
- 单笔亏损限制
- 每日/每周止损线

#### 4. 策略市场
- 策略分享/订阅
- 信号复制交易
- 策略绩效排名

#### 5. 机器学习增强
- 价格预测模型
- 情绪分析（新闻/社交媒体）
- 异常检测（闪崩预警）

---

## 七、已知问题与注意事项

### 已修复问题
1. ✅ JWT `sub` 必须是字符串（backend/auth.py）
2. ✅ i18n 翻译对象语法错误（多余的 `},`）
3. ✅ Python HTTP服务器偶发卡死（已重启）

### 注意事项
1. **Groq已弃用** - AWS伦敦IP被Cloudflare 403封锁，全部改用DeepSeek
2. **MetaApi限制** - 新加坡/美国服务器被MetaApi封锁，只能用伦敦
3. **API2Trade Positions端点** - 返回"path not valid"，可能需要PRO套餐
4. **前端单文件** - index.html ~680KB，注意浏览器加载性能

---

## 八、常用命令

### SSH登录
```bash
ssh -i ~/.ssh/quantai-key-london.pem ubuntu@35.179.161.45
```

### 重启前端服务
```bash
# 在服务器上执行
pkill -f 'http.server 8080'
cd ~/quantai-app && nohup python3 -m http.server 8080 > frontend.log 2>&1 &
```

### 重启后端服务
```bash
cd ~/quantai-app/backend
pkill -f 'uvicorn main:app'
nohup uvicorn main:app --host 0.0.0.0 --port 8001 > backend.log 2>&1 &
```

### 检查服务状态
```bash
ps aux | grep -E 'http.server|uvicorn|openclaw'
netstat -tlnp | grep -E '8080|8001|18789'
```

### 同步文件到服务器
```bash
# 从本地Windows
scp -i ~/.ssh/quantai-key-london.pem index.html ubuntu@35.179.161.45:quantai-app/
```

---

## 九、OpenClaw知识库

路径：`/data/openclaw/knowledge/`

### 现有文件
- `_QUANTAI_KB.md` - 完整平台知识
- `ops-manual.md` - SSH/服务/API/CLI操作手册
- `troubleshooting.md` - 故障排查
- `faq.md` - 常见问题
- `platform-info.md` - 平台介绍
- `pricing.md` - 定价信息
- `trading-basics.md` - 交易基础

### 建议补充
- `ai-trading-logic.md` - AI交易逻辑详细说明
- `api-reference.md` - 后端API完整文档
- `deployment-guide.md` - 部署流程文档

---

## 十、联系方式

| 类型 | 地址 |
|------|------|
| 隐私政策 | privacy@quantai.app |
| 法律事务 | legal@quantai.app |
| 违规举报 | report@quantai.app |

---

## 十一、后续建议

1. **监控告警** - 建议设置服务状态监控（前端/后端/API响应）
2. **日志聚合** - 考虑使用ELK或类似方案集中管理日志
3. **数据库迁移** - 用户量增长后考虑从SQLite迁移到PostgreSQL
4. **CI/CD** - 建议配置GitHub Actions自动部署
5. **测试覆盖** - 补充单元测试和集成测试
6. **文档完善** - API文档、部署文档、用户手册

---

**文档版本**：v1.0  
**最后更新**：2026-04-30
