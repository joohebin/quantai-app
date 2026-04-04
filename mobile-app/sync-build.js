// Sync and Build APK script
process.env.JAVA_HOME = 'C:\\Program Files\\Eclipse Adoptium\\jdk-21.0.10.7-hotspot';
process.env.ANDROID_HOME = 'C:\\Users\\Administrator\\android-sdk';
process.env.ANDROID_SDK_ROOT = 'C:\\Users\\Administrator\\android-sdk';
process.env.PATH = 'C:\\Program Files\\nodejs;' + process.env.JAVA_HOME + '\\bin;' + process.env.ANDROID_HOME + '\\platform-tools;' + process.env.ANDROID_HOME + '\\cmdline-tools\\latest\\bin;' + process.env.PATH;

const { execSync } = require('child_process');
process.chdir('C:\\Users\\Administrator\\WorkBuddy\\Claw\\quantai-app\\mobile-app');

console.log('Syncing web app to Android...');
try {
  execSync('node node_modules/@capacitor/cli/dist/index.js sync android', {
    stdio: 'inherit',
    env: process.env
  });
  console.log('Sync completed!');
  
  console.log('Building APK...');
  execSync('node node_modules/@capacitor/cli/dist/index.js build android', {
    stdio: 'inherit',
    env: process.env
  });
  console.log('Build completed!');
} catch (error) {
  console.error('Failed:', error.message);
  process.exit(1);
}
