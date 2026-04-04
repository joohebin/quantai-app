const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

const androidDir = 'C:\\Users\\Administrator\\WorkBuddy\\Claw\\quantai-app\\mobile-app\\android';
const appDir = 'C:\\Users\\Administrator\\WorkBuddy\\Claw\\quantai-app\\mobile-app';

console.log('=== Gradle APK Build ===\n');

const env = {
    ...process.env,
    JAVA_HOME: 'C:\\Program Files\\Eclipse Adoptium\\jdk-21.0.10.7-hotspot',
    ANDROID_HOME: 'C:\\Users\\Administrator\\android-sdk',
    ANDROID_SDK_ROOT: 'C:\\Users\\Administrator\\android-sdk',
    PATH: process.env.PATH + ';C:\\Users\\Administrator\\AppData\\Roaming\\npm'
};

console.log('Building APK with Gradle...');

const gradle = spawn('gradle', ['assembleDebug', '--no-daemon'], {
    cwd: androidDir,
    env,
    shell: true,
    stdio: 'inherit'
});

gradle.on('close', (code) => {
    console.log('\nBuild exit code:', code);
    
    if (code === 0) {
        const apkPath = path.join(androidDir, 'app', 'build', 'outputs', 'apk', 'debug', 'app-debug.apk');
        if (fs.existsSync(apkPath)) {
            const stats = fs.statSync(apkPath);
            console.log(`\n🎉 APK built successfully!`);
            console.log(`📦 ${apkPath}`);
            console.log(`📊 Size: ${(stats.size / 1024 / 1024).toFixed(2)} MB`);
        } else {
            console.log('APK not found, checking build dir...');
            const buildDir = path.join(androidDir, 'app', 'build');
            if (fs.existsSync(buildDir)) {
                console.log('Build dir exists');
            }
        }
    } else {
        console.log('❌ Build failed');
    }
});
