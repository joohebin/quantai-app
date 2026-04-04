// 下载并安装 Android SDK
const https = require('https');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const sdkDir = 'C:\\Android\\Sdk';
const cmdlineToolsUrl = 'https://dl.google.com/android/repository/commandlinetools-win-11076708_latest.zip';

console.log('📥 下载 Android SDK Command Line Tools...\n');

// 确保目录存在
if (!fs.existsSync(sdkDir)) {
    fs.mkdirSync(sdkDir, { recursive: true });
}

// 下载文件
function downloadFile(url, dest) {
    return new Promise((resolve, reject) => {
        const file = fs.createWriteStream(dest);
        https.get(url, (response) => {
            if (response.statusCode === 301 || response.statusCode === 302) {
                file.close();
                return downloadFile(response.headers.location, dest).then(resolve).catch(reject);
            }
            response.pipe(file);
            file.on('finish', () => {
                file.close();
                console.log(`✅ 下载完成: ${dest}`);
                resolve();
            });
        }).on('error', (err) => {
            fs.unlink(dest, () => {});
            reject(err);
        });
    });
}

async function main() {
    const zipPath = path.join(sdkDir, 'cmdline-tools.zip');
    
    try {
        await downloadFile(cmdlineToolsUrl, zipPath);
        
        console.log('\n📦 解压文件...');
        // 使用PowerShell解压
        const extractDir = path.join(sdkDir, 'temp');
        if (fs.existsSync(extractDir)) {
            fs.rmSync(extractDir, { recursive: true });
        }
        
        execSync(`powershell -NoProfile -Command "Expand-Archive -Path '${zipPath}' -DestinationPath '${extractDir}' -Force"`, { stdio: 'inherit' });
        
        // 移动到正确位置
        const toolsDir = path.join(sdkDir, 'cmdline-tools');
        if (fs.existsSync(toolsDir)) {
            fs.rmSync(toolsDir, { recursive: true });
        }
        fs.renameSync(path.join(extractDir, 'cmdline-tools'), toolsDir);
        fs.rmSync(extractDir, { recursive: true });
        fs.unlinkSync(zipPath);
        
        console.log('\n📥 安装 SDK 组件...');
        
        // 设置环境变量
        const env = { ...process.env, ANDROID_HOME: sdkDir, JAVA_HOME: 'C:\\Program Files\\Android\\Android Studio\\jbr' };
        
        // 安装 platform-tools
        const sdkManager = path.join(toolsDir, 'latest', 'bin', 'sdkmanager.bat');
        execSync(`"${sdkManager}" "platform-tools" "platforms;android-34" "build-tools;34.0.0"`, {
            env,
            stdio: 'inherit'
        });
        
        console.log('\n✅ SDK 安装完成！');
        console.log(`SDK 位置: ${sdkDir}`);
        
    } catch (err) {
        console.error('\n❌ 安装失败:', err.message);
    }
}

main();
