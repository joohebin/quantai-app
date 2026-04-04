// 使用 Node.js 子进程执行
const { spawn, execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const projectDir = 'C:\\Users\\Administrator\\WorkBuddy\\Claw\\quantai-app\\mobile-app';

process.chdir(projectDir);

// 设置干净的环境变量
const env = {
    ...process.env,
    JAVA_HOME: 'C:\\Program Files\\Eclipse Adoptium\\jdk-21.0.10.7-hotspot',
    ANDROID_HOME: 'C:\\Users\\Administrator\\android-sdk',
    ANDROID_SDK_ROOT: 'C:\\Users\\Administrator\\android-sdk',
    PATH: 'C:\\Program Files\\nodejs;C:\\Program Files\\Eclipse Adoptium\\jdk-21.0.10.7-hotspot\\bin;C:\\Users\\Administrator\\android-sdk\\platform-tools;C:\\Users\\Administrator\\android-sdk\\cmdline-tools\\latest\\bin;C:\\Windows\\system32;C:\\Windows;C:\\Windows\\System32\\Wbem'
};

console.log('工作目录:', process.cwd());

// 同步输出到父进程
function syncExec(cmd, args, options = {}) {
    return new Promise((resolve, reject) => {
        console.log(`\n>>> ${cmd} ${args.join(' ')}`);
        
        const child = spawn(cmd, args, {
            cwd: projectDir,
            env: env,
            stdio: 'inherit',
            shell: true
        });
        
        child.on('close', (code) => {
            if (code === 0) {
                console.log(`✅ 成功`);
                resolve(code);
            } else {
                console.log(`❌ 失败，退出码: ${code}`);
                reject(code);
            }
        });
        
        child.on('error', reject);
    });
}

async function main() {
    try {
        // 1. 添加 Android 平台
        await syncExec('node', ['node_modules/@capacitor/cli/dist/index.js', 'add', 'android']);
        
        // 2. 检查 android 目录
        const androidDir = path.join(projectDir, 'android');
        if (!fs.existsSync(androidDir)) {
            console.log('❌ android 目录未创建');
            return;
        }
        console.log('✅ android 目录已创建');
        
        // 3. 同步
        await syncExec('node', ['node_modules/@capacitor/cli/dist/index.js', 'sync', 'android']);
        
        // 4. 构建 APK
        const gradlewBat = path.join(androidDir, 'gradlew.bat');
        if (!fs.existsSync(gradlewBat)) {
            console.log('❌ gradlew.bat 不存在');
            return;
        }
        
        await syncExec('gradlew.bat', ['assembleDebug'], androidDir);
        
        // 5. 检查 APK
        const apkDir = path.join(androidDir, 'app', 'build', 'outputs', 'apk', 'debug');
        if (fs.existsSync(apkDir)) {
            const files = fs.readdirSync(apkDir).filter(f => f.endsWith('.apk'));
            if (files.length > 0) {
                files.forEach(f => {
                    const size = (fs.statSync(path.join(apkDir, f)).size / 1024 / 1024).toFixed(2);
                    console.log(`\n✅ APK 已生成: ${f} (${size} MB)`);
                });
            }
        }
        
        console.log('\n🎉 构建完成!');
    } catch (e) {
        console.log('\n❌ 构建失败:', e);
    }
}

main();
