process.chdir('C:\\Users\\Administrator\\WorkBuddy\\Claw\\quantai-app\\mobile-app');
const fs = require('fs');
const path = require('path');
const tar = require('tar');

const projectDir = 'C:\\Users\\Administrator\\WorkBuddy\\Claw\\quantai-app\\mobile-app';
const androidDir = path.join(projectDir, 'android');
const sdkPath = 'C:\\Users\\Administrator\\android-sdk';

(async () => {
    console.log('=== 1. 提取 Android 模板 ===');
    const templatePath = path.join(projectDir, 'node_modules', '@capacitor', 'cli', 'assets', 'android-template.tar.gz');
    
    if (!fs.existsSync(androidDir)) {
        fs.mkdirSync(androidDir, { recursive: true });
    }
    
    await tar.extract({ file: templatePath, cwd: androidDir });
    console.log('✅ 模板提取完成');
    console.log('android 目录内容:', fs.readdirSync(androidDir));
    
    console.log('\n=== 2. 创建 local.properties ===');
    const localProps = `sdk.dir=${sdkPath.replace(/\\/g, '\\\\')}`;
    fs.writeFileSync(path.join(androidDir, 'local.properties'), localProps);
    console.log('✅ local.properties 已创建');
    
    console.log('\n=== 3. 创建 Gradle 配置文件 ===');
    
    // 创建 capacitor.settings.gradle
    const settingsContent = `// GENERATED
include ':capacitor-android'
project(':capacitor-android').projectDir = new File('../node_modules/@capacitor/android/capacitor')

include ':capacitor-cordova-android-plugins'
project(':capacitor-cordova-android-plugins').projectDir = new File('./capacitor-cordova-android-plugins/')
`;
    fs.writeFileSync(path.join(androidDir, 'capacitor.settings.gradle'), settingsContent);
    console.log('✅ capacitor.settings.gradle 已创建');
    
    // 创建 cordova plugins 目录和文件
    const cordovaDir = path.join(androidDir, 'capacitor-cordova-android-plugins');
    if (!fs.existsSync(cordovaDir)) {
        fs.mkdirSync(cordovaDir, { recursive: true });
    }
    
    fs.writeFileSync(path.join(cordovaDir, 'build.gradle'), `
ext {
  cdvMinSdkVersion = 22
}
dependencies {}
`);
    
    fs.writeFileSync(path.join(cordovaDir, 'cordova.variables.gradle'), `
ext {
  cdvMinSdkVersion = project.hasProperty('minSdkVersion') ? rootProject.ext.minSdkVersion : 22
  cdvPluginPostBuildExtras = []
  cordovaConfig = [:]
}
`);
    
    fs.writeFileSync(path.join(cordovaDir, 'cdv-build.gradle'), `
android {
    compileSdkVersion rootProject.ext.androidCompileSdkVersion
    defaultConfig {
        minSdkVersion rootProject.ext.androidMinSdkVersion
        targetSdkVersion rootProject.ext.androidTargetSdkVersion
    }
}
`);
    console.log('✅ Cordova 插件配置已创建');
    
    // 创建 app/capacitor.build.gradle
    const appDir = path.join(androidDir, 'app');
    fs.writeFileSync(path.join(appDir, 'capacitor.build.gradle'), `
android {
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_17
        targetCompatibility JavaVersion.VERSION_17
    }
}

apply from: '../capacitor-cordova-android-plugins/cordova.variables.gradle'
dependencies {
    implementation project(':capacitor-android')
}
`);
    console.log('✅ app/capacitor.build.gradle 已创建');
    
    console.log('\n=== 4. 同步 Web 资源 ===');
    const webDir = path.join(appDir, 'src', 'main', 'assets', 'public');
    if (!fs.existsSync(webDir)) {
        fs.mkdirSync(webDir, { recursive: true });
    }
    
    const wwwDir = path.join(projectDir, 'www');
    if (fs.existsSync(wwwDir)) {
        const wwwFiles = fs.readdirSync(wwwDir);
        wwwFiles.forEach(file => {
            const src = path.join(wwwDir, file);
            const dest = path.join(webDir, file);
            fs.copyFileSync(src, dest);
            console.log(`  复制: ${file}`);
        });
    }
    console.log('✅ Web 资源已同步');
    
    console.log('\n=== 5. 开始构建 APK ===');
    const { spawn } = require('child_process');
    
    const env = {
        ...process.env,
        JAVA_HOME: 'C:\\Program Files\\Eclipse Adoptium\\jdk-21.0.10.7-hotspot',
        ANDROID_HOME: sdkPath,
        ANDROID_SDK_ROOT: sdkPath,
        PATH: `C:\\Program Files\\Eclipse Adoptium\\jdk-21.0.10.7-hotspot\\bin;${sdkPath}\\platform-tools;${sdkPath}\\cmdline-tools\\latest\\bin;C:\\Windows\\system32;C:\\Windows;C:\\Windows\\System32\\Wbem`
    };
    
    return new Promise((resolve, reject) => {
        const child = spawn('cmd.exe', ['/c', 'gradlew.bat', 'assembleDebug'], {
            cwd: androidDir,
            env: env,
            stdio: 'inherit'
        });
        
        child.on('close', (code) => {
            if (code === 0) {
                console.log('\n✅ Gradle 构建成功');
                
                // 检查 APK
                const apkDir = path.join(androidDir, 'app', 'build', 'outputs', 'apk', 'debug');
                if (fs.existsSync(apkDir)) {
                    const files = fs.readdirSync(apkDir).filter(f => f.endsWith('.apk'));
                    if (files.length > 0) {
                        files.forEach(f => {
                            const fullPath = path.join(apkDir, f);
                            const size = (fs.statSync(fullPath).size / 1024 / 1024).toFixed(2);
                            console.log(`\n🎉 APK 已生成!`);
                            console.log(`   文件: ${f}`);
                            console.log(`   大小: ${size} MB`);
                            console.log(`   路径: ${fullPath}`);
                        });
                    }
                }
                resolve();
            } else {
                console.log(`\n❌ Gradle 构建失败，退出码: ${code}`);
                reject(code);
            }
        });
        
        child.on('error', reject);
    });
})().catch(err => console.error('错误:', err));
