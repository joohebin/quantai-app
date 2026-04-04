process.chdir('C:\\Users\\Administrator\\WorkBuddy\\Claw\\quantai-app\\mobile-app');
const path = require('path');
const tar = require('tar');
const fs = require('fs');

const templatePath = 'C:\\Users\\Administrator\\WorkBuddy\\Claw\\quantai-app\\mobile-app\\node_modules\\@capacitor\\cli\\assets\\android-template.tar.gz';
const destDir = 'C:\\Users\\Administrator\\WorkBuddy\\Claw\\quantai-app\\mobile-app\\android';

console.log('Source:', templatePath);
console.log('Source exists:', fs.existsSync(templatePath));
console.log('Destination:', destDir);
console.log('Destination exists:', fs.existsSync(destDir));

(async () => {
    try {
        // 确保目录存在
        if (!fs.existsSync(destDir)) {
            fs.mkdirSync(destDir, { recursive: true });
        }
        
        // 提取模板
        console.log('Extracting template...');
        await tar.extract({ file: templatePath, cwd: destDir });
        
        console.log('Extraction completed');
        console.log('Destination contents:', fs.readdirSync(destDir));
    } catch (e) {
        console.error('Error:', e);
    }
})();
