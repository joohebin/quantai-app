const fs = require('fs');
const content = fs.readFileSync('./index.html', 'utf8');

// Find I18N section
const start = content.indexOf('const I18N = {');
const end = content.indexOf('};', start) + 2;
const i18nSection = content.substring(start, end);

// Count braces outside of strings
let bracketCount = 0;
let inString = false;
let stringChar = '';
let lineNum = 0;
let lines = i18nSection.split('\n');

for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
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
                if (bracketCount === 0 && j === line.length - 1) {
                    // Found the end
                    console.log('End of I18N at line', i + 1);
                }
            }
        } else {
            if (ch === stringChar && line[j-1] !== '\\') {
                inString = false;
            }
        }
    }
    
    // Show problematic lines
    if (line.trim() === '};' && bracketCount < 0) {
        console.log('Extra }; at line', i + 1);
        console.log('Context:');
        for (let k = Math.max(0, i-3); k <= Math.min(lines.length-1, i+3); k++) {
            console.log('  Line', k+1, ':', lines[k].substring(0, 100));
        }
    }
}

console.log('Final bracket count:', bracketCount);
