const { spawn } = require('child_process');
const path = require('path');

const androidDir = 'C:\\Users\\Administrator\\WorkBuddy\\Claw\\quantai-app\\mobile-app\\android';

console.log('Starting APK build...');

// Set environment
const env = {
  ...process.env,
  JAVA_HOME: 'C:\\Program Files\\Eclipse Adoptium\\jdk-21.0.10.7-hotspot',
  ANDROID_HOME: 'C:\\Users\\Administrator\\android-sdk',
  ANDROID_SDK_ROOT: 'C:\\Users\\Administrator\\android-sdk'
};

const gradlew = path.join(androidDir, 'gradlew.bat');
const args = ['assembleDebug', '--stacktrace'];

console.log('Running Gradle build...');

const gradle = spawn(gradlew, args, {
  cwd: androidDir,
  env: env,
  shell: true,
  stdio: 'pipe'
});

gradle.stdout.on('data', (data) => {
  process.stdout.write(data.toString());
});

gradle.stderr.on('data', (data) => {
  process.stderr.write(data.toString());
});

gradle.on('close', (code) => {
  console.log(`\nGradle process exited with code ${code}`);
  
  if (code === 0) {
    // Check for APK
    const apkDir = path.join(androidDir, 'app', 'build', 'outputs', 'apk', 'debug');
    const apkPath = path.join(apkDir, 'app-debug.apk');
    
    const fs = require('fs');
    if (fs.existsSync(apkPath)) {
      const stats = fs.statSync(apkPath);
      console.log(`\n✅ APK built successfully!`);
      console.log(`📦 Location: ${apkPath}`);
      console.log(`📊 Size: ${(stats.size / 1024 / 1024).toFixed(2)} MB`);
    } else {
      console.log('APK not found, checking build directory...');
      if (fs.existsSync(apkDir)) {
        console.log('Contents:', fs.readdirSync(apkDir));
      }
    }
  } else {
    console.log('Build failed!');
  }
  
  process.exit(code);
});
