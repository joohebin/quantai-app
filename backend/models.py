"""
QuantAI - 数据模型（SQLAlchemy ORM）
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum


class SubscriptionTier(str, enum.Enum):
    FREE = "free"
    BASIC = "basic"
    STARTER = "starter"
    PRO = "pro"
    ELITE = "elite"


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    TRADER = "trader"
    VIEWER = "viewer"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, default="")
    phone = Column(String, default="")
    avatar_url = Column(String, default="")
    subscription_tier = Column(String, default=SubscriptionTier.FREE)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    preferred_language = Column(String, default="zh")
    total_balance = Column(Float, default=0.0)
    total_pnl = Column(Float, default=0.0)
    # 子账户相关
    parent_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    role = Column(String, default="trader")  # admin/manager/trader/viewer
    max_subaccounts = Column(Integer, default=0)  # 最大子账户数
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关联
    broker_accounts = relationship("BrokerAccount", back_populates="user", cascade="all, delete-orphan")
    positions = relationship("Position", back_populates="user", cascade="all, delete-orphan")
    strategies = relationship("Strategy", back_populates="user", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")
    risk_settings = relationship("RiskSettings", back_populates="user", uselist=False, cascade="all, delete-orphan")
    # 子账户关系 - 自关联
    parent = relationship("User", remote_side=[id], back_populates="subaccounts")
    subaccounts = relationship("User", back_populates="parent", cascade="all, delete-orphan")


class BrokerAccount(Base):
    __tablename__ = "broker_accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    broker_name = Column(String, nullable=False)   # e.g. "Binance", "OKX", "MT5"
    broker_type = Column(String, nullable=False)   # "crypto" | "forex" | "futures"
    api_key = Column(String, default="")           # 加密存储
    api_secret = Column(String, default="")        # 加密存储
    api_passphrase = Column(String, default="")    # OKX专用
    account_id = Column(String, default="")
    # 海外期货券商额外字段
    email = Column(String, default="")             # 登录邮箱
    password = Column(String, default="")         # 登录密码 (生产环境加密)
    server = Column(String, default="")           # 服务器名称
    account_type = Column(String, default="real") # real or demo
    display_name = Column(String, default="")
    balance = Column(Float, default=0.0)
    currency = Column(String, default="USDT")
    is_active = Column(Boolean, default=True)
    is_testnet = Column(Boolean, default=False)
    last_sync_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="broker_accounts")
    positions = relationship("Position", back_populates="broker_account")


class Position(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    broker_account_id = Column(Integer, ForeignKey("broker_accounts.id"))
    symbol = Column(String, nullable=False)        # e.g. "BTC/USDT"
    side = Column(String, nullable=False)          # "long" | "short"
    size = Column(Float, nullable=False)
    entry_price = Column(Float, nullable=False)
    current_price = Column(Float, default=0.0)
    unrealized_pnl = Column(Float, default=0.0)
    realized_pnl = Column(Float, default=0.0)
    margin = Column(Float, default=0.0)
    leverage = Column(Integer, default=1)
    stop_loss = Column(Float)
    take_profit = Column(Float)
    status = Column(String, default="open")        # "open" | "closed" | "liquidated"
    opened_at = Column(DateTime(timezone=True), server_default=func.now())
    closed_at = Column(DateTime(timezone=True))

    user = relationship("User", back_populates="positions")
    broker_account = relationship("BrokerAccount", back_populates="positions")


class Strategy(Base):
    __tablename__ = "strategies"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, default="")
    strategy_type = Column(String, default="trend")  # trend/arbitrage/grid/ai
    symbols = Column(Text, default="[]")             # JSON数组
    timeframe = Column(String, default="1h")
    parameters = Column(Text, default="{}")          # JSON参数
    is_active = Column(Boolean, default=False)
    is_backtested = Column(Boolean, default=False)
    backtest_return = Column(Float, default=0.0)
    backtest_winrate = Column(Float, default=0.0)
    live_return = Column(Float, default=0.0)
    total_trades = Column(Integer, default=0)
    win_trades = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="strategies")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    broker_account_id = Column(Integer, ForeignKey("broker_accounts.id"))
    strategy_id = Column(Integer, ForeignKey("strategies.id"))
    symbol = Column(String, nullable=False)
    order_type = Column(String, nullable=False)    # "market" | "limit" | "stop"
    side = Column(String, nullable=False)          # "buy" | "sell"
    quantity = Column(Float, nullable=False)
    price = Column(Float)
    filled_price = Column(Float)
    filled_quantity = Column(Float, default=0.0)
    status = Column(String, default="pending")     # pending/filled/cancelled/failed
    exchange_order_id = Column(String, default="")
    error_message = Column(Text, default="")
    # 返点相关字段
    trade_amount = Column(Float, default=0.0)     # 交易金额（USDT）
    rebate_percent = Column(Float, default=1.0)   # 返点比例默认1%
    rebate_amount = Column(Float, default=0.0)    # 返点金额
    is_rebated = Column(Boolean, default=False)   # 是否已计算返点
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    filled_at = Column(DateTime(timezone=True))

    user = relationship("User", back_populates="orders")


class RiskSettings(Base):
    __tablename__ = "risk_settings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    max_daily_loss = Column(Float, default=5.0)       # 最大日亏损%
    max_position_size = Column(Float, default=10.0)   # 单仓最大%
    max_leverage = Column(Integer, default=10)
    stop_loss_enabled = Column(Boolean, default=True)
    auto_close_on_loss = Column(Boolean, default=True)
    emergency_stop = Column(Boolean, default=False)
    notification_email = Column(Boolean, default=True)
    notification_sms = Column(Boolean, default=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="risk_settings")


class AIConversation(Base):
    __tablename__ = "ai_conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(String, nullable=False)           # "user" | "assistant"
    content = Column(Text, nullable=False)
    action_taken = Column(String, default="")       # 如"place_order","analyze"等
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AISignal(Base):
    """AI交易信号记录 - 用于模型训练数据收集"""
    __tablename__ = "ai_signals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # 信号内容
    signal_type = Column(String, default="")        # "buy" | "sell" | "hold"
    symbol = Column(String, default="")
    amount = Column(Float, default=0)
    reason = Column(Text, default="")
    # 市场环境快照
    market_snapshot = Column(Text, default="{}")   # JSON: 当时各交易所价格
    # 执行结果（后续更新）
    executed = Column(Boolean, default=False)      # 用户是否执行
    execution_result = Column(String, default="")  # "success" | "cancelled" | "failed"
    pnl_result = Column(Float, default=0.0)           # 实盘盈亏结果
    # 元数据
    source = Column(String, default="ai_advisor")      # "ai_advisor" | "copy_trading" | "arbitrage"
    model_version = Column(String, default="v1")  # 使用的模型版本
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    # 结果更新时刻
    result_updated_at = Column(DateTime(timezone=True))

    user = relationship("User")
