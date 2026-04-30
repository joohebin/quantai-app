const fs = require('fs');
const content = fs.readFileSync('./index.html', 'utf8');

// Remove all these comment lines that have }, at the end
const patterns = [
    '  // Français},\n',
    '  // Deutsch},\n',
    '  // Turkce},\n',
    '  // Thai},\n',
    '  // Bahasa Indonesia},\n',
    '  // Tiếng Việt},\n',
    '  // हिन्दी (Hindi)},\n',
    '  // Bahasa Melayu (Malay)},\n'
];

let fixed = content;
patterns.forEach(p => {
    if (fixed.includes(p)) {
        fixed = fixed.replace(p, '');
        console.log('Removed:', p.trim());
    } else {
        console.log('Not found:', p.trim());
    }
});

fs.writeFileSync('./index.html', fixed);
console.log('Done!');
