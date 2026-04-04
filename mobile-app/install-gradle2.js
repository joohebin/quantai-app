const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

const gradleDir = 'C:\\gradle';
const gradleHome = path.join(gradleDir, 'gradle-8.2');
const zipPath = path.join(gradleDir, 'gradle-8.2-bin.zip');

console.log('=== Installing Gradle 8.2 ===\n');

// Create directory
if (!fs.existsSync(gradleDir)) {
    fs.mkdirSync(gradleDir, { recursive: true });
}

async function main() {
    // Download using PowerShell
    if (!fs.existsSync(zipPath)) {
        console.log('Downloading Gradle 8.2...');
        const dl = spawn('powershell', [
            '-Command',
            `Invoke-WebRequest -Uri 'https://services.gradle.org/distributions/gradle-8.2-bin.zip' -OutFile '${zipPath}'`
        ], { stdio: 'inherit' });
        
        await new Promise((resolve, reject) => {
            dl.on('close', (code) => {
                if (code === 0) resolve();
                else reject(new Error('Download failed'));
            });
        });
    } else {
        console.log('Zip already exists');
    }
    
    // Extract
    console.log('\nExtracting...');
    const extract = spawn('powershell', [
        '-Command',
        `Expand-Archive -Path '${zipPath}' -DestinationPath '${gradleDir}' -Force`
    ], { stdio: 'inherit' });
    
    await new Promise((resolve, reject) => {
        extract.on('close', (code) => {
            if (code === 0) resolve();
            else reject(new Error('Extract failed'));
        });
    });
    
    const gradleBat = path.join(gradleHome, 'bin', 'gradle.bat');
    
    if (fs.existsSync(gradleBat)) {
        console.log('\n✅ Gradle installed!');
        
        // Build APK
        buildAPK(gradleBat);
    } else {
        console.log('❌ Gradle not found');
    }
}

function buildAPK(gradleCmd) {
    const androidDir = 'C:\\Users\\Administrator\\WorkBuddy\\Claw\\quantai-app\\mobile-app\\android';
    
    console.log('\n=== Building APK ===\n');
    
    const env = {
        ...process.env,
        JAVA_HOME: 'C:\\Program Files\\Eclipse Adoptium\\jdk-21.0.10.7-hotspot',
        ANDROID_HOME: 'C:\\Users\\Administrator\\android-sdk',
        ANDROID_SDK_ROOT: 'C:\\Users\\Administrator\\android-sdk'
    };
    
    const build = spawn(gradleCmd, ['assembleDebug', '--no-daemon'], {
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
        } else {
            console.log('❌ Build failed');
        }
    });
}

main().catch(console.error);
