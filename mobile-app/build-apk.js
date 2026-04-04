process.chdir('C:\\Users\\Administrator\\WorkBuddy\\Claw\\quantai-app\\mobile-app');
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

const androidDir = 'C:\\Users\\Administrator\\WorkBuddy\\Claw\\quantai-app\\mobile-app\\android';
const sdkPath = 'C:\\Users\\Administrator\\android-sdk';

console.log('=== 1. 确保 local.properties ===');
const localProps = `sdk.dir=${sdkPath.replace(/\\/g, '\\\\')}`;
fs.writeFileSync(path.join(androidDir, 'local.properties'), localProps);
console.log('✅ local.properties 已创建');

// 2. 确保 web 资源
console.log('\n=== 2. 同步 web 资源 ===');
const webDir = path.join(androidDir, 'app', 'src', 'main', 'assets', 'public');
if (!fs.existsSync(webDir)) {
    fs.mkdirSync(webDir, { recursive: true });
}

const wwwDir = 'C:\\Users\\Administrator\\WorkBuddy\\Claw\\quantai-app\\mobile-app\\www';
if (fs.existsSync(wwwDir)) {
    const wwwFiles = fs.readdirSync(wwwDir);
    wwwFiles.forEach(file => {
        const src = path.join(wwwDir, file);
        const dest = path.join(webDir, file);
        fs.copyFileSync(src, dest);
        console.log(`  复制: ${file}`);
    });
}
console.log('✅ Web 资源已同步');

// 3. 构建 APK
console.log('\n=== 3. 构建 APK ===');
const env = {
    ...process.env,
    JAVA_HOME: 'C:\\Program Files\\Eclipse Adoptium\\jdk-21.0.10.7-hotspot',
    ANDROID_HOME: sdkPath,
    ANDROID_SDK_ROOT: sdkPath,
    PATH: `C:\\Program Files\\Eclipse Adoptium\\jdk-21.0.10.7-hotspot\\bin;${sdkPath}\\platform-tools;${sdkPath}\\cmdline-tools\\latest\\bin;C:\\Windows\\system32;C:\\Windows;C:\\Windows\\System32\\Wbem`
};

return new Promise((resolve, reject) => {
    const child = spawn('cmd.exe', ['/c', 'gradlew.bat', 'assembleDebug'], {
        cwd: androidDir,
        env: env,
        stdio: 'inherit'
    });
    
    child.on('close', (code) => {
        if (code === 0) {
            console.log('\n✅ Gradle 构建成功');
            
            // 4. 检查 APK
            console.log('\n=== 4. 检查 APK ===');
            const apkDir = path.join(androidDir, 'app', 'build', 'outputs', 'apk', 'debug');
            if (fs.existsSync(apkDir)) {
                const files = fs.readdirSync(apkDir).filter(f => f.endsWith('.apk'));
                if (files.length > 0) {
                    files.forEach(f => {
                        const fullPath = path.join(apkDir, f);
                        const size = (fs.statSync(fullPath).size / 1024 / 1024).toFixed(2);
                        console.log(`\n🎉 APK 已生成: ${f} (${size} MB)`);
                        console.log(`   路径: ${fullPath}`);
                    });
                } else {
                    console.log('⚠️ APK 目录为空');
                }
            } else {
                console.log('⚠️ APK 目录不存在');
            }
            resolve();
        } else {
            console.log(`\n❌ Gradle 构建失败，退出码: ${code}`);
            reject(code);
        }
    });
    
    child.on('error', reject);
});
