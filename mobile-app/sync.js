process.chdir('C:\\Users\\Administrator\\WorkBuddy\\Claw\\quantai-app\\mobile-app');
const { spawn } = require('child_process');

const env = {
    ...process.env,
    JAVA_HOME: 'C:\\Program Files\\Eclipse Adoptium\\jdk-21.0.10.7-hotspot',
    ANDROID_HOME: 'C:\\Users\\Administrator\\android-sdk',
    ANDROID_SDK_ROOT: 'C:\\Users\\Administrator\\android-sdk',
    PATH: `C:\\Program Files\\nodejs;C:\\Program Files\\Eclipse Adoptium\\jdk-21.0.10.7-hotspot\\bin;C:\\Users\\Administrator\\android-sdk\\platform-tools;C:\\Users\\Administrator\\android-sdk\\cmdline-tools\\latest\\bin;C:\\Windows\\system32;C:\\Windows;C:\\Windows\\System32\\Wbem`
};

console.log('=== 运行 Capacitor Sync ===');
console.log('工作目录:', process.cwd());

const child = spawn('C:\\Program Files\\nodejs\\node.exe', ['node_modules/@capacitor/cli/dist/index.js', 'sync', 'android'], {
    cwd: 'C:\\Users\\Administrator\\WorkBuddy\\Claw\\quantai-app\\mobile-app',
    env: env,
    stdio: 'inherit'
});

child.on('close', (code) => {
    console.log('\n=== Sync 完成 ===');
    console.log('退出码:', code);
    
    // 完成后检查配置文件
    const fs = require('fs');
    const capSettings = 'C:\\Users\\Administrator\\WorkBuddy\\Claw\\quantai-app\\mobile-app\\android\\capacitor.settings.gradle';
    console.log('capacitor.settings.gradle 存在:', fs.existsSync(capSettings));
});

child.on('error', (err) => {
    console.log('错误:', err);
});
