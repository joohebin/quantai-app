const fs = require('fs');
const https = require('https');
const path = require('path');

const androidDir = 'C:\\Users\\Administrator\\WorkBuddy\\Claw\\quantai-app\\mobile-app\\android';
const wrapperDir = path.join(androidDir, 'gradle', 'wrapper');
const wrapperJar = path.join(wrapperDir, 'gradle-wrapper.jar');

// First try: gradle repo
const urls = [
    'https://raw.githubusercontent.com/nicferrier/gradle/master/gradle/wrapper/gradle-wrapper.jar',
    'https://github.com/nicferrier/gradle/raw/master/gradle/wrapper/gradle-wrapper.jar',
];

function tryDownload(urlIndex = 0) {
    if (urlIndex >= urls.length) {
        console.log('All downloads failed, trying alternative method...');
        // Create a minimal gradlew that uses gradle directly
        createGradlewWithoutWrapper();
        return;
    }
    
    console.log(`Trying URL ${urlIndex + 1}: ${urls[urlIndex]}`);
    
    const file = fs.createWriteStream(wrapperJar);
    
    https.get(urls[urlIndex], (response) => {
        console.log('Status:', response.statusCode);
        
        if (response.statusCode === 200) {
            response.pipe(file);
            file.on('finish', () => {
                file.close();
                const stats = fs.statSync(wrapperJar);
                console.log(`Downloaded: ${stats.size} bytes`);
                
                if (stats.size > 50000) {
                    console.log('✅ Valid gradle-wrapper.jar!');
                } else {
                    console.log('⚠️ File too small, trying next URL...');
                    tryDownload(urlIndex + 1);
                }
            });
        } else {
            tryDownload(urlIndex + 1);
        }
    }).on('error', (err) => {
        console.error('Error:', err.message);
        tryDownload(urlIndex + 1);
    });
}

function createGradlewWithoutWrapper() {
    // Create gradlew that uses gradle installed via other means
    const gradlewBat = path.join(androidDir, 'gradlew.bat');
    const gradlewSh = path.join(androidDir, 'gradlew');
    
    const batContent = `@echo off
setlocal
set DIRNAME=%~dp0
set APP_HOME=%DIRNAME%

rem Try to find gradle
set GRADLE_HOME=%USERPROFILE%\\.gradle
if exist "%GRADLE_HOME%\\wrapper\\dists\\gradle-8.2.1-bin\\*" (
    for /d %%i in ("%GRADLE_HOME%\\wrapper\\dists\\gradle-8.2.1-bin\\*") do set GRADLE_HOME=%%i
)

rem Use JAVA_HOME
set JAVA_HOME=C:\\Program Files\\Eclipse Adoptium\\jdk-21.0.10.7-hotspot

rem Find gradle in PATH or common locations
where gradle >nul 2>&1
if %errorlevel% equ 0 (
    gradle %*
) else (
    rem Try to use gradle from Android Studio
    if exist "C:\\Program Files\\Android\\Android Studio\\plugins\\gradle" (
        echo Gradle not found. Please install Gradle or use Android Studio.
        exit /b 1
    )
)

exit /b %errorlevel%
`;
    
    fs.writeFileSync(gradlewBat, batContent);
    console.log('Created fallback gradlew.bat');
}

tryDownload();
