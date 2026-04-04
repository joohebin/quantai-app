process.chdir('C:\\Users\\Administrator\\WorkBuddy\\Claw\\quantai-app\\mobile-app');
const { loadConfig } = require('./node_modules/@capacitor/cli/dist/config.js');
const path = require('path');

(async () => {
    const config = await loadConfig();
    console.log('Android platform dir:', config.android.platformDirAbs);
    console.log('Template archive:', config.cli.assets.android.platformTemplateArchiveAbs);
    
    // 检查模板文件是否存在
    const fs = require('fs');
    console.log('Template exists:', fs.existsSync(config.cli.assets.android.platformTemplateArchiveAbs));
    
    // 列出 assets 目录
    console.log('Assets dir:', config.cli.assetsDirAbs);
    if (fs.existsSync(config.cli.assetsDirAbs)) {
        console.log('Assets contents:', fs.readdirSync(config.cli.assetsDirAbs));
    }
})();
