"""
生成 QuantAI PWA 图标 + 自签名 HTTPS 证书 + 启动本地服务器
"""
import os, sys, subprocess, socket, ssl, threading, http.server

BASE = os.path.dirname(os.path.abspath(__file__))

# ── 1. 生成图标 ──────────────────────────────────────────
def make_icons():
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pillow', '-q'])
        from PIL import Image, ImageDraw, ImageFont

    icons_dir = os.path.join(BASE, 'icons')
    os.makedirs(icons_dir, exist_ok=True)

    for size in [192, 512]:
        img = Image.new('RGB', (size, size), '#0A1628')
        draw = ImageDraw.Draw(img)

        # 外圈
        margin = size // 10
        draw.ellipse([margin, margin, size-margin, size-margin],
                     outline='#3B82F6', width=max(3, size//40))

        # 内部圆
        m2 = size // 5
        draw.ellipse([m2, m2, size-m2, size-m2], fill='#1E3A5F')

        # "Q" 文字
        font_size = size // 3
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        text = "Q"
        bbox = draw.textbbox((0,0), text, font=font)
        tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
        draw.text(((size-tw)//2, (size-th)//2 - size//20), text,
                  fill='#60A5FA', font=font)

        # "AI" 小字
        small_size = size // 8
        try:
            small_font = ImageFont.truetype("arial.ttf", small_size)
        except:
            small_font = ImageFont.load_default()
        draw.text((size*0.58, size*0.60), "AI", fill='#00C896', font=small_font)

        out_path = os.path.join(icons_dir, f'icon-{size}.png')
        img.save(out_path)
        print(f'✅ 图标已生成: {out_path}')

# ── 2. 生成自签名证书 ─────────────────────────────────────
def make_cert():
    cert_file = os.path.join(BASE, 'cert.pem')
    key_file  = os.path.join(BASE, 'key.pem')
    if os.path.exists(cert_file) and os.path.exists(key_file):
        print('✅ 证书已存在，跳过生成')
        return cert_file, key_file

    try:
        subprocess.check_call([
            'openssl', 'req', '-x509', '-newkey', 'rsa:2048',
            '-keyout', key_file, '-out', cert_file,
            '-days', '365', '-nodes',
            '-subj', '/CN=localhost'
        ], stderr=subprocess.DEVNULL)
        print(f'✅ 证书生成完成')
    except FileNotFoundError:
        # openssl 不存在，用 Python cryptography 库
        try:
            from cryptography import x509
            from cryptography.x509.oid import NameOID
            from cryptography.hazmat.primitives import hashes, serialization
            from cryptography.hazmat.primitives.asymmetric import rsa
            import datetime, ipaddress

            key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
            subject = issuer = x509.Name([
                x509.NameAttribute(NameOID.COMMON_NAME, u"localhost"),
            ])
            cert = (
                x509.CertificateBuilder()
                .subject_name(subject)
                .issuer_name(issuer)
                .public_key(key.public_key())
                .serial_number(x509.random_serial_number())
                .not_valid_before(datetime.datetime.utcnow())
                .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365))
                .add_extension(x509.SubjectAlternativeName([
                    x509.DNSName(u"localhost"),
                    x509.IPAddress(ipaddress.IPv4Address('127.0.0.1')),
                ]), critical=False)
                .sign(key, hashes.SHA256())
            )
            with open(key_file, "wb") as f:
                f.write(key.private_bytes(
                    serialization.Encoding.PEM,
                    serialization.PrivateFormat.TraditionalOpenSSL,
                    serialization.NoEncryption()
                ))
            with open(cert_file, "wb") as f:
                f.write(cert.public_bytes(serialization.Encoding.PEM))
            print(f'✅ 证书生成完成（cryptography库）')
        except ImportError:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'cryptography', '-q'])
            print('❗ 请重新运行此脚本（cryptography 已安装）')
            sys.exit(1)

    return cert_file, key_file

# ── 3. 获取本机局域网 IP ──────────────────────────────────
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return '127.0.0.1'

# ── 4. 启动 HTTPS 服务器 ──────────────────────────────────
def start_server(cert_file, key_file, port=8443):
    os.chdir(BASE)

    class Handler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, fmt, *args):
            pass  # 静默日志
        def end_headers(self):
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('Access-Control-Allow-Origin', '*')
            super().end_headers()

    httpd = http.server.HTTPServer(('0.0.0.0', port), Handler)
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(cert_file, key_file)
    httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)

    local_ip = get_local_ip()
    url = f'https://{local_ip}:{port}'

    print()
    print('=' * 55)
    print('  🚀 QuantAI 本地 HTTPS 服务器已启动')
    print('=' * 55)
    print(f'  📱 局域网地址（手机扫码）: {url}')
    print(f'  💻 本机地址:               https://localhost:{port}')
    print()
    print('  ⚠️  手机首次访问会提示证书不受信任')
    print('     → 点"高级" → "继续访问" 即可')
    print()
    print('  📲 手机操作步骤：')
    print('     1. 手机与电脑连同一 WiFi')
    print('     2. 扫下方二维码或手动输入地址')
    print('     3. 忽略证书警告，进入页面')
    print('     4. 浏览器菜单 → "添加到主屏幕"')
    print('     5. 从桌面图标打开 = 和 APP 一样！')
    print()
    print('  🛑 按 Ctrl+C 停止服务器')
    print('=' * 55)

    # 生成二维码（文字版）
    try:
        import qrcode
        qr = qrcode.QRCode(border=1)
        qr.add_data(url)
        qr.make(fit=True)
        qr.print_ascii(invert=True)
    except ImportError:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'qrcode', '-q'],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            import qrcode
            qr = qrcode.QRCode(border=1)
            qr.add_data(url)
            qr.make(fit=True)
            qr.print_ascii(invert=True)
        except:
            print(f'  🔗 访问地址: {url}')

    print()
    httpd.serve_forever()

# ── 主流程 ────────────────────────────────────────────────
if __name__ == '__main__':
    print('🔧 正在准备 QuantAI 本地服务...')
    make_icons()
    cert, key = make_cert()
    start_server(cert, key)
