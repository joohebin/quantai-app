const fs = require('fs');
const content = fs.readFileSync('./index.html', 'utf8');
const lines = content.split('\n');

// Find all cases where a line ending with '},' is followed by ai_auto_trading_title
let fixed = [];
let i = 0;
let removedCount = 0;

while (i < lines.length) {
    const line = lines[i];
    
    // Check if this line ends with }, and next line has ai_auto_trading_title
    if (line.trim() === '},' && i + 1 < lines.length && lines[i + 1].includes('ai_auto_trading_title')) {
        // Remove this }, line and the ai_auto_trading_title line
        // Change previous line from , to },
        if (fixed.length > 0) {
            const prevLine = fixed[fixed.length - 1];
            // Remove trailing , and add },
            fixed[fixed.length - 1] = prevLine.replace(/,(\s*)$/, '},$1');
        }
        // Skip the }, line
        i++;
        // Skip the ai_auto_trading_title line
        i++;
        removedCount += 2;
        console.log('Merged at line', i);
        
        // Also check if there's a comment line like // xxx},
        if (i < lines.length && lines[i].match(/^\s+\/\/ .+\},/)) {
            i++;
            removedCount++;
            console.log('Removed comment line');
        }
    }
    else if (line.match(/^\s+\/\/ .+\},/)) {
        // Skip standalone comment lines with },
        i++;
        removedCount++;
        console.log('Removed standalone comment line');
    }
    else {
        fixed.push(line);
        i++;
    }
}

fs.writeFileSync('./index.html', fixed.join('\n'));
console.log('Removed', removedCount, 'lines');
