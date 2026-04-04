"""
QuantAI - 券商账户路由
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from database import get_db
import models
import schemas
import auth

router = APIRouter(prefix="/api/brokers", tags=["券商"])

SUPPORTED_BROKERS = [
    {"name": "Binance",    "type": "crypto",  "logo": "🟡", "description": "全球最大加密货币交易所"},
    {"name": "OKX",        "type": "crypto",  "logo": "⚫", "description": "OKX衍生品交易所"},
    {"name": "Bybit",      "type": "crypto",  "logo": "🟠", "description": "Bybit合约交易"},
    {"name": "MT5/MetaTrader", "type": "forex","logo": "🔵","description": "外汇/期货主流平台"},
    {"name": "Interactive Brokers", "type": "stock", "logo": "🟢", "description": "美股/港股/期货"},
]


@router.get("/supported")
def get_supported_brokers():
    """获取支持的券商列表"""
    return SUPPORTED_BROKERS


@router.get("/", response_model=List[schemas.BrokerAccountOut])
def get_broker_accounts(
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    return db.query(models.BrokerAccount).filter(
        models.BrokerAccount.user_id == current_user.id
    ).all()


@router.post("/", response_model=schemas.BrokerAccountOut, status_code=201)
def add_broker_account(
    payload: schemas.BrokerAccountCreate,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    # Free 只能连1个
    existing = db.query(models.BrokerAccount).filter(
        models.BrokerAccount.user_id == current_user.id
    ).count()
    tier_limits = {"free": 1, "basic": 2, "starter": 3, "pro": 5, "elite": 999}
    limit = tier_limits.get(current_user.subscription_tier, 1)
    if existing >= limit:
        raise HTTPException(
            status_code=403,
            detail=f"当前订阅最多连接 {limit} 个券商账户"
        )

    account = models.BrokerAccount(
        user_id=current_user.id,
        broker_name=payload.broker_name,
        broker_type=payload.broker_type,
        api_key=payload.api_key,         # TODO: 生产环境加密存储
        api_secret=payload.api_secret,
        api_passphrase=payload.api_passphrase,
        display_name=payload.display_name or payload.broker_name,
        is_testnet=payload.is_testnet,
        last_sync_at=datetime.utcnow()
    )
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


@router.delete("/{account_id}", response_model=schemas.ResponseOK)
def remove_broker_account(
    account_id: int,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    account = db.query(models.BrokerAccount).filter(
        models.BrokerAccount.id == account_id,
        models.BrokerAccount.user_id == current_user.id
    ).first()
    if not account:
        raise HTTPException(status_code=404, detail="账户不存在")
    db.delete(account)
    db.commit()
    return schemas.ResponseOK(message=f"已断开 {account.broker_name}")


@router.post("/{account_id}/sync")
def sync_broker_account(
    account_id: int,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """同步券商账户余额（模拟，真实对接 CCXT）"""
    account = db.query(models.BrokerAccount).filter(
        models.BrokerAccount.id == account_id,
        models.BrokerAccount.user_id == current_user.id
    ).first()
    if not account:
        raise HTTPException(status_code=404, detail="账户不存在")

    import random
    account.balance = round(random.uniform(1000, 50000), 2)
    account.last_sync_at = datetime.utcnow()
    db.commit()

    return {"balance": account.balance, "currency": account.currency, "synced_at": account.last_sync_at}
