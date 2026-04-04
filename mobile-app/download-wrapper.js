const fs = require('fs');
const http = require('http');
const path = require('path');

const androidDir = 'C:\\Users\\Administrator\\WorkBuddy\\Claw\\quantai-app\\mobile-app\\android';
const wrapperJar = path.join(androidDir, 'gradle', 'wrapper', 'gradle-wrapper.jar');

console.log('Downloading gradle-wrapper.jar...');

// Use Maven Central
const url = 'https://repo1.maven.org/maven2/org/gradle/gradle-tooling/8.2/gradle-tooling-8.2.jar';

http.get(url, (response) => {
    console.log('Status:', response.statusCode);
    
    if (response.statusCode === 200) {
        const file = fs.createWriteStream(wrapperJar);
        response.pipe(file);
        file.on('finish', () => {
            file.close();
            const stats = fs.statSync(wrapperJar);
            console.log(`Downloaded: ${stats.size} bytes`);
            
            if (stats.size < 1000) {
                console.log('⚠️ File too small, might be error page');
                console.log(fs.readFileSync(wrapperJar, 'utf8').substring(0, 200));
            }
        });
    } else {
        console.log('Trying alternative URL...');
        // Try gradle wrapper from github releases
        const altUrl = 'https://github.com/nicferrier/gradle/raw/master/gradle/wrapper/gradle-wrapper.jar';
        http.get(altUrl, (res2) => {
            if (res2.statusCode === 200) {
                const file2 = fs.createWriteStream(wrapperJar);
                res2.pipe(file2);
                file2.on('finish', () => {
                    console.log('Downloaded from alternative');
                });
            }
        });
    }
}).on('error', (err) => console.error(err));
