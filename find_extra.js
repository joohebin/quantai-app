const fs = require('fs');
const content = fs.readFileSync('./index.html', 'utf8');

// Find I18N section
const start = content.indexOf('const I18N = {');
const end = content.indexOf('};', start) + 2;
const lines = content.substring(start, end).split('\n');

// Find all lines that are just },
let closingLines = [];
for (let i = 0; i < lines.length; i++) {
    if (lines[i].trim() === '},') {
        // Check if previous line also ends with },
        if (i > 0 && lines[i-1].trim().endsWith('},')) {
            console.log('Double }, at line', i + start.split('\n').length);
        }
        closingLines.push(i);
    }
}

console.log('Total }, lines:', closingLines.length);

// Show lines around closing braces
for (let i = 0; i < lines.length; i++) {
    if (lines[i].trim() === '},') {
        const prev = lines[i-1] ? lines[i-1].substring(0, 80) : '';
        const next = lines[i+1] ? lines[i+1].substring(0, 80) : '';
        console.log('Line', i + 1, ':');
        console.log('  Prev:', prev);
        console.log('  Curr:', lines[i].trim());
        console.log('  Next:', next);
    }
}
