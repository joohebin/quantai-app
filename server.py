#!/usr/bin/env python3
"""
QuantAI 开发服务器 - 带 no-cache headers，防止浏览器缓存旧版本
"""
import http.server
import socketserver
import os

PORT = 8899
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        # 强制 no-cache，确保每次都加载最新文件
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def log_message(self, format, *args):
        # 只打印 HTML/JS 请求，减少噪音
        if args and ('.html' in str(args[0]) or '.js' in str(args[0])):
            super().log_message(format, *args)

with socketserver.TCPServer(("", PORT), NoCacheHandler) as httpd:
    print(f"[QuantAI Server] Serving at http://localhost:{PORT}")
    print(f"[QuantAI Server] Directory: {DIRECTORY}")
    print(f"[QuantAI Server] Cache-Control: no-cache enabled")
    httpd.serve_forever()
