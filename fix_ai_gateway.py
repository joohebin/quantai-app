"""
Fix AI Gateway scope issue:
- sendChat is in script[2], aiGateway is in script[4]
- Browser executes script[2] before script[4], so aiGateway is undefined when sendChat runs
- Solution: Move aiGateway and related functions to script[2]
"""
import re, shutil

SRC = 'quantai-app/index.html'
BAK = SRC + '.bak_clean'

# Step 1: Read current file (bak2 is cleaner)
s = open('quantai-app/index.html.bak2', encoding='utf-8').read()
print(f'Loaded backup: {len(s)} chars')

# Step 2: Find all script block boundaries
script_starts = [(m.start(), m.end()) for m in re.finditer(r'<script[^>]*>', s)]
script_ends   = [m.start() for m in re.finditer(r'</script>', s)]

def get_script_range(idx):
    start = script_starts[idx][1]  # after <script>
    # find matching </script>
    end = next(e for e in script_ends if e > script_starts[idx][0])
    return start, end

# script indices:
# 0: tiny head script
# 1: external cdn
# 2: main app (sendChat here)
# 3: diagnostic
# 4: CS Widget + AI Gateway

s2_content_start, s2_content_end = get_script_range(2)
s4_content_start, s4_content_end = get_script_range(4)
print(f'script[2]: content {s2_content_start}-{s2_content_end}')
print(f'script[4]: content {s4_content_start}-{s4_content_end}')

# Verify
sc_pos = s.find('async function sendChat', s2_content_start, s2_content_end)
ag_pos = s.find('async function aiGateway', s4_content_start, s4_content_end)
print(f'sendChat at {sc_pos} (in script2: {s2_content_start}<={sc_pos}<{s2_content_end})')
print(f'aiGateway at {ag_pos} (in script4: {s4_content_start}<={ag_pos}<{s4_content_end})')

# Step 3: Extract AI Gateway block from script[4]
# Everything from "// ═══ QuantAI AI GATEWAY" to before "/* ── 账户页"
gw_marker  = '// ═══════════════════════════════════════════════════════════════\n// QuantAI AI GATEWAY'
aic_marker = '/* ── 账户页 AI 配置卡片渲染'

gw_start = s.find(gw_marker, s4_content_start, s4_content_end)
aic_pos   = s.find(aic_marker, s4_content_start, s4_content_end)
gw_block  = s[gw_start:aic_pos].rstrip()
print(f'Gateway block: {gw_start}-{aic_pos}, {len(gw_block)} chars')
print('First 80:', gw_block[:80])
print('Last 80:',  gw_block[-80:])

# Step 4: Replace "const X" with "var X" in gateway block to avoid re-declaration errors
# when it exists in both script[2] and script[4]
# Actually better: keep const in script[2] injection, and in script[4] change to var
gw_block_for_s2 = gw_block  # keep as-is for script[2]

# Step 5: Modify script[4]'s gateway section to use window.X pattern (avoid const re-declare)
def constify_for_s4(code):
    # Replace const PLATFORM_GROQ_KEY = ... with window.PLATFORM_GROQ_KEY = ...
    # Replace const QUOTA = { ... with window.QUOTA = window.QUOTA || {
    # Replace const PLATFORM_GROQ_MODEL with window.PLATFORM_GROQ_MODEL = ...
    code = re.sub(r'\bconst (PLATFORM_GROQ_KEY|PLATFORM_GROQ_MODEL|QUOTA)\b', r'window.\1', code)
    # Replace async function X with window.X = async function (to allow overwrite)
    code = re.sub(r'\basync function (aiGateway|_callAI)\b', r'window.\1 = async function', code)
    code = re.sub(r'\bfunction (_quotaKey|getQuotaUsed|incQuotaUsed|checkQuota|_quotaExceededMsg|_upgradeHint|_cleanOldQuota)\b', r'window.\1 = function', code)
    # Fix IIFE: (function _cleanOldQuota(){...})() -- already an IIFE, keep as-is
    return code

gw_block_for_s4 = constify_for_s4(gw_block)

# Step 6: Inject gw_block_for_s2 into end of script[2]
insert_pos = s2_content_end  # just before </script>
inject_code = '\n\n// ===== AI Gateway（前置注入 v2，与sendChat同作用域）=====\n' + gw_block_for_s2 + '\n'

new_s = s[:insert_pos] + inject_code + s[insert_pos:]

# Step 7: In the shifted script[4], replace original gateway block with window.X version
# After injection, positions shift by len(inject_code)
shift = len(inject_code)
new_gw_start = gw_start + shift
new_aic_pos  = aic_pos + shift

original_block = new_s[new_gw_start:new_aic_pos]
new_s = new_s[:new_gw_start] + gw_block_for_s4 + new_s[new_aic_pos:]

print(f'\nFinal file size: {len(new_s)} chars')

# Step 8: Verify no const re-declaration
import collections
const_decls = re.findall(r'const (PLATFORM_GROQ_KEY|PLATFORM_GROQ_MODEL|QUOTA)\b', new_s)
counter = collections.Counter(const_decls)
print('const declarations:', dict(counter))

# Step 9: Write
shutil.copy(SRC, SRC + '.bak_before_fix')
open(SRC, 'w', encoding='utf-8').write(new_s)
print('Done! Written to', SRC)
