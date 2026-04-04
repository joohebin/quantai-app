@echo off
chcp 65001 >nul
echo.
echo  ========================================
echo   QuantAI 手机测试服务器
echo  ========================================
echo.
cd /d "%~dp0"
python serve_https.py
pause
