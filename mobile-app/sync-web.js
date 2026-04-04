// Sync web content to Android assets
const fs = require('fs');
const path = require('path');

const srcDir = path.join(__dirname, 'www');
const destDir = path.join(__dirname, 'android', 'app', 'src', 'main', 'assets', 'public');

// Create destination directory
if (!fs.existsSync(destDir)) {
    fs.mkdirSync(destDir, { recursive: true });
}

// Copy all files from www to public
function copyDir(src, dest) {
    if (!fs.existsSync(src)) return;
    
    const entries = fs.readdirSync(src, { withFileTypes: true });
    
    for (const entry of entries) {
        const srcPath = path.join(src, entry.name);
        const destPath = path.join(dest, entry.name);
        
        if (entry.isDirectory()) {
            if (!fs.existsSync(destPath)) {
                fs.mkdirSync(destPath, { recursive: true });
            }
            copyDir(srcPath, destPath);
        } else {
            fs.copyFileSync(srcPath, destPath);
            console.log(`Copied: ${entry.name}`);
        }
    }
}

copyDir(srcDir, destDir);
console.log(`\n✅ Web content synced to ${destDir}`);
console.log(`Files: ${fs.readdirSync(destDir).length}`);
