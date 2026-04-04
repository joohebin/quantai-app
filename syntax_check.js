// syntax_check.js - 用 Node 解析 HTML 中提取的 JS 块并检查语法
const fs = require('fs');

// 读取 _main.js（UTF-8）
let js;
try {
    js = fs.readFileSync('_main.js', 'utf8');
} catch(e) {
    console.error('Cannot read _main.js:', e.message);
    process.exit(1);
}

// 用 new Function 做语法检查（不执行）
try {
    new Function(js);
    console.log('SYNTAX OK');
} catch(e) {
    // 提取行号
    const msg = e.toString();
    console.log('SYNTAX ERROR:', msg);
    
    // 尝试定位行
    const lineMatch = msg.match(/<anonymous>:(\d+)/);
    if(lineMatch) {
        const errLine = parseInt(lineMatch[1]) - 1; // new Function 包了一层
        const lines = js.split('\n');
        console.log('\nContext:');
        for(let i = Math.max(0, errLine-3); i < Math.min(lines.length, errLine+3); i++) {
            const marker = i === errLine - 1 ? '>>>' : '   ';
            console.log(`${marker} L${i+1}: ${lines[i].substring(0,120)}`);
        }
    }
}
