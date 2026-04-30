#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取 TradeMux OpenAPI 规范
"""

import requests
import json

BASE_URL = "https://mux.skybluefin.tech"

response = requests.get("{}/openapi.json".format(BASE_URL), timeout=10)

print("Status: {}".format(response.status_code))

if response.status_code == 200:
    data = response.json()

    # 保存完整 JSON
    with open("trademux_openapi.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("API Title: {}".format(data.get("info", {}).get("title", "N/A")))
    print("Version: {}".format(data.get("info", {}).get("version", "N/A")))
    print("")

    # 列出所有端点
    print("=" * 50)
    print("API ENDPOINTS")
    print("=" * 50)

    paths = data.get("paths", {})
    for path, methods in paths.items():
        for method, details in methods.items():
            if method.upper() in ["GET", "POST", "PUT", "DELETE", "PATCH"]:
                summary = details.get("summary", "")
                print("{} {} - {}".format(method.upper(), path, summary))

    print("")
    print("=" * 50)
    print("SECURITY SCHEMES")
    print("=" * 50)
    security = data.get("components", {}).get("securitySchemes", {})
    for name, scheme in security.items():
        print("{}: {}".format(name, scheme.get("type", "N/A")))

    print("")
    print("OpenAPI spec saved to: trademux_openapi.json")
else:
    print("Error: {}".format(response.text))
