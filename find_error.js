const fs = require('fs');
const content = fs.readFileSync('./index.html', 'utf8');

// Find the second script block (the main one)
const scripts = content.match(/<script>([\s\S]*?)<\/script>/g);
if (scripts && scripts.length >= 2) {
    const mainScript = scripts[1]; // Second script block
    const inner = mainScript.replace(/<\/?script>/g, '');
    
    // Try to find the error by checking line by line
    const lines = inner.split('\n');
    
    // Simple bracket matching to find potential issues
    let bracketCount = 0;
    let objCount = 0;
    let inString = false;
    let stringChar = '';
    let lineNum = 0;
    
    for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        if (line.includes('const I18N')) {
            console.log('Found I18N at line', i + 2072);
            // Start tracking
            for (let j = i; j < lines.length; j++) {
                const l = lines[j];
                for (let k = 0; k < l.length; k++) {
                    const ch = l[k];
                    if (!inString) {
                        if (ch === '"' || ch === "'" || ch === '`') {
                            inString = true;
                            stringChar = ch;
                        } else if (ch === '{') {
                            objCount++;
                        } else if (ch === '}') {
                            objCount--;
                        }
                    } else {
                        if (ch === stringChar && l[k-1] !== '\\') {
                            inString = false;
                        }
                    }
                }
                if (l.includes('pt:') || l.includes('ru:') || l.includes('ko:')) {
                    console.log('Language block at line', j + 2072, ':', l.substring(0, 50));
                    console.log('  Bracket balance:', objCount);
                }
            }
            break;
        }
    }
}
