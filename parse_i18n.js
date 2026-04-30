const fs = require('fs');
const content = fs.readFileSync('./index.html', 'utf8');

// Find I18N section
const start = content.indexOf('const I18N = {');
const end = content.indexOf('};', start) + 2;
const i18nSection = content.substring(start, end);

// Try to parse as JavaScript
try {
    const result = new Function('return ' + i18nSection.replace('const I18N = ', ''));
    result(); // Execute to trigger syntax error
    console.log('Parsed successfully!');
} catch (e) {
    console.log('Parse error:', e.message);
    
    // Try to find the error position
    const lines = i18nSection.split('\n');
    for (let i = 0; i < lines.length; i++) {
        // Try parsing up to this line
        try {
            const partial = lines.slice(0, i + 1).join('\n');
            new Function('return ' + partial.replace('const I18N = ', ''));
        } catch (e2) {
            if (e2.message !== e.message) {
                console.log('Error first appears at line', i + 1, ':', lines[i].substring(0, 80));
                console.log('  Error:', e2.message);
                break;
            }
        }
    }
}
