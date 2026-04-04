process.chdir('C:\\Users\\Administrator\\WorkBuddy\\Claw\\quantai-app\\mobile-app');
console.log('Working directory:', process.cwd());

const { execSync } = require('child_process');

// 设置环境变量
process.env.JAVA_HOME = 'C:\\Program Files\\Eclipse Adoptium\\jdk-21.0.10.7-hotspot';
process.env.ANDROID_HOME = 'C:\\Users\\Administrator\\android-sdk';
process.env.ANDROID_SDK_ROOT = 'C:\\Users\\Administrator\\android-sdk';
process.env.PATH = 'C:\\Program Files\\nodejs;' + process.env.JAVA_HOME + '\\bin;' + process.env.ANDROID_HOME + '\\platform-tools;' + process.env.ANDROID_HOME + '\\cmdline-tools\\latest\\bin;' + process.env.PATH;

console.log('\n=== 1. 添加 Android 平台 ===');
try {
    const result = execSync('node node_modules/@capacitor/cli/dist/index.js add android', { encoding: 'utf8', timeout: 120000, stdio: 'inherit' });
    console.log('✅ Android 平台添加成功');
} catch (e) {
    console.log('添加失败:', e.message);
    process.exit(1);
}

console.log('\n=== 2. 同步 Capacitor ===');
try {
    const result = execSync('node node_modules/@capacitor/cli/dist/index.js sync android', { encoding: 'utf8', timeout: 120000, stdio: 'inherit' });
    console.log('✅ 同步成功');
} catch (e) {
    console.log('同步失败:', e.message);
    process.exit(1);
}

console.log('\n=== 3. 构建 APK ===');
try {
    const result = execSync('.\\gradlew.bat assembleDebug', {
        encoding: 'utf8',
        timeout: 600000,
        stdio: 'inherit',
        cwd: 'C:\\Users\\Administrator\\WorkBuddy\\Claw\\quantai-app\\mobile-app\\android'
    });
    console.log('✅ Gradle 构建成功');
} catch (e) {
    console.log('Gradle 构建失败:', e.message);
    process.exit(1);
}

console.log('\n=== 4. 检查 APK ===');
const fs = require('fs');
const apkDir = 'C:\\Users\\Administrator\\WorkBuddy\\Claw\\quantai-app\\mobile-app\\android\\app\\build\\outputs\\apk\\debug';
if (fs.existsSync(apkDir)) {
    const files = fs.readdirSync(apkDir).filter(f => f.endsWith('.apk'));
    files.forEach(f => {
        const size = (fs.statSync(apkDir + '\\' + f).size / 1024 / 1024).toFixed(2) + ' MB';
        console.log('✅ APK: ' + f + ' (' + size + ')');
    });
} else {
    console.log('⚠️ APK 目录不存在');
}
