"""
QuantAI Backend - FastAPI 主入口
运行方式：uvicorn main:app --reload --host 0.0.0.0 --port 8000
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

from database import engine, Base
import models  # noqa: 确保模型被加载

# 路由
from routers.users import router as auth_router, user_router, admin_router
from routers.market import router as market_router
from routers.positions import router as positions_router
from routers.strategies import router as strategies_router
from routers.broker import router as broker_router
from routers.orders import router as orders_router
from routers.ai_trading import router as ai_router
from routers.trading_executor import router as trading_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时自动创建数据库表
    Base.metadata.create_all(bind=engine)
    print("✅ QuantAI 数据库初始化完成")
    yield
    print("👋 QuantAI 服务已停止")


app = FastAPI(
    title="QuantAI API",
    description="QuantAI 量化交易 SaaS 后端服务",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS（允许前端跨域）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境替换为具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(admin_router)
app.include_router(market_router)
app.include_router(positions_router)
app.include_router(strategies_router)
app.include_router(broker_router)
app.include_router(orders_router)
app.include_router(ai_router)
app.include_router(trading_router)


@app.get("/")
def root():
    return {"service": "QuantAI API", "version": "1.0.0", "status": "running"}


@app.get("/health")
def health():
    return {"status": "ok"}


# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"success": False, "message": f"服务器内部错误: {str(exc)}"}
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
