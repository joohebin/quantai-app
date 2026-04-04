QuantAI HarmonyOS NEXT - ArkTS 开发说明
=========================================

## 文件结构

harmony-app/
├── entry/src/main/
│   ├── ets/
│   │   ├── pages/
│   │   │   ├── Index.ets           ← 主页（TabBar 导航 + 仪表盘）
│   │   │   ├── MarketPage.ets      ← 行情页（分类筛选+列表）
│   │   │   ├── AIAssistantPage.ets ← AI 助手聊天页
│   │   │   └── PositionsPage.ets   ← 持仓页 + 账户设置页
│   │   └── entryability/           ← Ability 入口（标准模板）
│   ├── module.json5                 ← 模块配置 + 权限声明
│   └── resources/

## 开发环境

- **IDE**：DevEco Studio 5.0+（华为官方 IDE）
  下载：https://developer.huawei.com/consumer/cn/deveco-studio/
- **SDK**：HarmonyOS NEXT SDK
- **语言**：ArkTS（TypeScript 超集）
- **UI 框架**：ArkUI 声明式

## 快速开始

1. 下载安装 DevEco Studio 5.0
2. 打开 `quantai-app/harmony-app/` 目录作为项目
3. 连接 HarmonyOS 真机或启动模拟器
4. Run → Run 'entry'

## 已实现页面

| 页面 | 功能 |
|------|------|
| 仪表盘 | 总资产/日盈亏（模拟实时）、快捷操作、AI简报、持仓小卡片 |
| 行情 | 10个品种、分类筛选（全部/加密/外汇/贵金属/能源/指数） |
| AI 助手 | 完整对话流、快速回复、意图识别（分析/下单/持仓/风控） |
| 持仓管理 | 持仓列表、汇总卡片、平仓/AI分析按钮 |
| 账户 | 用户信息、券商连接、风控Toggle开关、退出登录 |

## 技术要点

- ArkTS 声明式 UI（Column/Row/List/Text/Button/Toggle 等基础组件）
- @State 驱动 UI 自动刷新
- setInterval 模拟实时数据跳动
- 深色主题：#0A1628 背景，#00C896 绿色主色
- 底部安全区适配（padding bottom）
- List 组件高效渲染行情/持仓列表

## 生产部署注意

1. **API 地址**：将 localhost:8000 替换为生产 HTTPS API
2. **网络安全**：module.json5 已声明 INTERNET 权限
3. **签名**：需要华为开发者账号 + HAP 签名
4. **上架**：华为应用市场（AppGallery）

## HarmonyOS 独有特性（待实现）

- 元服务（Atomic Service）：轻量化，免安装体验
- 分布式流转：手机↔平板↔大屏无缝切换
- 组件化卡片：桌面快捷行情卡片
- 华为支付集成（HiPay）：订阅付款
