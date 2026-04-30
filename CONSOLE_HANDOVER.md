# QuantAI 运营中控台 交接文档

> 交接日期：2026-04-30  
> 关联项目：QuantAI 量化交易平台

---

## 一、中控台概述

**console.html** - QuantAI内部运营管理控制台，用于管理员监控平台运行状态、管理用户、查看交易数据等。

### 访问地址
```
http://35.179.161.45:8080/console.html
```

### 文件信息
| 项目 | 信息 |
|------|------|
| **文件名** | console.html |
| **大小** | ~103KB |
| **本地路径** | c:\Users\Administrator\WorkBuddy\Claw\quantai-app\console.html |
| **服务器路径** | /home/ubuntu/quantai-app/console.html |
| **最后修改** | 2026-04-22 |

---

## 二、功能模块

### 1. 登录认证
- **路径**：`/#/login`
- **功能**：管理员账号登录
- **API**：`POST /api/auth/login`
- **说明**：使用与主应用相同的认证体系

### 2. 仪表盘概览
- **路径**：`/#/dashboard`
- **功能**：
  - 平台用户统计（总用户数、新增用户、活跃用户）
  - 交易数据统计（总订单数、总交易额、盈亏统计）
  - 系统健康状态（服务状态、API响应时间）
  - 实时资金监控

### 3. 用户管理
- **路径**：`/#/users`
- **功能**：
  - 用户列表查看
  - 用户详情（账户信息、交易历史、持仓情况）
  - 子账户管理
  - 用户状态管理（启用/禁用）

**API端点**：
```
GET  /api/admin/users          # 用户列表
GET  /api/admin/users/stats    # 用户统计
POST /api/admin/subaccount     # 创建子账户
GET  /api/admin/subaccounts    # 子账户列表
```

### 4. 订单管理
- **路径**：`/#/orders`
- **功能**：
  - 全平台订单列表
  - 订单状态筛选
  - 订单详情查看
  - 异常订单处理

**API端点**：
```
GET /api/orders/?limit={n}     # 订单列表
```

### 5. 券商/经纪商管理
- **路径**：`/#/brokers`
- **功能**：
  - MetaApi配置管理
  - API2Trade连接状态
  - 券商账户列表
  - 连接测试

**API端点**：
```
GET  /api/brokers/                    # 券商列表
GET  /api/admin/brokers/all           # 所有券商（管理员）
GET  /api/brokers/status              # 连接状态
POST /api/brokers/metaapi/save-config # 保存MetaApi配置
POST /api/api2trade/connect           # 连接API2Trade
GET  /api/api2trade/status            # API2Trade状态
GET  /api/api2trade/accounts          # API2Trade账户列表
```

### 6. 套利监控
- **路径**：`/#/arbitrage`
- **功能**：
  - 跨交易所价格监控
  - 套利机会实时展示
  - 价差图表

**API端点**：
```
GET /api/arbitrage/prices/{symbol}    # 获取品种套利价格
```

### 7. 交易统计
- **路径**：`/#/stats`
- **功能**：
  - 交易量统计
  - 盈亏分析
  - 策略绩效排名

**API端点**：
```
GET /api/trading-stats/summary        # 交易统计摘要
```

### 8. 系统设置
- **路径**：`/#/settings`
- **功能**：
  - 服务配置（后端API地址、端口）
  - 通知设置
  - 日志查看

---

## 三、技术配置

### API基础地址
```javascript
const API_BASE = 'http://35.179.161.45:8001';
```

**注意**：当前硬编码为伦敦服务器地址，如需修改请编辑第1495行。

### 默认服务配置
```javascript
{
  backendUrl: '35.179.161.45',
  servicePort: '8001'
}
```

---

## 四、后端API依赖

中控台依赖以下后端API端点：

### 认证相关
| 端点 | 方法 | 说明 |
|------|------|------|
| /api/auth/login | POST | 管理员登录 |
| /api/auth/register | POST | 注册（如有需要） |

### 用户管理
| 端点 | 方法 | 说明 |
|------|------|------|
| /api/admin/users | GET | 用户列表 |
| /api/admin/users/stats | GET | 用户统计 |
| /api/admin/subaccounts | GET | 子账户列表 |
| /api/admin/subaccount | POST | 创建子账户 |

### 交易数据
| 端点 | 方法 | 说明 |
|------|------|------|
| /api/orders/ | GET | 订单列表 |
| /api/trading-stats/summary | GET | 交易统计 |
| /api/arbitrage/prices/{symbol} | GET | 套利价格 |

### 券商管理
| 端点 | 方法 | 说明 |
|------|------|------|
| /api/brokers/ | GET | 券商列表 |
| /api/admin/brokers/all | GET | 所有券商 |
| /api/brokers/status | GET | 连接状态 |
| /api/brokers/metaapi/save-config | POST | 保存配置 |
| /api/api2trade/connect | POST | 连接API2Trade |
| /api/api2trade/status | GET | API2Trade状态 |
| /api/api2trade/accounts | GET | 账户列表 |

---

## 五、部署与访问

### 当前部署状态
- **服务器**：AWS伦敦 (35.179.161.45)
- **访问地址**：http://35.179.161.45:8080/console.html
- **状态**：✅ 可正常访问 (HTTP 200)

### 部署方式
console.html与主应用index.html部署在同一目录，由Python HTTP服务器统一提供：
```bash
cd ~/quantai-app
python3 -m http.server 8080
```

### 文件同步
如需更新中控台：
```bash
# 从本地Windows
scp -i ~/.ssh/quantai-key-london.pem console.html ubuntu@35.179.161.45:quantai-app/
```

---

## 六、已知限制

1. **单页面应用**：使用hash路由（/#/path），刷新页面需重新登录
2. **无持久化存储**：配置存储在内存中，刷新后重置
3. **硬编码API地址**：当前写死为35.179.161.45:8001
4. **无权限细分**：所有管理员看到相同内容

---

## 七、后续优化建议

1. **配置持久化** - 将服务配置保存到localStorage
2. **API地址可配置** - 提供UI修改后端API地址
3. **权限管理** - 区分超级管理员/运营人员权限
4. **实时监控** - WebSocket连接实时推送数据
5. **操作日志** - 记录管理员操作历史
6. **数据导出** - 支持Excel/CSV导出用户/订单数据

---

## 八、相关文件

| 文件 | 路径 | 说明 |
|------|------|------|
| console.html | /quantai-app/console.html | 中控台主体 |
| index.html | /quantai-app/index.html | 主应用前端 |
| backend/main.py | /quantai-app/backend/main.py | 后端API入口 |
| backend/routers/users.py | /quantai-app/backend/routers/users.py | 用户管理API |
| backend/routers/orders.py | /quantai-app/backend/routers/orders.py | 订单管理API |
| backend/routers/broker.py | /quantai-app/backend/routers/broker.py | 券商管理API |

---

**文档版本**：v1.0  
**最后更新**：2026-04-30
