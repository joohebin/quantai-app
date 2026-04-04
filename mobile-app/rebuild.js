// QuantAI Android APK Build Script
// 使用方法: node rebuild.js
const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const androidDir = path.join(__dirname, 'android');
const wwwDir = path.join(__dirname, 'www');
const assetsDir = path.join(androidDir, 'app', 'src', 'main', 'assets', 'public');

console.log('🚀 QuantAI Android APK Builder\n');

// 1. 同步Web内容
console.log('📁 Syncing web content...');
if (!fs.existsSync(assetsDir)) {
    fs.mkdirSync(assetsDir, { recursive: true });
}

// 复制www到assets/public
function copyDir(src, dest) {
    if (!fs.existsSync(src)) return;
    const entries = fs.readdirSync(src, { withFileTypes: true });
    for (const entry of entries) {
        const srcPath = path.join(src, entry.name);
        const destPath = path.join(dest, entry.name);
        if (entry.isDirectory()) {
            if (!fs.existsSync(destPath)) fs.mkdirSync(destPath, { recursive: true });
            copyDir(srcPath, destPath);
        } else {
            fs.copyFileSync(srcPath, destPath);
        }
    }
}
copyDir(wwwDir, assetsDir);
console.log('✅ Web content synced\n');

// 2. 设置环境变量并构建
console.log('🔨 Building APK...');
const javaHome = 'C:\\Program Files\\Android\\Android Studio\\jbr';
const gradleHome = 'C:\\gradle\\gradle-8.2';
const gradlew = path.join(androidDir, 'gradlew.bat');

try {
    // 使用 gradlew
    const cmd = `cd "${androidDir}" && "${gradleHome}\\bin\\gradle.bat" assembleDebug --no-daemon`;
    execSync(cmd, { 
        env: { 
            ...process.env, 
            JAVA_HOME: javaHome,
            PATH: `${javaHome}\\bin;${gradleHome}\\bin;${process.env.PATH}`
        },
        stdio: 'inherit'
    });
    
    // 复制APK
    const srcApk = path.join(androidDir, 'app', 'build', 'outputs', 'apk', 'debug', 'app-debug.apk');
    const destApk = path.join(__dirname, '..', 'QuantAI-debug.apk');
    fs.copyFileSync(srcApk, destApk);
    
    const stat = fs.statSync(destApk);
    console.log(`\n✅ APK built successfully!`);
    console.log(`📦 Location: ${destApk}`);
    console.log(`📊 Size: ${(stat.size / 1024 / 1024).toFixed(2)} MB`);
    
} catch (err) {
    console.error('❌ Build failed:', err.message);
    process.exit(1);
}
