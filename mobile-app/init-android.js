// 正确的Capacitor Android项目初始化脚本
const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const appDir = path.join(__dirname);
const androidDir = path.join(appDir, 'android');
const wwwDir = path.join(appDir, 'www');

console.log('🔧 重新初始化 Capacitor Android 项目\n');

// 1. 删除旧Android项目
console.log('1️⃣ 删除旧Android项目...');
if (fs.existsSync(androidDir)) {
    fs.rmSync(androidDir, { recursive: true, force: true });
    console.log('   ✅ 已删除旧Android项目\n');
}

// 2. 使用npx调用Capacitor CLI初始化
console.log('2️⃣ 初始化Android平台...');
try {
    // 确保使用Capacitor CLI添加Android
    const cmd = `"C:\\Program Files\\nodejs\\node.exe" "C:\\Users\\Administrator\\WorkBuddy\\Claw\\quantai-app\\mobile-app\\node_modules\\@capacitor\\cli\\bin\\capacitor" add android`;
    console.log(`   执行: ${cmd}\n`);
    
    execSync(cmd, {
        cwd: appDir,
        env: { ...process.env },
        stdio: 'inherit'
    });
    
    console.log('\n3️⃣ 同步Web内容...');
    const syncCmd = `"C:\\Program Files\\nodejs\\node.exe" "C:\\Users\\Administrator\\WorkBuddy\\Claw\\quantai-app\\mobile-app\\node_modules\\@capacitor\\cli\\bin\\capacitor" sync android`;
    execSync(syncCmd, {
        cwd: appDir,
        env: { ...process.env },
        stdio: 'inherit'
    });
    
    console.log('\n✅ Capacitor初始化完成！');
    console.log('   Android项目位置: ' + androidDir);
    
} catch (err) {
    console.error('\n❌ 初始化失败:', err.message);
    process.exit(1);
}
