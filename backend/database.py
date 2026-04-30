"""Database, auth, and shared utilities"""
from sqlalchemy import create_engine, Column, String, Float, Integer, Boolean, Text, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Optional
import os, uuid

SECRET_KEY = os.environ.get("QUANTAI_SECRET", "quantai-prod-secret-change-me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 7
DATABASE_URL = "sqlite:///./quantai.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# === Models ===
class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: uuid.uuid4().hex)
    email = Column(String, unique=True, index=True)
    username = Column(String)
    password_hash = Column(String)
    plan = Column(String, default="free")
    plan_expires = Column(DateTime, nullable=True)
    nodes = Column(Text, default="[]")
    addons = Column(Text, default="[]")
    avatar = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class ExchangeBinding(Base):
    __tablename__ = "exchange_bindings"
    id = Column(String, primary_key=True, default=lambda: uuid.uuid4().hex)
    user_id = Column(String, index=True)
    exchange = Column(String)
    api_key = Column(String)
    api_secret = Column(String)
    label = Column(String, default="")
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Strategy(Base):
    __tablename__ = "strategies"
    id = Column(String, primary_key=True, default=lambda: uuid.uuid4().hex)
    user_id = Column(String, index=True)
    name = Column(String)
    symbol = Column(String, default="BTCUSDT")
    strategy_type = Column(String, default="rsi")
    params = Column(Text, default="{}")
    enabled = Column(Boolean, default=False)
    auto_trade = Column(Boolean, default=False)
    exchange = Column(String, default="binance")
    stop_loss = Column(Float, nullable=True)
    take_profit = Column(Float, nullable=True)
    max_position = Column(Float, default=1.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

class Trade(Base):
    __tablename__ = "trades"
    id = Column(String, primary_key=True, default=lambda: uuid.uuid4().hex)
    user_id = Column(String, index=True)
    strategy_id = Column(String, nullable=True)
    exchange = Column(String)
    symbol = Column(String)
    side = Column(String)
    order_type = Column(String, default="market")
    price = Column(Float, nullable=True)
    amount = Column(Float)
    filled = Column(Float, default=0)
    status = Column(String, default="pending")
    pnl = Column(Float, nullable=True)
    source = Column(String, default="manual")
    created_at = Column(DateTime, default=datetime.utcnow)

class Position(Base):
    __tablename__ = "positions"
    id = Column(String, primary_key=True, default=lambda: uuid.uuid4().hex)
    user_id = Column(String, index=True)
    exchange = Column(String)
    symbol = Column(String)
    side = Column(String)
    size = Column(Float, default=0)
    entry_price = Column(Float, default=0)
    current_price = Column(Float, default=0)
    unrealized_pnl = Column(Float, default=0)
    margin = Column(Float, default=0)
    updated_at = Column(DateTime, default=datetime.utcnow)

class PlanOrder(Base):
    __tablename__ = "plan_orders"
    id = Column(String, primary_key=True, default=lambda: uuid.uuid4().hex)
    user_id = Column(String, index=True)
    plan_id = Column(String)
    amount = Column(Float)
    currency = Column(String, default="usd")
    status = Column(String, default="pending")
    period_months = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)

class PnLRecord(Base):
    __tablename__ = "pnl_records"
    id = Column(String, primary_key=True, default=lambda: uuid.uuid4().hex)
    user_id = Column(String, index=True)
    month = Column(String)
    total_pnl = Column(Float, default=0)
    revenue_share = Column(Float, default=0)
    settled = Column(Boolean, default=False)
    settled_at = Column(DateTime, nullable=True)

# === Auth Functions ===
def create_token(user_id: str):
    expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    payload = {"sub": user_id, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# === DB Session ===
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
