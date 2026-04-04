QuantAI Mobile - Capacitor 打包说明
=====================================

支持平台：Android / iOS / 旧鸿蒙（兼容 Android）

## 前置要求

### Android 打包
- JDK 17+
- Android Studio（含 SDK Build-tools 34+）
- 环境变量：ANDROID_HOME / JAVA_HOME

### iOS 打包（需要 macOS）
- Xcode 15+
- Apple Developer 账号（$99/年，发布到 App Store 必须）
- CocoaPods：`sudo gem install cocoapods`

## 步骤

### 1. 安装 Capacitor 依赖
    cd quantai-app/mobile-app
    npm install

### 2. 添加平台
    npx cap add android
    npx cap add ios

### 3. 同步 Web 前端代码
    npx cap sync

### 4. Android 调试运行
    npx cap run android
    # 或用 Android Studio 打开
    npx cap open android

### 5. iOS 调试运行（macOS 限定）
    npx cap run ios
    # 或用 Xcode 打开
    npx cap open ios

### 6. Android 生产打包（APK）
    cd android
    ./gradlew assembleRelease
    # APK 路径：android/app/build/outputs/apk/release/app-release.apk

### 7. Android 签名（发布到应用商店）
    # 生成签名密钥
    keytool -genkey -v -keystore quantai-release.keystore -alias quantai -keyalg RSA -keysize 2048 -validity 10000
    # 在 android/app/build.gradle 配置 signingConfigs

## 鸿蒙兼容版（旧鸿蒙 = Android 内核）

- 旧鸿蒙（HarmonyOS 3.x 及以前）基于 Android 内核
- 直接将 Android APK 上架到**华为应用市场**即可
- WebView 版本可能较旧，确保兼容性：
  - 避免使用 ES2022+ 特性（或用 Babel 转译）
  - 测试 Flexbox/Grid 在华为 WebView 的表现

## Capacitor 插件说明

| 插件 | 用途 |
|------|------|
| @capacitor/status-bar | 状态栏颜色适配深色主题 |
| @capacitor/splash-screen | 启动屏（2秒后自动隐藏） |
| @capacitor/keyboard | 键盘弹出时调整布局 |
| @capacitor/push-notifications | 推送：行情预警/持仓止损提醒 |
| @capacitor/network | 检测网络状态，断网提示 |
| @capacitor/haptics | 下单时震动反馈 |

## 推送通知配置

### Android Firebase
1. 在 Firebase Console 创建项目
2. 下载 google-services.json 放入 android/app/
3. 在 android/build.gradle 添加 Firebase 依赖

### iOS APNs
1. Xcode 中开启 Push Notifications capability
2. 上传 APNs 密钥到 Firebase 或自建推送服务

## 应用图标和启动屏

图标要求：
- Android：在 android/app/src/main/res/ 下放各尺寸 mipmap
- iOS：1024x1024 PNG（Xcode 会自动缩放）

推荐工具：
- https://capacitorjs.com/docs/guides/splash-screens-and-icons
- npm install --save-dev @capacitor/assets
- npx capacitor-assets generate
