const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

const appDir = 'C:\\Users\\Administrator\\WorkBuddy\\Claw\\quantai-app\\mobile-app';
const androidDir = path.join(appDir, 'android');
const nodeExe = 'C:\\Program Files\\nodejs\\node.exe';
const npmExe = 'C:\\Program Files\\nodejs\\npm.cmd';

console.log('=== Capacitor Android Build ===\n');

// Remove old android if exists
if (fs.existsSync(androidDir)) {
    console.log('1. Removing old android folder...');
    fs.rmSync(androidDir, { recursive: true, force: true });
}

// Set environment
const env = {
    ...process.env,
    JAVA_HOME: 'C:\\Program Files\\Eclipse Adoptium\\jdk-21.0.10.7-hotspot',
    ANDROID_HOME: 'C:\\Users\\Administrator\\android-sdk',
    ANDROID_SDK_ROOT: 'C:\\Users\\Administrator\\android-sdk'
};

const capBin = path.join(appDir, 'node_modules', '@capacitor', 'cli', 'bin', 'cap');

// Add Android platform
console.log('\n2. Adding Android platform...');

return new Promise((resolve, reject) => {
    const addCmd = spawn(nodeExe, [capBin, 'add', 'android'], {
        cwd: appDir,
        env,
        shell: true,
        stdio: 'pipe'
    });

    addCmd.stdout.on('data', (data) => process.stdout.write(data.toString()));
    addCmd.stderr.on('data', (data) => process.stderr.write(data.toString()));

    addCmd.on('close', (code) => {
        console.log('\n--- Add Android Result:', code, '---');
        
        if (code === 0 && fs.existsSync(androidDir)) {
            console.log('✅ Android folder created!');
            
            console.log('\n3. Syncing web assets...');
            const syncCmd = spawn(nodeExe, [capBin, 'sync', 'android'], {
                cwd: appDir,
                env,
                shell: true,
                stdio: 'inherit'
            });
            
            syncCmd.on('close', (syncCode) => {
                if (syncCode === 0) {
                    console.log('\n4. Building APK...');
                    const buildCmd = spawn(nodeExe, [capBin, 'build', 'android'], {
                        cwd: appDir,
                        env,
                        shell: true,
                        stdio: 'inherit'
                    });
                    
                    buildCmd.on('close', (buildCode) => {
                        if (buildCode === 0) {
                            const apkPath = path.join(androidDir, 'app', 'build', 'outputs', 'apk', 'debug', 'app-debug.apk');
                            if (fs.existsSync(apkPath)) {
                                const stats = fs.statSync(apkPath);
                                console.log(`\n🎉 APK built!`);
                                console.log(`📦 ${apkPath}`);
                                console.log(`📊 Size: ${(stats.size / 1024 / 1024).toFixed(2)} MB`);
                            }
                        }
                        resolve(buildCode);
                    });
                } else {
                    resolve(syncCode);
                }
            });
        } else {
            console.log('❌ Android not created, checking what happened...');
            resolve(code || 1);
        }
    });
});
