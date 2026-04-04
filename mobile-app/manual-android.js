const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

const androidDir = 'C:\\Users\\Administrator\\WorkBuddy\\Claw\\quantai-app\\mobile-app\\android';
const appDir = 'C:\\Users\\Administrator\\WorkBuddy\\Claw\\quantai-app\\mobile-app';

console.log('=== Manual Android Project Build ===\n');

// Clean old
if (fs.existsSync(androidDir)) {
    fs.rmSync(androidDir, { recursive: true, force: true });
    console.log('✓ Cleaned old android folder\n');
}

// Create structure
const dirs = [
    androidDir,
    path.join(androidDir, 'app', 'src', 'main', 'java', 'com', 'quantai', 'app'),
    path.join(androidDir, 'app', 'src', 'main', 'res', 'drawable'),
    path.join(androidDir, 'app', 'src', 'main', 'res', 'mipmap-hdpi'),
    path.join(androidDir, 'app', 'src', 'main', 'res', 'mipmap-mdpi'),
    path.join(androidDir, 'app', 'src', 'main', 'res', 'mipmap-xhdpi'),
    path.join(androidDir, 'app', 'src', 'main', 'res', 'mipmap-xxhdpi'),
    path.join(androidDir, 'app', 'src', 'main', 'res', 'mipmap-xxxhdpi'),
    path.join(androidDir, 'app', 'src', 'main', 'res', 'values'),
    path.join(androidDir, 'app', 'src', 'main', 'res', 'xml'),
    path.join(androidDir, 'gradle', 'wrapper'),
];

dirs.forEach(d => {
    fs.mkdirSync(d, { recursive: true });
    console.log('Created:', d);
});

// ====== gradle.properties ======
fs.writeFileSync(path.join(androidDir, 'gradle.properties'), `
org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.useAndroidX=true
android.enableJetifier=true
kotlin.code.style=official
android.nonTransitiveRClass=true
`);

// ====== settings.gradle ======
fs.writeFileSync(path.join(androidDir, 'settings.gradle'), `
include ':app'
include ':capacitor-android'
project(':capacitor-android').projectDir = new File(rootProject.projectDir, '../node_modules/@capacitor/android/capacitor')
`);

// ====== build.gradle (root) ======
fs.writeFileSync(path.join(androidDir, 'build.gradle'), `
buildscript {
    repositories {
        google()
        mavenCentral()
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:8.2.1'
    }
}
allprojects {
    repositories {
        google()
        mavenCentral()
    }
}
task clean(type: Delete) { delete rootProject.buildDir }
`);

// ====== local.properties ======
fs.writeFileSync(path.join(androidDir, 'local.properties'), `
sdk.dir=C\\:\\\\Users\\\\Administrator\\\\android-sdk
`);

// ====== gradle-wrapper.properties ======
fs.writeFileSync(path.join(androidDir, 'gradle', 'wrapper', 'gradle-wrapper.properties'), `
distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\\://services.gradle.org/distributions/gradle-8.2.1-bin.zip
networkTimeout=10000
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
`);

// ====== gradlew.bat ======
fs.writeFileSync(path.join(androidDir, 'gradlew.bat'), `@echo off
setlocal enabledelayedexpansion
set DIRNAME=%~dp0
set APP_BASE_NAME=%~n0
set APP_HOME=%DIRNAME%
set JAVA_HOME=%JAVA_HOME:"=%
if defined JAVA_HOME goto findJavaFromJavaHome
set JAVA_EXE=%JAVA_HOME%/bin/java.exe
if exist "%JAVA_EXE%" goto init
:findJavaFromJavaHome
set JAVA_HOME=C:\\Program Files\\Eclipse Adoptium\\jdk-21.0.10.7-hotspot
set JAVA_EXE=%JAVA_HOME%/bin/java.exe
if exist "%JAVA_EXE%" goto init
echo ERROR: JAVA_HOME is not set.
exit /b 1
:init
@rem Get command-line arguments
set CMD_LINE_ARGS=
set _SKIP=2
:argloop
if "%~1"=="" goto runGradle
set CMD_LINE_ARGS=%CMD_LINE_ARGS% %1
shift
goto argloop
:runGradle
call "%JAVA_EXE%" -Xmx2048m -jar "%APP_HOME%\\gradle\\wrapper\\gradle-wrapper.jar" %CMD_LINE_ARGS%
exit /b %ERRORLEVEL%
`);

// ====== app/build.gradle ======
fs.writeFileSync(path.join(androidDir, 'app', 'build.gradle'), `
plugins {
    id 'com.android.application'
}
android {
    namespace 'com.quantai.app'
    compileSdk 34
    defaultConfig {
        applicationId "com.quantai.app"
        minSdk 22
        targetSdk 34
        versionCode 1
        versionName "1.0.0"
    }
    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
        }
    }
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_17
        targetCompatibility JavaVersion.VERSION_17
    }
}
dependencies {
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'androidx.core:core:1.12.0'
    implementation project(':capacitor-android')
}
`);

// ====== app/proguard-rules.pro ======
fs.writeFileSync(path.join(androidDir, 'app', 'proguard-rules.pro'), `
# Add project specific ProGuard rules here.
`);

// ====== AndroidManifest.xml ======
fs.writeFileSync(path.join(androidDir, 'app', 'src', 'main', 'AndroidManifest.xml'), `<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="QuantAI"
        android:roundIcon="@mipmap/ic_launcher"
        android:supportsRtl="true"
        android:theme="@style/Theme.AppCompat.Light.NoActionBar">
        <activity
            android:configChanges="orientation|keyboardHidden|keyboard|screenSize|locale|smallestScreenSize|screenLayout|uiMode"
            android:name="com.quantai.app.MainActivity"
            android:exported="true"
            android:windowSoftInputMode="adjustResize">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
`);

// ====== MainActivity.java ======
fs.writeFileSync(path.join(androidDir, 'app', 'src', 'main', 'java', 'com', 'quantai', 'app', 'MainActivity.java'), `
package com.quantai.app;

import android.os.Bundle;
import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }
}
`);

// ====== strings.xml ======
fs.writeFileSync(path.join(androidDir, 'app', 'src', 'main', 'res', 'values', 'strings.xml'), `<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">QuantAI</string>
</resources>
`);

// ====== styles.xml ======
fs.writeFileSync(path.join(androidDir, 'app', 'src', 'main', 'res', 'values', 'styles.xml'), `<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="Theme.AppCompat.Light.NoActionBar" parent="@style/Theme.AppCompat.Light.DarkActionBar">
        <item name="windowActionBar">false</item>
        <item name="windowNoTitle">true</item>
    </style>
</resources>
`);

// ====== Create web assets directory ======
const webDir = path.join(androidDir, 'app', 'src', 'main', 'assets', 'public');
fs.mkdirSync(webDir, { recursive: true });
console.log('\nCreated web assets dir:', webDir);

// Copy web files
const indexSrc = path.join(appDir, 'dist', 'index.html');
const indexDst = path.join(webDir, 'index.html');
if (fs.existsSync(indexSrc)) {
    fs.copyFileSync(indexSrc, indexDst);
    console.log('Copied index.html');
}

console.log('\n✅ Android project structure created!');
console.log('\nNext: Copy your web assets to', webDir);
