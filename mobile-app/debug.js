// 详细调试脚本
const { execSync } = require('child_process');
const path = require('path');

const projectDir = 'C:\\Users\\Administrator\\WorkBuddy\\Claw\\quantai-app\\mobile-app';
process.chdir(projectDir);

console.log('当前工作目录:', process.cwd());
console.log('Node 版本:', process.version);

// 设置环境变量
process.env.JAVA_HOME = 'C:\\Program Files\\Eclipse Adoptium\\jdk-21.0.10.7-hotspot';
process.env.ANDROID_HOME = 'C:\\Users\\Administrator\\android-sdk';
process.env.ANDROID_SDK_ROOT = 'C:\\Users\\Administrator\\android-sdk';
process.env.PATH = 'C:\\Program Files\\nodejs;' + process.env.JAVA_HOME + '\\bin;' + process.env.ANDROID_HOME + '\\platform-tools;' + process.env.ANDROID_HOME + '\\cmdline-tools\\latest\\bin;' + process.env.PATH;

console.log('JAVA_HOME:', process.env.JAVA_HOME);
console.log('ANDROID_HOME:', process.env.ANDROID_HOME);

// 检查CLI文件
const cliPath = path.join(projectDir, 'node_modules', '@capacitor', 'cli', 'dist', 'index.js');
console.log('CLI路径:', cliPath);
console.log('CLI存在:', require('fs').existsSync(cliPath));

try {
    console.log('\n=== 运行 Capacitor CLI ===');
    const result = execSync(`"C:\\Program Files\\nodejs\\node.exe" "${cliPath}" add android`, {
        encoding: 'utf8',
        timeout: 120000,
        stdio: 'pipe'
    });
    console.log('输出:', result);
    console.log('✅ 成功添加 Android 平台');
} catch (e) {
    console.log('❌ 错误:', e.message);
    if (e.stderr) console.log('STDERR:', e.stderr);
    if (e.stdout) console.log('STDOUT:', e.stdout);
    if (e.status) console.log('Exit code:', e.status);
}
