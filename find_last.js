const fs = require('fs');
const content = fs.readFileSync('./index.html', 'utf8');

// Find I18N section
const start = content.indexOf('const I18N = {');
const end = content.indexOf('};', start) + 2;
const i18nSection = content.substring(start, end);

const lines = i18nSection.split('\n');

// Track bracket balance
let bracketCount = 0;
let expectedLang = false;

for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    
    // Skip strings for bracket counting
    let inString = false;
    let stringChar = '';
    for (let j = 0; j < line.length; j++) {
        const ch = line[j];
        if (!inString) {
            if (ch === '"' || ch === "'" || ch === '`') {
                inString = true;
                stringChar = ch;
            } else if (ch === '{') {
                bracketCount++;
            } else if (ch === '}') {
                bracketCount--;
                if (bracketCount === 1 && line.includes(': {')) {
                    // Found a language block
                    console.log('Line', i + 1, ': Language block starts, bracket count =', bracketCount);
                }
            }
        } else {
            if (ch === stringChar && line[j-1] !== '\\') {
                inString = false;
            }
        }
    }
    
    // Show lines where bracket count is negative
    if (bracketCount < 0) {
        console.log('Negative bracket at line', i + 1, ':', line.substring(0, 80));
        console.log('  Balance:', bracketCount);
    }
}

console.log('Final bracket count:', bracketCount);
