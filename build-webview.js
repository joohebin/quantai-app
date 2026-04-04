// 简化的 Android APK 构建 - 使用 WebView 直接加载 HTML
const fs = require('fs');
const path = require('path');

const projectDir = 'C:\\Users\\Administrator\\WorkBuddy\\Claw\\quantai-app';
const buildDir = path.join(projectDir, 'build-output');
const apkDir = path.join(buildDir, 'apk');
const wwwDir = path.join(projectDir, 'www');

// 创建目录
[buildDir, apkDir, path.join(apkDir, 'assets')].forEach(dir => {
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
});

// 1. 复制 HTML 文件
console.log('📁 复制 Web 内容...');
const srcHtml = path.join(wwwDir, 'index.html');
const destHtml = path.join(apkDir, 'assets', 'index.html');
fs.copyFileSync(srcHtml, destHtml);
console.log(`✅ 复制: ${path.basename(srcHtml)}`);

// 2. 创建 AndroidManifest.xml
console.log('\n📝 创建 AndroidManifest.xml...');
const manifest = `<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.quantai.app"
    android:versionCode="1"
    android:versionName="1.0.0">
    <uses-permission android:name="android.permission.INTERNET"/>
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>
    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="QuantAI"
        android:supportsRtl="true"
        android:theme="@android:style/Theme.NoTitleBar.Fullscreen"
        android:usesCleartextTraffic="true">
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:screenOrientation="portrait">
            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
        </activity>
    </application>
</manifest>`;
fs.writeFileSync(path.join(apkDir, 'AndroidManifest.xml'), manifest);
console.log('✅ AndroidManifest.xml 创建完成');

// 3. 创建 MainActivity.java
console.log('\n📝 创建 MainActivity.java...');
const mainActivity = `package com.quantai.app;

import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class MainActivity extends Activity {
    private WebView webView;
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
        // 创建 WebView
        webView = new WebView(this);
        setContentView(webView);
        
        // 配置 WebView
        WebSettings webSettings = webView.getSettings();
        webSettings.setJavaScriptEnabled(true);
        webSettings.setDomStorageEnabled(true);
        webSettings.setAllowFileAccess(true);
        webSettings.setCacheMode(WebSettings.LOAD_DEFAULT);
        webSettings.setSupportZoom(true);
        webSettings.setBuiltInZoomControls(true);
        webSettings.setDisplayZoomControls(false);
        
        // 允许加载混合内容 (HTTP + HTTPS)
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.LOLLIPOP) {
            webView.getSettings().setMixedContentMode(WebSettings.MIXED_CONTENT_ALWAYS_ALLOW);
        }
        
        // 设置 WebViewClient
        webView.setWebViewClient(new WebViewClient());
        
        // 加载本地 HTML
        webView.loadUrl("file:///android_asset/index.html");
    }
    
    @Override
    public void onBackPressed() {
        if (webView.canGoBack()) {
            webView.goBack();
        } else {
            super.onBackPressed();
        }
    }
}`;
fs.writeFileSync(path.join(apkDir, 'MainActivity.java'), mainActivity);
console.log('✅ MainActivity.java 创建完成');

console.log('\n' + '='.repeat(50));
console.log('⚠️  注意：这是源代码目录结构，不是完整的APK');
console.log('   需要使用 Android Studio 或 AAPT 工具来打包 APK');
console.log('='.repeat(50));
console.log('\n📦 构建内容已准备在: ' + apkDir);
