// 详细检查 Capacitor CLI 输出
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

const nodeExe = '"C:\\Program Files\\nodejs\\node.exe"';
const cliPath = 'node_modules/@capacitor/cli/dist/index.js';

console.log('\n=== 检查 Capacitor CLI 版本 ===');
try {
    const result = execSync(`${nodeExe} ${cliPath} --version`, {
        cwd: projectDir,
        env: process.env,
        encoding: 'utf8',
        stdio: 'pipe'
    });
    console.log('版本:', result.trim());
} catch (e) {
    console.log('错误:', e.message);
}

console.log('\n=== 添加 Android 平台（详细输出）===');
try {
    const result = execSync(`${nodeExe} ${cliPath} add android --verbose`, {
        cwd: projectDir,
        env: process.env,
        encoding: 'utf8',
        maxBuffer: 10 * 1024 * 1024
    });
    console.log('输出:', result);
} catch (e) {
    console.log('错误信息:', e.message);
    console.log('状态码:', e.status);
    console.log('STDERR:', e.stderr ? e.stderr.toString() : '无');
    console.log('STDOUT:', e.stdout ? e.stdout.toString() : '无');
}

console.log('\n=== 检查 android 目录 ===');
const androidDir = path.join(projectDir, 'android');
console.log('android 目录存在:', fs.existsSync(androidDir));

if (fs.existsSync(androidDir)) {
    console.log('android 目录内容:', fs.readdirSync(androidDir));
}
