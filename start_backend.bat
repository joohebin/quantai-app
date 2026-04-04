@echo off
echo QuantAI Backend 启动中...
cd /d "%~dp0backend"

REM 检查虚拟环境
if not exist "venv" (
    echo 创建虚拟环境...
    python -m venv venv
)

call venv\Scripts\activate.bat

REM 安装依赖
echo 安装依赖...
pip install -r requirements.txt -q

REM 启动服务
echo.
echo =========================================
echo  QuantAI API 已启动
echo  地址：http://localhost:8000
echo  文档：http://localhost:8000/docs
echo =========================================
echo.
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
