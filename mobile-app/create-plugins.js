const fs = require('fs');
const path = require('path');

const baseDir = 'C:\\Users\\Administrator\\WorkBuddy\\Claw\\quantai-app\\mobile-app\\android\\capacitor-cordova-android-plugins';

// Create directory structure
const dirs = [
    path.join(baseDir, 'src', 'main', 'java'),
    path.join(baseDir, 'src', 'main', 'libs'),
    path.join(baseDir, 'src', 'main', 'res'),
];

dirs.forEach(dir => {
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
        console.log('Created:', dir);
    }
});

// Create build.gradle
const buildGradle = `
apply plugin: 'com.android.library'

android {
    namespace "com.cordova.plugins"
    compileSdk rootProject.ext.compileSdkVersion
    
    defaultConfig {
        minSdkVersion rootProject.ext.minSdkVersion
        targetSdkVersion rootProject.ext.targetSdkVersion
        versionCode 1
        versionName "1.0"
    }
    
    lintOptions {
        abortOnError false
    }
    
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_17
        targetCompatibility JavaVersion.VERSION_17
    }
}

repositories {
    google()
    mavenCentral()
    flatDir { dirs 'src/main/libs', 'libs' }
}

dependencies {
    implementation fileTree(include: ['*.jar'], dir: 'src/main/libs')
    implementation "androidx.appcompat:appcompat:$androidxAppCompatVersion"
}
`;

fs.writeFileSync(path.join(baseDir, 'build.gradle'), buildGradle);
console.log('Created build.gradle');

// Create gradle.properties
const gradleProperties = `
android.useAndroidX=true
android.enableJetifier=true
`;

fs.writeFileSync(path.join(baseDir, 'gradle.properties'), gradleProperties);
console.log('Created gradle.properties');

// Create AndroidManifest.xml
const manifest = `<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
</manifest>
`;

fs.writeFileSync(path.join(baseDir, 'src', 'main', 'AndroidManifest.xml'), manifest);
console.log('Created AndroidManifest.xml');

console.log('\\nCordova plugins module created successfully!');
