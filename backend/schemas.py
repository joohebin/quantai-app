"""
QuantAI - Pydantic Schemas（请求/响应数据验证）
"""
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List
from datetime import datetime


# ─────────────────── 用户 ───────────────────

class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: str
    full_name: Optional[str] = ""
    preferred_language: Optional[str] = "zh"

    @field_validator("username")
    @classmethod
    def username_valid(cls, v):
        if len(v) < 3:
            raise ValueError("用户名至少3个字符")
        if not v.replace("_", "").replace("-", "").isalnum():
            raise ValueError("用户名只能包含字母、数字、下划线、连字符")
        return v

    @field_validator("password")
    @classmethod
    def password_valid(cls, v):
        if len(v) < 6:
            raise ValueError("密码至少6位")
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    preferred_language: Optional[str] = None


class UserOut(BaseModel):
    id: int
    email: str
    username: str
    full_name: str
    subscription_tier: str
    is_active: bool
    is_verified: bool
    preferred_language: str
    total_balance: float
    total_pnl: float
    role: str = "trader"
    max_subaccounts: int = 0
    parent_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class SubAccountCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    full_name: Optional[str] = ""
    role: str = "trader"  # admin/manager/trader/viewer
    max_subaccounts: int = 0


class SubAccountOut(BaseModel):
    id: int
    email: str
    username: str
    full_name: str
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class TokenOut(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserOut


# ─────────────────── 券商账户 ───────────────────

class BrokerAccountCreate(BaseModel):
    broker_name: str
    broker_type: str
    api_key: str
    api_secret: str
    api_passphrase: Optional[str] = ""
    account_id: Optional[str] = ""  # MT5 账户ID
    display_name: Optional[str] = ""
    is_testnet: bool = False


class BrokerAccountOut(BaseModel):
    id: int
    broker_name: str
    broker_type: str
    display_name: str
    balance: float
    currency: str
    is_active: bool
    is_testnet: bool
    # 海外期货券商额外字段
    email: Optional[str] = ""
    server: Optional[str] = ""
    account_type: Optional[str] = "real"
    last_sync_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


# ─────────────────── 持仓 ───────────────────

class PositionOut(BaseModel):
    id: int
    symbol: str
    side: str
    size: float
    entry_price: float
    current_price: float
    unrealized_pnl: float
    realized_pnl: float
    margin: float
    leverage: int
    stop_loss: Optional[float]
    take_profit: Optional[float]
    status: str
    opened_at: datetime

    class Config:
        from_attributes = True


# ─────────────────── 策略 ───────────────────

class StrategyCreate(BaseModel):
    name: str
    description: Optional[str] = ""
    strategy_type: str = "trend"
    symbols: List[str] = []
    timeframe: str = "1h"
    parameters: dict = {}


class StrategyUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    parameters: Optional[dict] = None


class StrategyOut(BaseModel):
    id: int
    name: str
    description: str
    strategy_type: str
    symbols: str
    timeframe: str
    is_active: bool
    is_backtested: bool
    backtest_return: float
    backtest_winrate: float
    live_return: float
    total_trades: int
    win_trades: int
    created_at: datetime

    class Config:
        from_attributes = True


# ─────────────────── 下单 ───────────────────

class OrderCreate(BaseModel):
    broker_account_id: int
    symbol: str
    order_type: str = "market"
    side: str
    quantity: float
    price: Optional[float] = None
    strategy_id: Optional[int] = None


class OrderOut(BaseModel):
    id: int
    symbol: str
    order_type: str
    side: str
    quantity: float
    price: Optional[float]
    filled_price: Optional[float]
    filled_quantity: float
    status: str
    exchange_order_id: str
    # 返点信息
    trade_amount: float = 0.0
    rebate_percent: float = 1.0
    rebate_amount: float = 0.0
    is_rebated: bool = False
    created_at: datetime

    class Config:
        from_attributes = True


# ─────────────────── 风控 ───────────────────

class RiskSettingsUpdate(BaseModel):
    max_daily_loss: Optional[float] = None
    max_position_size: Optional[float] = None
    max_leverage: Optional[int] = None
    stop_loss_enabled: Optional[bool] = None
    auto_close_on_loss: Optional[bool] = None
    emergency_stop: Optional[bool] = None
    notification_email: Optional[bool] = None
    notification_sms: Optional[bool] = None


class RiskSettingsOut(BaseModel):
    max_daily_loss: float
    max_position_size: float
    max_leverage: int
    stop_loss_enabled: bool
    auto_close_on_loss: bool
    emergency_stop: bool
    notification_email: bool
    notification_sms: bool

    class Config:
        from_attributes = True


# ─────────────────── AI 对话 ───────────────────

class AIChatRequest(BaseModel):
    message: str
    context: Optional[str] = ""


class AIChatResponse(BaseModel):
    reply: str
    action: Optional[str] = None      # place_order / analyze / backtest
    action_data: Optional[dict] = None


# ─────────────────── 行情 ───────────────────

class MarketQuote(BaseModel):
    symbol: str
    price: float
    change: float
    change_pct: float
    volume: float
    high_24h: float
    low_24h: float
    updated_at: str


# ─────────────────── 通用响应 ───────────────────

class ResponseOK(BaseModel):
    success: bool = True
    message: str = "OK"
    data: Optional[dict] = None
