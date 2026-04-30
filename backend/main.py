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
from routers.broker import router as broker_router, admin_router as broker_admin_router
from routers.orders import router as orders_router
from routers.ai_trading import router as ai_router
from routers.trading_executor import router as trading_router
from routers.arbitrage import router as arbitrage_router
from routers.trading_stats import router as trading_stats_router
from routers.ai_signals import router as ai_signals_router
from routers.ai_finetune import router as ai_finetune_router
from routers.meta_positions import router as meta_positions_router
from routers.meta_market import router as meta_market_router
from routers.cs_chat import router as cs_chat_router
from routers.advisor import router as advisor_router
from routers.auto_trade import router as auto_trade_router
from routers.knowledge_base import router as kb_router
from routers.trademux import router as trademux_router
from api2trade import router as api2trade_router


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
app.include_router(broker_admin_router)
app.include_router(orders_router)
app.include_router(ai_router)
app.include_router(trading_router)
app.include_router(arbitrage_router)
app.include_router(trading_stats_router)
app.include_router(ai_signals_router)
app.include_router(ai_finetune_router)
app.include_router(meta_positions_router)
app.include_router(meta_market_router)
app.include_router(cs_chat_router)
app.include_router(advisor_router)      # AI 顾问
app.include_router(auto_trade_router)   # 自动交易
app.include_router(kb_router)          # 知识库
app.include_router(trademux_router)     # TradeMux MT5
app.include_router(api2trade_router)    # API2Trade MT4/MT5 (无EA直连)


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
