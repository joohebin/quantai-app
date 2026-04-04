// check3.js - 读取时指定UTF-8编码
const fs = require('fs');
const code = fs.readFileSync('_check.js', {encoding:'utf8'});

const lines = code.split('\n');
console.log('Total lines:', lines.length);

// 使用 vm 模块做更准确的语法检查
const vm = require('vm');
try {
    new vm.Script(code);
    console.log('SYNTAX OK!');
} catch(e) {
    const msg = e.message;
    console.log('SYNTAX ERROR:', msg);
    // 从错误消息提取行号
    const m = e.stack.match(/:(\d+)\n/);
    if(m) {
        const errLine = parseInt(m[1]);
        console.log('Error at line:', errLine);
        for(let i = Math.max(0, errLine-4); i < Math.min(lines.length, errLine+2); i++) {
            const marker = i === errLine-1 ? '>>>' : '   ';
            console.log(`${marker} L${i+1}: ${lines[i].substring(0,150)}`);
        }
    }
}
