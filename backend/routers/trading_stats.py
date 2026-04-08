"""
QuantAI - 交易统计路由
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from database import get_db
import models
import auth

router = APIRouter(prefix="/api/trading-stats", tags=["交易统计"])


@router.get("/summary")
def get_trading_summary(
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取当前用户的交易统计摘要"""
    # 总交易金额
    total_amount = db.query(func.sum(models.Order.trade_amount)).filter(
        models.Order.user_id == current_user.id,
        models.Order.status == "filled"
    ).scalar() or 0
    
    # 待收取手续费
    pending_fee = db.query(func.sum(models.Order.rebate_amount)).filter(
        models.Order.user_id == current_user.id,
        models.Order.status == "filled",
        models.Order.is_rebated == False
    ).scalar() or 0
    
    # 已收取手续费
    collected_fee = db.query(func.sum(models.Order.rebate_amount)).filter(
        models.Order.user_id == current_user.id,
        models.Order.status == "filled",
        models.Order.is_rebated == True
    ).scalar() or 0
    
    # 交易次数
    order_count = db.query(func.count(models.Order.id)).filter(
        models.Order.user_id == current_user.id,
        models.Order.status == "filled"
    ).scalar() or 0
    
    return {
        "total_trade_amount": round(total_amount, 2),
        "pending_fee": round(pending_fee, 2),
        "collected_fee": round(collected_fee, 2),
        "order_count": order_count
    }


@router.get("/user/{user_id}")
def get_user_trading_stats(
    user_id: int,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取指定用户的交易统计（用于中控台）"""
    # 检查权限（管理员或当前用户自己）
    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="无权限查看此用户数据")
    
    # 获取用户信息
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 获取用户的交易所配置
    broker_accounts = db.query(models.BrokerAccount).filter(
        models.BrokerAccount.user_id == user_id
    ).all()
    
    exchanges = []
    for b in broker_accounts:
        exchanges.append({
            "id": b.id,
            "broker_name": b.broker_name,
            "display_name": b.display_name or b.broker_name,
            "is_active": b.is_active,
            "balance": b.balance,
            "last_sync_at": b.last_sync_at.isoformat() if b.last_sync_at else None
        })
    
    # 交易统计
    total_amount = db.query(func.sum(models.Order.trade_amount)).filter(
        models.Order.user_id == user_id,
        models.Order.status == "filled"
    ).scalar() or 0
    
    pending_fee = db.query(func.sum(models.Order.rebate_amount)).filter(
        models.Order.user_id == user_id,
        models.Order.status == "filled",
        models.Order.is_rebated == False
    ).scalar() or 0
    
    collected_fee = db.query(func.sum(models.Order.rebate_amount)).filter(
        models.Order.user_id == user_id,
        models.Order.status == "filled",
        models.Order.is_rebated == True
    ).scalar() or 0
    
    order_count = db.query(func.count(models.Order.id)).filter(
        models.Order.user_id == user_id,
        models.Order.status == "filled"
    ).scalar() or 0
    
    return {
        "user_id": user_id,
        "username": user.username,
        "email": user.email,
        "exchanges": exchanges,
        "stats": {
            "total_trade_amount": round(total_amount, 2),
            "pending_fee": round(pending_fee, 2),
            "collected_fee": round(collected_fee, 2),
            "order_count": order_count
        }
    }


@router.get("/all-users")
def get_all_users_trading_stats(
    limit: int = 50,
    offset: int = 0,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取所有用户的交易统计（用于中控台）"""
    # 检查权限
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="需要管理员权限")
    
    # 查询所有有交易记录的用户
    users = db.query(models.User).join(
        models.Order, models.Order.user_id == models.User.id
    ).group_by(models.User.id).limit(limit).offset(offset).all()
    
    results = []
    for user in users:
        # 交易统计
        total_amount = db.query(func.sum(models.Order.trade_amount)).filter(
            models.Order.user_id == user.id,
            models.Order.status == "filled"
        ).scalar() or 0
        
        pending_fee = db.query(func.sum(models.Order.rebate_amount)).filter(
            models.Order.user_id == user.id,
            models.Order.status == "filled",
            models.Order.is_rebated == False
        ).scalar() or 0
        
        order_count = db.query(func.count(models.Order.id)).filter(
            models.Order.user_id == user.id,
            models.Order.status == "filled"
        ).scalar() or 0
        
        # 交易所配置
        broker_accounts = db.query(models.BrokerAccount).filter(
            models.BrokerAccount.user_id == user.id
        ).all()
        
        exchanges = [b.broker_name for b in broker_accounts]
        
        results.append({
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "exchanges": exchanges,
            "total_trade_amount": round(total_amount, 2),
            "pending_fee": round(pending_fee, 2),
            "order_count": order_count
        })
    
    return results