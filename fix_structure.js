const fs = require('fs');
const content = fs.readFileSync('./index.html', 'utf8');

// Find I18N section
const start = content.indexOf('const I18N = {');
const end = content.indexOf('};', start) + 2;
const i18nSection = content.substring(0, end);
const restSection = content.substring(end);

const lines = i18nSection.split('\n');

// Languages that need fixing (they have ai_auto_trading_title after legal_title)
const langs = ['pt:', 'fr:', 'de:', 'nl:', 'pl:', 'tr:', 'th:', 'id:', 'vi:', 'hi:', 'ms:'];

let fixedLines = [];
let i = 0;
let skipNextClose = false;

while (i < lines.length) {
    const line = lines[i];
    
    // Check if this line contains legal_title and ends with },
    if (line.includes('legal_title:') && line.trim().endsWith('},')) {
        // This is the closing of a language block, but we need to add ai_auto_trading_title first
        // Remove the }, and add ai_auto_trading_title
        const fixedLine = line.replace(/},$/, ',');
        fixedLines.push(fixedLine);
        skipNextClose = true;
        console.log('Fixed line', i + 1, '- added comma instead of },');
    }
    // Check if this is a standalone }, that we should skip
    else if (line.trim() === '},' && skipNextClose) {
        skipNextClose = false;
        console.log('Skipped duplicate }, at line', i + 1);
    }
    else {
        fixedLines.push(line);
    }
    i++;
}

const fixedContent = fixedLines.join('\n') + '\n' + restSection;
fs.writeFileSync('./index.html', fixedContent);
console.log('Done!');
