// 创建 Android SDK 许可证文件
const fs = require('fs');

const licensesDir = 'C:\\Android\\Sdk\\licenses';

if (!fs.existsSync(licensesDir)) {
    fs.mkdirSync(licensesDir, { recursive: true });
}

// Android SDK License
const licenseContent = `24333f8a63b6825ea9c5514f83c2829b004d1fee
84831b9409646a918e30573bab4c9c91346d8abd
d56f5187479451eabf01fb78af6dfcb131a6481e`;

fs.writeFileSync(`${licensesDir}\\android-sdk-license`, licenseContent);
fs.writeFileSync(`${licensesDir}\\android-sdk-preview-license`, licenseContent);

// Android NDK License
fs.writeFileSync(`${licensesDir}\\android-googletv-license`, licenseContent);
fs.writeFileSync(`${licensesDir}\\google-gdk-license`, licenseContent);
fs.writeFileSync(`${licensesDir}\\intel-android-extra-license`, licenseContent);

console.log('✅ Android SDK 许可证文件创建完成');
console.log(`   位置: ${licensesDir}`);
