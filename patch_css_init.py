
# -*- coding: utf-8 -*-
# patch showPage copy init + CSS for new modules

with open(r'c:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 改 copy 页面初始化为 initLbPage
old1 = "  if(name==='copy') renderCopyPage();"
new1 = "  if(name==='copy') initLbPage();"
if old1 in content:
    content = content.replace(old1, new1, 1)
    print('Patch 1: copy init -> initLbPage OK')
else:
    print('Patch 1: NOT FOUND, looking for context...')
    idx = content.find("name==='copy'")
    print(repr(content[idx-5:idx+60]))

# 2. 检查是否已有 .lb-rank-row CSS，没有则补充
if '.lb-rank-row' not in content:
    css_addition = r"""
.lb-rank-row{display:flex;align-items:center;gap:12px;padding:12px 14px;background:var(--card2);border-radius:14px;margin-bottom:10px;cursor:pointer;transition:.2s;border:1px solid transparent}
.lb-rank-row:hover{border-color:var(--green);transform:translateX(2px)}
.lb-medal{width:28px;text-align:center;font-size:18px;flex-shrink:0}
.lb-info{flex:1;min-width:0}
.lb-name{font-weight:700;font-size:14px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.lb-stats{display:flex;gap:14px;flex-shrink:0}
.lb-stat-item{display:flex;flex-direction:column;align-items:center;min-width:48px}
.sq-post{background:var(--card2);border-radius:14px;padding:14px;margin-bottom:12px;border:1px solid var(--border)}
.sq-post-header{display:flex;align-items:flex-start;gap:10px;margin-bottom:8px}
.sq-content{font-size:13px;line-height:1.7;margin-bottom:8px}
.sq-tags{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:10px}
.sq-tag{font-size:11px;padding:2px 8px;background:var(--card3,#2a2d3a);border-radius:10px;color:var(--muted)}
.sq-actions{display:flex;gap:10px}
.sq-action{background:none;border:1px solid var(--border);border-radius:20px;padding:5px 14px;font-size:12px;cursor:pointer;color:var(--text2);transition:.2s}
.sq-action:hover,.sq-action.liked{border-color:var(--red,#ef4444);color:var(--red,#ef4444)}
.sq-sent-bull{background:#064e3b;color:#6ee7b7;border-radius:20px;padding:3px 10px;font-size:12px}
.sq-sent-bear{background:#450a0a;color:#fca5a5;border-radius:20px;padding:3px 10px;font-size:12px}
.sq-sent-neutral{background:var(--card3,#2a2d3a);color:var(--muted);border-radius:20px;padding:3px 10px;font-size:12px}
.sm-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px}
.sm-card{background:var(--card2);border-radius:14px;padding:14px;border:1px solid var(--border);cursor:pointer;transition:.2s}
.sm-card:hover{border-color:var(--purple);transform:translateY(-2px)}
.sm-card-head{display:flex;align-items:center;gap:10px;margin-bottom:10px}
.sig-signal-card{background:var(--card2);border-radius:14px;padding:14px;margin-bottom:12px;border:1px solid var(--border)}
.sig-broadcaster-card{background:var(--card2);border-radius:14px;padding:14px;margin-bottom:12px;border:1px solid var(--border)}
.tdp-overlay{position:fixed;inset:0;background:rgba(0,0,0,.6);z-index:900;opacity:0;pointer-events:none;transition:.25s}
.tdp-overlay.active{opacity:1;pointer-events:auto}
.trader-detail-panel{position:fixed;right:0;top:0;height:100%;width:min(380px,96vw);background:var(--card);padding:24px 20px;overflow-y:auto;z-index:901;transform:translateX(100%);transition:.3s cubic-bezier(.4,0,.2,1);box-shadow:-4px 0 24px rgba(0,0,0,.4)}
.trader-detail-panel.active{transform:translateX(0)}
"""
    # 在 </style> 前插入
    if '</style>' in content:
        content = content.replace('</style>', css_addition + '\n</style>', 1)
        print('Patch 2: CSS补充 OK')
    else:
        print('Patch 2: </style> not found')
else:
    print('Patch 2: CSS already present, skip')

# 3. 确保 sm-detail-modal 弹窗存在（检查一下）
if 'sm-detail-modal' in content:
    print('Patch 3: sm-detail-modal exists OK')
else:
    print('Patch 3: sm-detail-modal NOT FOUND - need to add')

with open(r'c:\Users\Administrator\WorkBuddy\Claw\quantai-app\index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('All patches done. File size:', len(content))
