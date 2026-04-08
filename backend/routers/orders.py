"""
QuantAI - 下单路由
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models
import schemas
import auth
import random

router = APIRouter(prefix="/api/orders", tags=["下单"])


@router.post("/", response_model=schemas.OrderOut, status_code=201)
def place_order(
    payload: schemas.OrderCreate,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """下单（模拟成交，真实环境对接 CCXT）"""
    # 检查券商账户
    broker = db.query(models.BrokerAccount).filter(
        models.BrokerAccount.id == payload.broker_account_id,
        models.BrokerAccount.user_id == current_user.id
    ).first()
    if not broker:
        raise HTTPException(status_code=404, detail="券商账户不存在")

    # 模拟成交价格
    fill_price = payload.price or round(random.uniform(1000, 90000), 2)
    fill_qty = payload.quantity

    order = models.Order(
        user_id=current_user.id,
        broker_account_id=payload.broker_account_id,
        strategy_id=payload.strategy_id,
        symbol=payload.symbol,
        order_type=payload.order_type,
        side=payload.side,
        quantity=payload.quantity,
        price=payload.price,
        filled_price=fill_price,
        filled_quantity=fill_qty,
        status="filled",
        exchange_order_id=f"QORD{random.randint(100000, 999999)}",
        # 计算交易金额和返点
        trade_amount=fill_price * fill_qty,
        rebate_percent=1.0,  # 默认1%返点
        rebate_amount=round(fill_price * fill_qty * 0.01, 2),
        is_rebated=False
    )
    db.add(order)

    # 创建持仓记录
    margin = fill_price * fill_qty / 10  # 10x默认杠杆
    position = models.Position(
        user_id=current_user.id,
        broker_account_id=payload.broker_account_id,
        symbol=payload.symbol,
        side=payload.side,
        size=fill_qty,
        entry_price=fill_price,
        current_price=fill_price,
        margin=margin,
        leverage=10
    )
    db.add(position)
    db.commit()
    db.refresh(order)
    return order


@router.get("/", response_model=List[schemas.OrderOut])
def get_orders(
    limit: int = 50,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    return db.query(models.Order).filter(
        models.Order.user_id == current_user.id
    ).order_by(models.Order.created_at.desc()).limit(limit).all()
