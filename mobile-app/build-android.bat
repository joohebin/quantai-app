@echo off
cd /d C:\Users\Administrator\WorkBuddy\Claw\quantai-app\mobile-app
set JAVA_HOME=C:\Program Files\Eclipse Adoptium\jdk-21.0.10.7-hotspot
set ANDROID_HOME=C:\Users\Administrator\android-sdk
set ANDROID_SDK_ROOT=C:\Users\Administrator\android-sdk
set PATH=C:\Program Files\nodejs;%JAVA_HOME%\bin;%ANDROID_HOME%\platform-tools;%ANDROID_HOME%\cmdline-tools\latest\bin;%PATH%
node node_modules/@capacitor/cli/dist/index.js build android
