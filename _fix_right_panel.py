"""Precise right panel replacement"""
import subprocess
filepath = 'index.html'
with open(filepath, 'rb') as f:
    r = f.read()
t = r.decode('utf-8', errors='replace')

# Exact positions
open_pos = 105342  # <div ... right panel opening
close1 = t.find('</div>', 105307)  # 观点广场 title close
close2 = t.find('</div>', close1 + 6)  # sq-posts close
close3 = t.find('</div>', close2 + 6)  # outer div close
print(f'Close positions: {close1}, {close2}, {close3}')
old_block = t[open_pos:close3+6]
print(f'Old block: {len(old_block)} chars')
print(old_block.encode('ascii', errors='replace').decode('ascii'))

new_right = '''<div style="width:280px;min-width:280px;background:var(--card);border:1px solid var(--border);border-radius:12px;display:flex;flex-direction:column;overflow:hidden">
          <div style="display:flex;border-bottom:1px solid var(--border)">
            <div class="fr-tab active" data-tab="rank" onclick="window.switchFRTab('rank')" style="flex:1;padding:10px 0;text-align:center;font-size:12px;font-weight:600;cursor:pointer;border-bottom:2px solid var(--green);color:var(--green)">:trophy: 排行榜</div>
            <div class="fr-tab" data-tab="friends" onclick="window.switchFRTab('friends')" style="flex:1;padding:10px 0;text-align:center;font-size:12px;font-weight:600;cursor:pointer;border-bottom:2px solid transparent;color:var(--muted)">:busts_in_silhouette: 好友</div>
            <div class="fr-tab" data-tab="requests" onclick="window.switchFRTab('requests')" style="flex:1;padding:10px 0;text-align:center;font-size:12px;font-weight:600;cursor:pointer;border-bottom:2px solid transparent;color:var(--muted)">:incoming_envelope: 请求</div>
          </div>
          <div id="fr-rank-panel" style="flex:1;overflow-y:auto;padding:8px;display:block"></div>
          <div id="fr-friends-panel" style="flex:1;overflow-y:auto;padding:8px;display:none"></div>
          <div id="fr-requests-panel" style="flex:1;overflow-y:auto;padding:8px;display:none"></div>
        </div>'''

# Replace emoji shortcodes with actual emoji
new_right = new_right.replace(':trophy:', '\U0001f3c6')
new_right = new_right.replace(':busts_in_silhouette:', '\U0001f465')
new_right = new_right.replace(':incoming_envelope:', '\U0001f4e9')

print(f'New block: {len(new_right)} chars')
t = t[:open_pos] + new_right + t[close3+6:]
print('HTML replaced')

r = t.encode('utf-8', errors='replace')
with open(filepath, 'wb') as f:
    f.write(r)
print(f'Saved: {len(r)} bytes')
