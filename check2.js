// check2.js - 用 Node 运行时语法检查，正确处理 UTF-8
process.stdin.setEncoding('utf8');

const fs = require('fs');
const code = fs.readFileSync('_check.js', {encoding:'utf8'});

// 逐步缩小范围：二分查找错误位置
const lines = code.split('\n');
console.log('Total lines:', lines.length);

function tryParse(subset) {
    try {
        new Function(subset);
        return true;
    } catch(e) {
        return false;
    }
}

// 先检查全文
if(tryParse(code)) {
    console.log('FULL CODE: SYNTAX OK');
    process.exit(0);
}
console.log('FULL CODE: HAS SYNTAX ERROR - binary searching...');

// 二分查找最小错误位置
let lo = 1, hi = lines.length;
while(lo < hi) {
    const mid = Math.floor((lo + hi) / 2);
    const partial = lines.slice(0, mid).join('\n');
    if(tryParse(partial)) {
        lo = mid + 1;
    } else {
        hi = mid;
    }
}

console.log(`\nError likely around line: ${lo}`);
console.log('Context:');
for(let i = Math.max(0, lo-5); i < Math.min(lines.length, lo+3); i++) {
    const marker = i === lo-1 ? '>>>' : '   ';
    console.log(`${marker} L${i+1}: ${lines[i].substring(0,130)}`);
}
