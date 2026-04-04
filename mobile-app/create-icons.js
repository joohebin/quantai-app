const fs = require('fs');
const path = require('path');

// Create a simple PNG icon using raw bytes (green square)
function createPNG(width, height) {
    // Simple PNG: minimal valid PNG with green color
    const png = Buffer.from([
        0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A, // PNG signature
        0x00, 0x00, 0x00, 0x0D, // IHDR length
        0x49, 0x48, 0x44, 0x52, // IHDR
        (width >> 24) & 0xFF, (width >> 16) & 0xFF, (width >> 8) & 0xFF, width & 0xFF, // width
        (height >> 24) & 0xFF, (height >> 16) & 0xFF, (height >> 8) & 0xFF, height & 0xFF, // height
        0x08, // bit depth
        0x02, // color type (RGB)
        0x00, // compression
        0x00, // filter
        0x00, // interlace
        0x00, 0x00, 0x00, 0x00, // CRC placeholder
    ]);
    
    // For simplicity, create a minimal valid PNG
    // This is a 1x1 green pixel PNG
    return Buffer.from([
        0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A,
        0x00, 0x00, 0x00, 0x0D, 0x49, 0x48, 0x44, 0x52,
        0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01,
        0x08, 0x02, 0x00, 0x00, 0x00, 0x90, 0x77, 0x53,
        0xDE, 0x00, 0x00, 0x00, 0x0C, 0x49, 0x44, 0x41,
        0x54, 0x08, 0xD7, 0x63, 0x60, 0x60, 0x60, 0x00,
        0x00, 0x00, 0x82, 0x00, 0x01, 0x00, 0x31, 0x7E,
        0xFC, 0xD6, 0x00, 0x00, 0x00, 0x00, 0x49, 0x45,
        0x4E, 0x44, 0xAE, 0x42, 0x60, 0x82
    ]);
}

const baseDir = 'C:\\Users\\Administrator\\WorkBuddy\\Claw\\quantai-app\\mobile-app\\android\\app\\src\\main\\res';

// Icon sizes for mipmap
const sizes = [
    { name: 'mipmap-mdpi', size: 48 },
    { name: 'mipmap-hdpi', size: 72 },
    { name: 'mipmap-xhdpi', size: 96 },
    { name: 'mipmap-xxhdpi', size: 144 },
    { name: 'mipmap-xxxhdpi', size: 192 },
];

// Create a simple colored icon using HTML Canvas equivalent - base64 PNG
const greenIconBase64 = 'iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAACXBIWXMAAAsTAAALEwEAmpwYAAABKElEQVR4nO2YQQ6CMBCG/0t6ER1YuHEBHoEn0Im7HsSNgZsgF+BiYOFCB04sLGwM0IPY0C70QpCWtE37TyYUCARBEARBEHoGegbU/9o7cACsgI0ZxA4YARtgY8axA0bAxgx0Z9A5QO8A3QP0DtA7QO8AvQP0DtA7QO8AvQP0DtA7QO8AvQP0DtA7QO8AvQP0DtA7QO8AvQP0DtA7QO8AvQP0DtA7QO8AvQP0DtA7QO8AvQP0DtA7QO8AvQP0DtA7QO8AvQP0DtA7QO8AvQP0DtA7QO8AvQP0DtA7QO8AvQP0DtA7QO8AvQP0DtA7QO8AvQP0DtA7QO8AvQP0DtA7QO8AvQP0DtA7QO8AvQP0DtA7QO8AvQP0DtA7QO8AvQP0DtA7QO8AvQP0DlACgH8B6B2gd4DeAXoH6B2gd4DeAXoH6B2gd4DeAXoH6B0g7QHpHaB3gN4BegfoHaB3gN4BfgFOgR4K0D8K5wAAAABJRU5ErkJggg==';

const iconBuffer = Buffer.from(greenIconBase64, 'base64');

sizes.forEach(({ name, size }) => {
    const dir = path.join(baseDir, name);
    fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(path.join(dir, 'ic_launcher.png'), iconBuffer);
    console.log(`Created ${name}/ic_launcher.png`);
});

// Create mipmap-anydpi-v26 adaptive icon
const anydpiDir = path.join(baseDir, 'mipmap-anydpi-v26');
fs.mkdirSync(anydpiDir, { recursive: true });

// Create adaptive icon XMLs
const ic_launcherXml = `<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@color/ic_launcher_background"/>
    <foreground android:drawable="@drawable/ic_launcher_foreground"/>
</adaptive-icon>`;

const ic_launcherForeground = `<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
    <path
        android:fillColor="#00C896"
        android:pathData="M54,54m-40,0a40,40 0,1 1,80 0a40,40 0,1 1,-80 0"/>
    <path
        android:fillColor="#FFFFFF"
        android:pathData="M44,44L64,54L44,64Z"/>
</vector>`;

fs.writeFileSync(path.join(anydpiDir, 'ic_launcher.xml'), ic_launcherXml);
fs.writeFileSync(path.join(baseDir, 'drawable', 'ic_launcher_foreground.xml'), ic_launcherForeground);

// Create color resource for background
const colorsXml = `<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="ic_launcher_background">#FFFFFF</color>
</resources>`;
fs.writeFileSync(path.join(baseDir, 'values', 'colors.xml'), colorsXml);

console.log('\n✅ Icons created!');
