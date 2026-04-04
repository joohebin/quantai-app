process.chdir('C:\\Users\\Administrator\\WorkBuddy\\Claw\\quantai-app\\mobile-app');
const fs = require('fs');
const path = require('path');
const tar = require('tar');

const projectDir = 'C:\\Users\\Administrator\\WorkBuddy\\Claw\\quantai-app\\mobile-app';
const androidDir = path.join(projectDir, 'android');
const cordovaDir = path.join(androidDir, 'capacitor-cordova-android-plugins');

(async () => {
    console.log('=== 提取 Cordova 插件模板 ===');
    const templatePath = path.join(projectDir, 'node_modules', '@capacitor', 'cli', 'assets', 'capacitor-cordova-android-plugins.tar.gz');
    
    if (fs.existsSync(cordovaDir)) {
        fs.rmSync(cordovaDir, { recursive: true });
    }
    
    await tar.extract({ file: templatePath, cwd: androidDir });
    console.log('✅ Cordova 插件模板提取完成');
    console.log('目录内容:', fs.readdirSync(androidDir));
    console.log('cordova 目录内容:', fs.readdirSync(cordovaDir));
})().catch(err => console.error('错误:', err));
