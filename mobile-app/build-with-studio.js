// 使用 Android Studio 命令行构建 APK
const { execSync } = require('child_process');
const path = require('path');

const androidDir = 'C:\\Users\\Administrator\\WorkBuddy\\Claw\\quantai-app\\mobile-app\\android';
const studioBin = 'C:\\Program Files\\Android\\Android Studio\\bin\\studio64.exe';

console.log('🔨 使用 Android Studio 构建 APK...\n');

// 设置环境变量
const env = {
    ...process.env,
    ANDROID_HOME: 'C:\\Program Files\\Android\\Android Studio\\jbr',
    ANDROID_SDK_ROOT: 'C:\\Program Files\\Android\\Android Studio\\jbr',
    JAVA_HOME: 'C:\\Program Files\\Android\\Android Studio\\jbr'
};

try {
    // 尝试使用 Android Studio 的命令行工具
    console.log('尝试使用 Gradle...');
    
    const gradleHome = 'C:\\gradle\\gradle-8.2';
    const cmd = `"${path.join(gradleHome, 'bin', 'gradle.bat')}" -p "${androidDir}" assembleDebug --no-daemon`;
    
    console.log(`执行: ${cmd}\n`);
    
    execSync(cmd, {
        env,
        stdio: 'inherit'
    });
    
    console.log('\n✅ 构建完成！');
    
} catch (err) {
    console.error('\n❌ Gradle 构建失败:', err.message);
    console.log('\n💡 请手动在 Android Studio 中打开项目:');
    console.log(`   ${androidDir}`);
    console.log('   然后选择 Build > Make Project');
}
