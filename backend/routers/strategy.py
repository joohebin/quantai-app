"""Strategy router"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_db, Strategy
from main import get_current_user, User, PLANS
from datetime import datetime

router = APIRouter()

class StrategyReq(BaseModel):
    name: str
    symbol: Optional[str] = "BTCUSDT"
    strategy_type: Optional[str] = "rsi"
    params: Optional[dict] = {}
    exchange: Optional[str] = "binance"
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    max_position: Optional[float] = 1.0

@router.get("/strategy/list")
def list_strategies(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    strategies = db.query(Strategy).filter(Strategy.user_id == user.id).all()
    return [{
        "id": s.id, "name": s.name, "symbol": s.symbol,
        "strategy_type": s.strategy_type,
        "params": json.loads(s.params) if s.params else {},
        "enabled": s.enabled, "auto_trade": s.auto_trade, "exchange": s.exchange,
        "stop_loss": s.stop_loss, "take_profit": s.take_profit,
        "max_position": s.max_position,
        "created_at": s.created_at.isoformat()
    } for s in strategies]

@router.post("/strategy/create")
def create_strategy(req: StrategyReq, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    plan_info = PLANS.get(user.plan, PLANS.get("free"))
    max_strats = plan_info.get("features", {}).get("strategies", -1)
    count = db.query(Strategy).filter(Strategy.user_id == user.id).count()
    if max_strats >= 0 and count >= max_strats:
        raise HTTPException(403, f"Plan limit: max {max_strats} strategies. Upgrade required.")
    
    strategy = Strategy(
        user_id=user.id, name=req.name,
        symbol=req.symbol.upper(), strategy_type=req.strategy_type,
        params=json.dumps(req.params), exchange=req.exchange,
        stop_loss=req.stop_loss, take_profit=req.take_profit,
        max_position=req.max_position
    )
    db.add(strategy)
    db.commit()
    db.refresh(strategy)
    return {"status": "ok", "id": strategy.id}

@router.put("/strategy/{sid}")
def update_strategy(sid: str, req: StrategyReq, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    s = db.query(Strategy).filter(Strategy.id == sid, Strategy.user_id == user.id).first()
    if not s:
        raise HTTPException(404, "Not found")
    for field in ["name", "exchange", "stop_loss", "take_profit", "max_position"]:
        val = getattr(req, field, None)
        if val is not None:
            setattr(s, field, val)
    s.symbol = req.symbol.upper()
    s.strategy_type = req.strategy_type
    s.params = json.dumps(req.params)
    s.updated_at = datetime.utcnow()
    db.commit()
    return {"status": "ok"}

@router.post("/strategy/{sid}/toggle")
def toggle_strategy(sid: str, field: str = "enabled", user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    s = db.query(Strategy).filter(Strategy.id == sid, Strategy.user_id == user.id).first()
    if not s:
        raise HTTPException(404, "Not found")
    if field in ["enabled", "auto_trade"]:
        setattr(s, field, not getattr(s, field))
    s.updated_at = datetime.utcnow()
    db.commit()
    return {"status": "ok", field: getattr(s, field)}

@router.delete("/strategy/{sid}")
def delete_strategy(sid: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    s = db.query(Strategy).filter(Strategy.id == sid, Strategy.user_id == user.id).first()
    if not s:
        raise HTTPException(404, "Not found")
    db.delete(s)
    db.commit()
    return {"status": "ok"}
