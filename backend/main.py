"""QuantAI Backend API — FastAPI + SQLite + WebSocket"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from database import engine, Base, get_db, User, create_token
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from fastapi import HTTPException, status
from datetime import datetime

SECRET_KEY = "quantai-prod-secret-change-me"  # TODO: env var
ALGORITHM = "HS256"

app = FastAPI(title="QuantAI Backend API", version="1.0.0")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

# === Auth Deps ===
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(401, "Invalid token")
    except JWTError:
        raise HTTPException(401, "Invalid token")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    return user

# === WebSocket Manager ===
class ConnectionManager:
    def __init__(self):
        self.active: dict[str, list[WebSocket]] = {}
    
    async def connect(self, user_id: str, ws: WebSocket):
        await ws.accept()
        if user_id not in self.active:
            self.active[user_id] = []
        self.active[user_id].append(ws)
    
    def disconnect(self, user_id: str, ws: WebSocket):
        if user_id in self.active:
            self.active[user_id] = [w for w in self.active[user_id] if w != ws]
            if not self.active[user_id]:
                del self.active[user_id]
    
    async def send_to_user(self, user_id: str, data: dict):
        if user_id in self.active:
            for ws in self.active[user_id]:
                try:
                    await ws.send_json(data)
                except:
                    pass

ws_manager = ConnectionManager()

# === Plans Config ===
PLANS = {
    "free": {"id": "free", "name": "\u514d\u8d39\u8bd5\u7528", "price": 0, "features": {"strategies": 3, "aiCalls": 20, "metaApiCalls": 100, "autoTrade": False}},
    "basic": {"id": "basic", "name": "\u57fa\u7840\u5957\u9910", "price": 39, "features": {"strategies": -1, "aiCalls": 100, "metaApiCalls": 500, "autoTrade": False}},
    "pro": {"id": "pro", "name": "\u4e13\u4e1a\u5957\u9910", "price": 79, "features": {"strategies": -1, "aiCalls": -1, "metaApiCalls": 5000, "autoTrade": True}},
    "flagship": {"id": "flagship", "name": "\u65d7\u8230\u5957\u9910", "price": 199, "features": {"strategies": -1, "aiCalls": -1, "metaApiCalls": -1, "autoTrade": True}}
}

REVENUE_SHARE = [
    {"min": 0, "max": 500, "rate": 0},
    {"min": 501, "max": 3000, "rate": 0.05},
    {"min": 3001, "max": 10000, "rate": 0.08},
    {"min": 10001, "max": -1, "rate": 0.10}
]

def calc_revenue_share(monthly_pnl):
    if not monthly_pnl or monthly_pnl <= 500:
        return {"total_share": 0, "effective_rate": 0}
    remaining = monthly_pnl - 500
    total = 0
    for tier in REVENUE_SHARE:
        if tier["min"] <= 500:
            continue
        band_max = tier["max"] if tier["max"] > 0 else remaining
        if tier["min"] > 501:
            band = min(remaining, band_max - tier["min"] + 501)
        else:
            band = min(remaining, band_max)
        if band <= 0:
            continue
        total += band * tier["rate"]
        remaining -= band
        if remaining <= 0:
            break
    return {"total_share": round(total, 2), "effective_rate": round(total / monthly_pnl * 100, 2) if monthly_pnl > 0 else 0}

# === WebSocket Endpoint ===
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(ws: WebSocket, user_id: str):
    await ws_manager.connect(user_id, ws)
    try:
        await ws.send_json({"type": "init", "status": "connected"})
        while True:
            data = await ws.receive_text()
            if data == "ping":
                await ws.send_json({"type": "pong"})
    except WebSocketDisconnect:
        ws_manager.disconnect(user_id, ws)

@app.get("/")
def root():
    return {"app": "QuantAI Backend", "version": "1.0.0", "status": "running"}

# === Import Routers ===
from routers.auth import router as auth_router
from routers.exchange import router as exchange_router
from routers.strategy import router as strategy_router
from routers.trading import router as trading_router
from routers.plan import router as plan_router
from routers.admin import router as admin_router
from routers.bot import router as bot_router

app.include_router(auth_router, prefix="/api/v1")
app.include_router(exchange_router, prefix="/api/v1")
app.include_router(strategy_router, prefix="/api/v1")
app.include_router(trading_router, prefix="/api/v1")
app.include_router(plan_router, prefix="/api/v1")
app.include_router(admin_router, prefix="/api/v1")
app.include_router(bot_router, prefix="/api/v1")
