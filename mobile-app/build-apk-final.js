const fs = require('fs');
const https = require('https');
const path = require('path');

const androidDir = 'C:\\Users\\Administrator\\WorkBuddy\\Claw\\quantai-app\\mobile-app\\android';
const wrapperJar = path.join(androidDir, 'gradle', 'wrapper', 'gradle-wrapper.jar');

console.log('Downloading gradle-wrapper.jar...');

// Download gradle-wrapper.jar
const url = 'https://raw.githubusercontent.com/gradle/gradle/v8.2.1/gradle/wrapper/gradle-wrapper.jar';
const file = fs.createWriteStream(wrapperJar);

https.get(url, (response) => {
    if (response.statusCode === 200) {
        response.pipe(file);
        file.on('finish', () => {
            file.close();
            console.log('✅ Downloaded gradle-wrapper.jar');
            
            // Now build
            const { spawn } = require('child_process');
            
            const env = {
                ...process.env,
                JAVA_HOME: 'C:\\Program Files\\Eclipse Adoptium\\jdk-21.0.10.7-hotspot',
                ANDROID_HOME: 'C:\\Users\\Administrator\\android-sdk',
                ANDROID_SDK_ROOT: 'C:\\Users\\Administrator\\android-sdk'
            };
            
            console.log('\nBuilding APK...');
            const gradlew = path.join(androidDir, 'gradlew.bat');
            
            const build = spawn(gradlew, ['assembleDebug', '--no-daemon'], {
                cwd: androidDir,
                env,
                shell: true,
                stdio: 'inherit'
            });
            
            build.on('close', (code) => {
                console.log('\nBuild exit code:', code);
                
                if (code === 0) {
                    const apkPath = path.join(androidDir, 'app', 'build', 'outputs', 'apk', 'debug', 'app-debug.apk');
                    if (fs.existsSync(apkPath)) {
                        const stats = fs.statSync(apkPath);
                        console.log(`\n🎉 APK built successfully!`);
                        console.log(`📦 ${apkPath}`);
                        console.log(`📊 Size: ${(stats.size / 1024 / 1024).toFixed(2)} MB`);
                    }
                }
            });
        });
    } else {
        console.error('Failed to download:', response.statusCode);
        process.exit(1);
    }
}).on('error', (err) => {
    console.error('Download error:', err);
    process.exit(1);
});
