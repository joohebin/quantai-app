"""
QuantAI - 策略路由
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import json
import random
from database import get_db
import models
import schemas
import auth

router = APIRouter(prefix="/api/strategies", tags=["策略"])


@router.get("/", response_model=List[schemas.StrategyOut])
def get_strategies(
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    return db.query(models.Strategy).filter(
        models.Strategy.user_id == current_user.id
    ).all()


@router.post("/", response_model=schemas.StrategyOut, status_code=201)
def create_strategy(
    payload: schemas.StrategyCreate,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    # 检查订阅权限（Free 最多3个策略）
    existing_count = db.query(models.Strategy).filter(
        models.Strategy.user_id == current_user.id
    ).count()

    tier_limits = {"free": 3, "basic": 5, "starter": 10, "pro": 30, "elite": 999}
    limit = tier_limits.get(current_user.subscription_tier, 3)
    if existing_count >= limit:
        raise HTTPException(
            status_code=403,
            detail=f"当前订阅（{current_user.subscription_tier}）最多支持 {limit} 个策略，请升级"
        )

    strategy = models.Strategy(
        user_id=current_user.id,
        name=payload.name,
        description=payload.description,
        strategy_type=payload.strategy_type,
        symbols=json.dumps(payload.symbols),
        timeframe=payload.timeframe,
        parameters=json.dumps(payload.parameters)
    )
    db.add(strategy)
    db.commit()
    db.refresh(strategy)
    return strategy


@router.put("/{strategy_id}", response_model=schemas.StrategyOut)
def update_strategy(
    strategy_id: int,
    payload: schemas.StrategyUpdate,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    strategy = db.query(models.Strategy).filter(
        models.Strategy.id == strategy_id,
        models.Strategy.user_id == current_user.id
    ).first()
    if not strategy:
        raise HTTPException(status_code=404, detail="策略不存在")

    update_data = payload.model_dump(exclude_none=True)
    if "parameters" in update_data:
        update_data["parameters"] = json.dumps(update_data["parameters"])
    for k, v in update_data.items():
        setattr(strategy, k, v)

    db.commit()
    db.refresh(strategy)
    return strategy


@router.delete("/{strategy_id}", response_model=schemas.ResponseOK)
def delete_strategy(
    strategy_id: int,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    strategy = db.query(models.Strategy).filter(
        models.Strategy.id == strategy_id,
        models.Strategy.user_id == current_user.id
    ).first()
    if not strategy:
        raise HTTPException(status_code=404, detail="策略不存在")
    db.delete(strategy)
    db.commit()
    return schemas.ResponseOK(message="策略已删除")


@router.post("/{strategy_id}/backtest")
def run_backtest(
    strategy_id: int,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """模拟回测（真实环境接 vectorbt/backtrader）"""
    strategy = db.query(models.Strategy).filter(
        models.Strategy.id == strategy_id,
        models.Strategy.user_id == current_user.id
    ).first()
    if not strategy:
        raise HTTPException(status_code=404, detail="策略不存在")

    # 模拟回测结果
    total_return = round(random.uniform(-10, 80), 2)
    win_rate = round(random.uniform(40, 75), 1)
    max_drawdown = round(random.uniform(5, 25), 2)
    sharpe = round(random.uniform(0.5, 3.0), 2)
    total_trades = random.randint(50, 300)
    win_trades = int(total_trades * win_rate / 100)

    # 更新策略统计
    strategy.is_backtested = True
    strategy.backtest_return = total_return
    strategy.backtest_winrate = win_rate
    strategy.total_trades = total_trades
    strategy.win_trades = win_trades
    db.commit()

    return {
        "strategy_id": strategy_id,
        "total_return_pct": total_return,
        "win_rate_pct": win_rate,
        "max_drawdown_pct": max_drawdown,
        "sharpe_ratio": sharpe,
        "total_trades": total_trades,
        "win_trades": win_trades,
        "loss_trades": total_trades - win_trades,
        "avg_win": round(random.uniform(50, 200), 2),
        "avg_loss": round(random.uniform(20, 80), 2),
        "profit_factor": round(random.uniform(1.1, 3.0), 2)
    }
