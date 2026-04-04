// 详细诊断脚本
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

const projectDir = 'C:\\Users\\Administrator\\WorkBuddy\\Claw\\quantai-app\\mobile-app';

const env = {
    ...process.env,
    JAVA_HOME: 'C:\\Program Files\\Eclipse Adoptium\\jdk-21.0.10.7-hotspot',
    ANDROID_HOME: 'C:\\Users\\Administrator\\android-sdk',
    ANDROID_SDK_ROOT: 'C:\\Users\\Administrator\\android-sdk',
    PATH: 'C:\\Program Files\\nodejs;C:\\Program Files\\Eclipse Adoptium\\jdk-21.0.10.7-hotspot\\bin;C:\\Users\\Administrator\\android-sdk\\platform-tools;C:\\Users\\Administrator\\android-sdk\\cmdline-tools\\latest\\bin;C:\\Windows\\system32;C:\\Windows;C:\\Windows\\System32\\Wbem'
};

console.log('=== 诊断 Capacitor CLI ===');
console.log('工作目录:', projectDir);

// 检查 CLI 文件
const cliPath = path.join(projectDir, 'node_modules', '@capacitor', 'cli', 'dist', 'index.js');
console.log('CLI 路径:', cliPath);
console.log('CLI 存在:', fs.existsSync(cliPath));

// 检查 www 目录
const wwwDir = path.join(projectDir, 'www');
console.log('www 目录存在:', fs.existsSync(wwwDir));
if (fs.existsSync(wwwDir)) {
    console.log('www 目录内容:', fs.readdirSync(wwwDir));
}

// 执行 CLI 命令并捕获输出
console.log('\n=== 执行 cap add android ===');

const child = spawn('node', ['node_modules/@capacitor/cli/dist/index.js', 'add', 'android'], {
    cwd: projectDir,
    env: env
});

let stdout = '';
let stderr = '';

child.stdout.on('data', (data) => {
    const text = data.toString();
    stdout += text;
    process.stdout.write('[STDOUT] ' + text);
});

child.stderr.on('data', (data) => {
    const text = data.toString();
    stderr += text;
    process.stdout.write('[STDERR] ' + text);
});

child.on('close', (code) => {
    console.log('\n=== 命令完成 ===');
    console.log('退出码:', code);
    console.log('android 目录存在:', fs.existsSync(path.join(projectDir, 'android')));
});

child.on('error', (err) => {
    console.log('\n=== 错误 ===');
    console.log(err);
});

// 5秒后超时
setTimeout(() => {
    console.log('\n=== 超时，强制结束 ===');
    child.kill();
}, 5000);
