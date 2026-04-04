"""
QuantAI - 持仓路由
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models
import schemas
import auth
import random

router = APIRouter(prefix="/api/positions", tags=["持仓"])


@router.get("/", response_model=List[schemas.PositionOut])
def get_positions(
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取当前用户所有持仓"""
    positions = db.query(models.Position).filter(
        models.Position.user_id == current_user.id,
        models.Position.status == "open"
    ).all()
    # 模拟当前价格更新
    for p in positions:
        drift = random.gauss(0, 0.002)
        p.current_price = round(p.entry_price * (1 + drift), 4)
        p.unrealized_pnl = round((p.current_price - p.entry_price) * p.size * (1 if p.side == "long" else -1), 2)
    return positions


@router.post("/close/{position_id}", response_model=schemas.ResponseOK)
def close_position(
    position_id: int,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """平仓"""
    position = db.query(models.Position).filter(
        models.Position.id == position_id,
        models.Position.user_id == current_user.id
    ).first()
    if not position:
        raise HTTPException(status_code=404, detail="持仓不存在")
    if position.status != "open":
        raise HTTPException(status_code=400, detail="该持仓已关闭")

    position.status = "closed"
    position.realized_pnl = position.unrealized_pnl
    db.commit()

    return schemas.ResponseOK(message=f"已平仓 {position.symbol}，盈亏：{position.realized_pnl:.2f} USDT")


@router.get("/summary")
def get_position_summary(
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """持仓汇总"""
    positions = db.query(models.Position).filter(
        models.Position.user_id == current_user.id,
        models.Position.status == "open"
    ).all()
    total_margin = sum(p.margin for p in positions)
    total_pnl = sum(p.unrealized_pnl for p in positions)
    return {
        "open_positions": len(positions),
        "total_margin": round(total_margin, 2),
        "total_unrealized_pnl": round(total_pnl, 2),
        "pnl_ratio": round(total_pnl / total_margin * 100, 2) if total_margin > 0 else 0
    }
