# QuantAI 模型微调流程设计

## 目标
让AI通过用户数据不断进化，实现真正的"越用越聪明"

---

## 整体架构

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       QuantAI 数据飞轮系统                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  用户 ──▶ AI分析 ──▶ 信号 ──▶ 执行 ──▶ 结果 ──▶ 数据积累 ──▶ 微调 ──▶ 新模型 │
│                │           │         │           │           │              │
│                ▼           ▼         ▼           ▼           ▼              │
│           实时记录    存入DB    用户反馈   更新结果    导出训练数据    部署上线 │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 阶段一：数据收集（已实现 ✅）

### AISignal 数据结构
```
- id: 唯一ID
- user_id: 用户ID
- signal_type: "buy" | "sell" | "hold" | "follow"
- symbol: 交易标的
- amount: 数量
- reason: AI给出的原因
- market_snapshot: 当时的市场价格快照 {}
- executed: 是否执行
- execution_result: "success" | "cancelled" | "failed"
- pnl_result: 实盘盈亏金额
- source: "ai_advisor" | "copy_trading" | "arbitrage"
- created_at: 信号产生时间
- result_updated_at: 结果更新时间
```

---

## 阶段二：数据清洗与标注

### 规则1：自动标注
```python
def auto_label(signal):
    """自动标注信号质量"""
    
    # 规则1：盈利 = 成功信号
    if signal.pnl_result > 0:
        return "positive"  # 好信号，用于训练
    
    # 规则2：亏损 < -5% = 负面信号
    if signal.pnl_result < -5:
        return "negative"  # 坏信号，权重降低
    
    # 规则3：未执行或持平 = 中性
    return "neutral"
```

### 规则2：数据清洗
```python
def clean_data(signals):
    """清洗数据"""
    
    # 过滤1：必须有市场快照
    signals = [s for s in signals if s.market_snapshot]
    
    # 过滤2：必须是已执行的信号
    signals = [s for s in signals if s.executed]
    
    # 过滤3：结果已更新（至少24小时有结果）
    signals = [s for s in signals if s.result_updated_at]
    
    # 过滤4：排除异常数据
    signals = [s for s in signals if -1000 < s.pnl_result < 1000]
    
    return signals
```

### 规则3：训练数据格式（JSONL）
```json
{"messages": [
  {"role": "system", "content": "你是QuantAI量化交易助手"},
  {"role": "user", "content": "BTC价格65000 ETH价格3500 分析市场"},
  {"role": "assistant", "content": "{\"action\": \"buy\", \"symbol\": \"BTC/USDT\", \"amount\": 0.1, \"reason\": \"BTC突破阻力位\"}"}
]}
```

---

## 阶段三：微调训练

### 选项A：OpenRouter Fine-tuning（推荐）

**费用**：$0.4/1M tokens（比从头训练便宜很多）
- 需要先将数据上传到 OpenRouter
- 指定基础模型 deepseek/deepseek-chat
- 生成专属微调版本

**流程**：
```
1. 导出信号数据为训练格式
2. 上传到 OpenRouter
3. 发起微调任务
4. 等待训练完成（约30分钟）
5. 获取新模型ID
```

### 选项B：AWS SageMaker（备选）

- 使用SageMaker JumpStart基础模型
- 自定义训练数据
- 费用：约$2/小时（GPU实例）

### 选项C：本地微调（成本最低）

- 使用LoRA轻量微调
- 需要GPU服务器
- 成本：电费+硬件

---

## 阶段四：A/B测试

### 测试设计
```python
def ab_test(new_model_id, old_model_id, test_users):
    """A/B测试"""
    
    # 50%用户用新模型，50%用旧模型
    group_a = test_users[:len(test_users)//2]  # 新模型
    group_b = test_users[len(test_users)//2:]  # 旧模型
    
    # 收集7天数据
    results = {
        "group_a": {"win_rate": 0, "avg_pnl": 0, "signals": 0},
        "group_b": {"win_rate": 0, "avg_pnl": 0, "signals": 0}
    }
    
    # 比较胜率
    if results["group_a"]["win_rate"] > results["group_b"]["win_rate"] + 5:
        return "new_model_wins"
    return "keep_old_model"
```

---

## 阶段五：部署上线

### 灰度发布
```
Day 1-2: 5%用户更新
Day 3-4: 20%用户更新  
Day 5-7: 100%用户更新
```

### 回滚机制
```
- 监控胜率下降 > 10%
- 触发自动回滚
- 发送告警通知
```

---

## API 设计

### 管理后台接口
```
GET  /api/admin/ai-signals/export?min_signals=100&source=ai_advisor
    → 导出指定条件的训练数据

POST /api/admin/ai-finetune/start
    → 发起微调任务
    
GET /api/admin/ai-finetune/status
    → 查看微调状态
    
POST /api/admin/ai-finetune/deploy/{version}
    → 部署指定版本
    
POST /api/admin/ai-finetune/rollback
    → 回滚到上一版本
```

### 统计面板
```
GET  /api/admin/ai-stats
    → 信号总数、执行率、胜率、趋势图
```

---

## 技术栈

| 组件 | 实现 |
|------|------|
| 数据存储 | SQLite (当前) → PostgreSQL (数据量大时) |
| 微调服务 | OpenRouter Fine-tuning |
| 模型版本管理 | 数据库表 + 配置文件 |
| 监控告警 | CloudWatch / 日志 |

---

## 实施路线图

```
Week 1: 数据收集（已实现）
Week 2: 导出脚本 + 清洗规则
Week 3: OpenRouter 微调测试
Week 4: A/B测试 + 部署
Week 5+: 持续迭代优化
```

---

## 关键决策点

1. **微调预算**：预计$50-100/月（取决于数据量）
2. **模型选择**：继续用 DeepSeek 还是换其他模型？
3. **更新频率**：每周？每月？
4. **失败处理**：微调失败后的回退方案

---

## 待确认事项

- [x] 数据收集流程
- [ ] 是否使用 OpenRouter 微调服务？
- [ ] 微调预算范围？
- [ ] 数据量达到多少开始第一次微调？（建议100+条）