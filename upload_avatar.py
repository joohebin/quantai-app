import urllib.request
import json

token = "8226286731:AAHjjcN3pFgUkMEnIxbHWJ8T2HR7_m6CHZs"
photo_path = r"c:\Users\Administrator\WorkBuddy\Claw\quantai-app\assets\Professional_fintech_app_logo__2026-03-29T18-50-09.png"

with open(photo_path, "rb") as f:
    photo_data = f.read()

boundary = "boundary12345678"
CRLF = b"\r\n"

body = b""
body += b"--" + boundary.encode() + CRLF
body += b'Content-Disposition: form-data; name="photo"; filename="avatar.png"' + CRLF
body += b"Content-Type: image/png" + CRLF + CRLF
body += photo_data
body += CRLF
body += b"--" + boundary.encode() + b"--" + CRLF

# 正确的接口是 setChatPhoto（但对 bot 自身不适用）
# Bot 头像只能通过 BotFather 的 /setuserpic 设置
# 验证一下 Bot 当前信息
url = f"https://api.telegram.org/bot{token}/getMe"
try:
    with urllib.request.urlopen(url, timeout=10) as resp:
        result = json.loads(resp.read())
        print("Bot信息:", json.dumps(result, ensure_ascii=False, indent=2))
except Exception as e:
    print("错误:", e)
