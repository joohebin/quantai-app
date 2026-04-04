const fs = require('fs');
const path = require('path');
const https = require('https');
const zlib = require('zlib');
const { spawn } = require('child_process');

const gradleDir = 'C:\\gradle';
const gradleHome = path.join(gradleDir, 'gradle-8.2');
const gradleBin = path.join(gradleHome, 'bin', 'gradle');
const gradleBat = path.join(gradleHome, 'bin', 'gradle.bat');

console.log('=== Installing Gradle 8.2 ===\n');

async function downloadGradle() {
    return new Promise((resolve, reject) => {
        // Create directories
        if (!fs.existsSync(gradleDir)) {
            fs.mkdirSync(gradleDir, { recursive: true });
        }
        
        // Download gradle zip
        const url = 'https://services.gradle.org/distributions/gradle-8.2-bin.zip';
        const zipPath = path.join(gradleDir, 'gradle-8.2-bin.zip');
        
        console.log('Downloading Gradle 8.2...');
        console.log('URL:', url);
        
        const file = fs.createWriteStream(zipPath);
        
        https.get(url, (response) => {
            console.log('Status:', response.statusCode);
            
            if (response.statusCode === 200) {
                response.pipe(file);
                file.on('finish', () => {
                    file.close();
                    console.log('Downloaded!');
                    
                    // Extract
                    console.log('Extracting...');
                    const extract = spawn('powershell', [
                        '-Command',
                        `Expand-Archive -Path '${zipPath}' -DestinationPath '${gradleDir}' -Force`
                    ], { stdio: 'inherit' });
                    
                    extract.on('close', (code) => {
                        console.log('Extract exit code:', code);
                        
                        if (fs.existsSync(gradleBat)) {
                            console.log('✅ Gradle installed!');
                            
                            // Build APK
                            buildAPK(gradleBat);
                        } else {
                            console.log('❌ Gradle not found at expected path');
                            reject(new Error('Install failed'));
                        }
                    });
                });
            } else {
                reject(new Error(`Download failed: ${response.statusCode}`));
            }
        }).on('error', reject);
    });
}

function buildAPK(gradleCmd) {
    const androidDir = 'C:\\Users\\Administrator\\WorkBuddy\\Claw\\quantai-app\\mobile-app\\android';
    
    console.log('\n=== Building APK ===\n');
    
    const env = {
        ...process.env,
        JAVA_HOME: 'C:\\Program Files\\Eclipse Adoptium\\jdk-21.0.10.7-hotspot',
        ANDROID_HOME: 'C:\\Users\\Administrator\\android-sdk',
        ANDROID_SDK_ROOT: 'C:\\Users\\Administrator\\android-sdk',
        GRADLE_HOME: gradleHome
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

downloadGradle().catch(console.error);
