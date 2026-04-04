@echo off
chcp 65001 >nul
cd /d C:\Users\Administrator\WorkBuddy\Claw\quantai-app\mobile-app
set JAVA_HOME=C:\Program Files\Eclipse Adoptium\jdk-21.0.10.7-hotspot
set ANDROID_HOME=C:\Users\Administrator\android-sdk
set ANDROID_SDK_ROOT=C:\Users\Administrator\android-sdk
set PATH=C:\Program Files\nodejs;%JAVA_HOME%\bin;%ANDROID_HOME%\platform-tools;%ANDROID_HOME%\cmdline-tools\latest\bin;%PATH%

echo === 检查 Capacitor CLI ===
"C:\Program Files\nodejs\node.exe" node_modules/@capacitor/cli/dist/index.js --version

echo.
echo === 添加 Android 平台 ===
"C:\Program Files\nodejs\node.exe" node_modules/@capacitor/cli/dist/index.js add android

echo.
echo === 同步 Capacitor ===
"C:\Program Files\nodejs\node.exe" node_modules/@capacitor/cli/dist/index.js sync android

echo.
echo === 构建 APK ===
cd android
call gradlew.bat assembleDebug

echo.
echo === 完成 ===
