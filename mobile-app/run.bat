@echo off
chcp 65001 >nul
cd /d C:\Users\Administrator\WorkBuddy\Claw\quantai-app\mobile-app
set JAVA_HOME=C:\Program Files\Eclipse Adoptium\jdk-21.0.10.7-hotspot
set ANDROID_HOME=C:\Users\Administrator\android-sdk
set ANDROID_SDK_ROOT=C:\Users\Administrator\android-sdk
set PATH=C:\Program Files\nodejs;%JAVA_HOME%\bin;%ANDROID_HOME%\platform-tools;%ANDROID_HOME%\cmdline-tools\latest\bin;%PATH%

echo === 1. 添加 Android 平台 ===
echo y | "C:\Program Files\nodejs\node.exe" node_modules/@capacitor/cli/dist/index.js add android
if errorlevel 1 (
    echo 添加失败
    exit /b 1
)

echo === 2. 检查 android 目录 ===
if not exist android (
    echo android 目录不存在!
    exit /b 1
)

echo === 3. 同步 ===
"C:\Program Files\nodejs\node.exe" node_modules/@capacitor/cli/dist/index.js sync android

echo === 4. 构建 APK ===
cd android
call gradlew.bat assembleDebug

echo === 5. 完成 ===
dir /s /b *.apk
