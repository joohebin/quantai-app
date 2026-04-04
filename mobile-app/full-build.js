// 完整构建脚本 - 使用 execSync
const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const projectDir = 'C:\\Users\\Administrator\\WorkBuddy\\Claw\\quantai-app\\mobile-app';
process.chdir(projectDir);

console.log('当前工作目录:', process.cwd());

// 设置环境变量
process.env.JAVA_HOME = 'C:\\Program Files\\Eclipse Adoptium\\jdk-21.0.10.7-hotspot';
process.env.ANDROID_HOME = 'C:\\Users\\Administrator\\android-sdk';
process.env.ANDROID_SDK_ROOT = 'C:\\Users\\Administrator\\android-sdk';
process.env.PATH = 'C:\\Program Files\\nodejs;' + process.env.JAVA_HOME + '\\bin;' + process.env.ANDROID_HOME + '\\platform-tools;' + process.env.ANDROID_HOME + '\\cmdline-tools\\latest\\bin;' + process.env.PATH;

console.log('JAVA_HOME:', process.env.JAVA_HOME);
console.log('ANDROID_HOME:', process.env.ANDROID_HOME);

const nodeExe = '"C:\\Program Files\\nodejs\\node.exe"';
const cliPath = 'node_modules/@capacitor/cli/dist/index.js';

function run(cmd, desc) {
    console.log(`\n=== ${desc} ===`);
    console.log(`>>> ${cmd.substring(0, 100)}...`);
    try {
        const result = execSync(cmd, {
            cwd: projectDir,
            env: process.env,
            encoding: 'utf8',
            stdio: 'pipe',
            timeout: 300000
        });
        console.log(result || '✅ 完成');
        return true;
    } catch (e) {
        console.log('❌ 错误:', e.message);
        if (e.stderr) console.log('STDERR:', e.stderr);
        if (e.stdout) console.log('STDOUT:', e.stdout);
        return false;
    }
}

async function main() {
    // 1. 添加 Android 平台
    if (!run(`${nodeExe} ${cliPath} add android`, '添加 Android 平台')) {
        console.log('添加 Android 平台失败');
        // 检查是否已经存在
        if (fs.existsSync(path.join(projectDir, 'android'))) {
            console.log('Android 目录已存在，跳过添加步骤');
        } else {
            return;
        }
    }
    
    // 2. 同步
    if (!run(`${nodeExe} ${cliPath} sync android`, '同步 Capacitor')) {
        console.log('同步失败');
        return;
    }
    
    // 3. 构建 APK
    const gradlewBat = path.join(projectDir, 'android', 'gradlew.bat');
    if (!fs.existsSync(gradlewBat)) {
        console.log('❌ gradlew.bat 不存在');
        return;
    }
    
    if (!run(`"${gradlewBat}" assembleDebug`, '构建 APK')) {
        console.log('Gradle 构建失败');
        return;
    }
    
    // 4. 检查 APK
    console.log('\n=== 检查 APK ===');
    const apkDir = path.join(projectDir, 'android', 'app', 'build', 'outputs', 'apk', 'debug');
    if (fs.existsSync(apkDir)) {
        const files = fs.readdirSync(apkDir).filter(f => f.endsWith('.apk'));
        if (files.length > 0) {
            files.forEach(f => {
                const size = (fs.statSync(path.join(apkDir, f)).size / 1024 / 1024).toFixed(2) + ' MB';
                console.log(`✅ APK: ${f} (${size})`);
            });
        } else {
            console.log('⚠️ APK 目录为空');
        }
    } else {
        console.log('⚠️ APK 目录不存在');
    }
    
    console.log('\n🎉 构建完成!');
}

main();
