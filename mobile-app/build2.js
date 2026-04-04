// 使用 echo 自动回答提示
const { execSync, spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

const projectDir = 'C:\\Users\\Administrator\\WorkBuddy\\Claw\\quantai-app\\mobile-app';
process.chdir(projectDir);

// 设置环境变量
process.env.JAVA_HOME = 'C:\\Program Files\\Eclipse Adoptium\\jdk-21.0.10.7-hotspot';
process.env.ANDROID_HOME = 'C:\\Users\\Administrator\\android-sdk';
process.env.ANDROID_SDK_ROOT = 'C:\\Users\\Administrator\\android-sdk';
process.env.PATH = 'C:\\Program Files\\nodejs;' + process.env.JAVA_HOME + '\\bin;' + process.env.ANDROID_HOME + '\\platform-tools;' + process.env.ANDROID_HOME + '\\cmdline-tools\\latest\\bin;' + process.env.PATH;

console.log('当前工作目录:', process.cwd());

function runCommand(command, desc) {
    return new Promise((resolve, reject) => {
        console.log(`\n=== ${desc} ===`);
        console.log(`执行: ${command}`);
        
        // 使用 Windows 的 cmd 来执行，这样可以使用 |
        const child = spawn('cmd.exe', ['/c', `echo y | ${command}`], {
            cwd: projectDir,
            env: process.env,
            shell: false
        });
        
        let stdout = '';
        let stderr = '';
        
        child.stdout.on('data', (data) => {
            stdout += data.toString();
        });
        
        child.stderr.on('data', (data) => {
            stderr += data.toString();
        });
        
        child.on('close', (code) => {
            console.log('退出码:', code);
            if (stdout) console.log('STDOUT:', stdout);
            if (stderr) console.log('STDERR:', stderr);
            
            if (code === 0) {
                resolve();
            } else {
                reject(new Error(`命令失败，退出码: ${code}`));
            }
        });
        
        child.on('error', (err) => {
            console.log('错误:', err.message);
            reject(err);
        });
    });
}

async function main() {
    try {
        // 1. 添加 Android
        await runCommand(`"C:\\Program Files\\nodejs\\node.exe" node_modules/@capacitor/cli/dist/index.js add android`, '添加 Android');
        
        // 检查 android 目录
        const androidDir = path.join(projectDir, 'android');
        if (!fs.existsSync(androidDir)) {
            console.log('❌ android 目录仍未创建');
            return;
        }
        
        // 2. 同步
        await runCommand(`"C:\\Program Files\\nodejs\\node.exe" node_modules/@capacitor/cli/dist/index.js sync android`, '同步');
        
        // 3. 构建
        const gradlew = path.join(androidDir, 'gradlew.bat');
        if (fs.existsSync(gradlew)) {
            await runCommand(`"${gradlew}" assembleDebug`, '构建 APK');
        } else {
            console.log('❌ gradlew.bat 不存在');
            return;
        }
        
        // 4. 检查 APK
        const apkDir = path.join(androidDir, 'app', 'build', 'outputs', 'apk', 'debug');
        if (fs.existsSync(apkDir)) {
            const files = fs.readdirSync(apkDir).filter(f => f.endsWith('.apk'));
            files.forEach(f => {
                const size = (fs.statSync(path.join(apkDir, f)).size / 1024 / 1024).toFixed(2);
                console.log(`✅ APK: ${f} (${size} MB)`);
            });
        }
        
        console.log('\n🎉 完成!');
    } catch (e) {
        console.log('❌ 失败:', e.message);
    }
}

main();
