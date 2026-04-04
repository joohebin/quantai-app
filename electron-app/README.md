QuantAI Desktop - Electron 构建说明
=====================================

## 目录结构

electron-app/
├── package.json          ← Electron 依赖 + electron-builder 配置
├── electron/
│   ├── main.js           ← 主进程（窗口/菜单/托盘/IPC）
│   └── preload.js        ← 预加载脚本（安全桥接）
├── assets/
│   ├── icon.ico          ← Windows 图标（256x256 ICO）
│   ├── icon.icns         ← macOS 图标（ICNS格式）
│   ├── icon.png          ← 通用 PNG（512x512）
│   └── dmg-bg.png        ← macOS DMG 背景图
└── dist/                 ← 构建输出目录（自动生成）

## 快速开始

### 安装依赖
    cd quantai-app/electron-app
    npm install

### 开发模式运行（实时预览）
    npm run dev

### 构建 Windows 安装包（.exe）
    npm run build:win

### 构建 macOS 安装包（.dmg）
    npm run build:mac

### 同时构建 Windows + macOS
    npm run build:all

## 构建产物

- Windows: dist/QuantAI Setup 1.0.0.exe（NSIS 安装程序）
           dist/QuantAI 1.0.0.exe（免安装便携版）
- macOS:   dist/QuantAI-1.0.0.dmg（安装镜像）
           dist/QuantAI-1.0.0-mac.zip（压缩包）

## 注意事项

1. **图标文件**：需要在 assets/ 目录下准备图标文件
   - icon.ico：256x256，多尺寸 ICO（可用 imagemagick 或在线工具生成）
   - icon.icns：macOS 格式（Mac 上用 iconutil 生成）
   - 临时可直接跳过，electron-builder 会使用默认图标

2. **macOS 签名**：
   - 正式发布需要 Apple Developer 账号签名
   - 开发测试：在 package.json 的 mac 配置加 "identity": null 跳过签名

3. **自动更新**：
   - 需要配置 electron-updater 的更新服务器
   - 可用 GitHub Releases 或 S3 托管更新包

4. **前端路径**：
   - main.js 中 frontendPath 指向 ../../index.html
   - 即 quantai-app/index.html（H5前端主文件）

## 功能特性

- ✅ 深色主题窗口（背景色 #0a0e1a 防白屏闪烁）
- ✅ macOS hiddenInset 标题栏（沉浸式）
- ✅ 系统托盘（最小化到托盘，双击恢复）
- ✅ 原生菜单（含键盘快捷键）
- ✅ 紧急平仓确认对话框（Cmd/Ctrl+Shift+X）
- ✅ 防多实例（第二个实例会激活已有窗口）
- ✅ 拦截外部链接（在系统浏览器打开）
- ✅ 自动更新（electron-updater）
- ✅ 原生通知支持
- ✅ 文件保存（导出报告 CSV）
- ✅ IPC 安全桥接（contextBridge）
