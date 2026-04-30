"""Trading + vnpy router"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_db, Trade, Position
from main import get_current_user, User, PLANS, ws_manager

router = APIRouter()

class ExecuteReq(BaseModel):
    exchange: str
    symbol: str
    side: str
    order_type: Optional[str] = "market"
    price: Optional[float] = None
    amount: float
    strategy_id: Optional[str] = None
    source: Optional[str] = "manual"

@router.post("/trade/execute")
def execute_trade(req: ExecuteReq, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if req.source == "auto":
        plan_info = PLANS.get(user.plan, PLANS.get("free"))
        if not plan_info.get("features", {}).get("autoTrade", False):
            raise HTTPException(403, "Auto trading requires Pro+")
    
    trade = Trade(
        user_id=user.id, strategy_id=req.strategy_id,
        exchange=req.exchange, symbol=req.symbol.upper(),
        side=req.side, order_type=req.order_type,
        price=req.price, amount=req.amount,
        status="filled", filled=req.amount, source=req.source
    )
    db.add(trade)
    
    existing = db.query(Position).filter(Position.user_id == user.id, Position.exchange == req.exchange, Position.symbol == req.symbol.upper()).first()
    if existing:
        if req.side in ["buy", "long"]:
            total_val = existing.size * existing.entry_price + req.amount * (req.price or 0)
            existing.size += req.amount
            existing.entry_price = total_val / existing.size if existing.size > 0 else 0
            existing.side = "long"
        else:
            existing.size -= req.amount
            if existing.size <= 0:
                db.delete(existing)
                existing = None
    else:
        db.add(Position(user_id=user.id, exchange=req.exchange, symbol=req.symbol.upper(),
                        side="long" if req.side in ["buy", "long"] else "short",
                        size=req.amount, entry_price=req.price or 0, current_price=req.price or 0))
    db.commit()
    return {"status": "ok", "trade_id": trade.id}

@router.get("/trade/history")
def trade_history(limit: int = 50, offset: int = 0, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    trades = db.query(Trade).filter(Trade.user_id == user.id).order_by(Trade.created_at.desc()).offset(offset).limit(limit).all()
    return [{"id": t.id, "exchange": t.exchange, "symbol": t.symbol, "side": t.side,
             "order_type": t.order_type, "price": t.price, "amount": t.amount,
             "filled": t.filled, "status": t.status, "pnl": t.pnl, "source": t.source,
             "created_at": t.created_at.isoformat()} for t in trades]

@router.get("/position/list")
def position_list(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    positions = db.query(Position).filter(Position.user_id == user.id).all()
    return [{"id": p.id, "symbol": p.symbol, "side": p.side, "size": p.size,
             "entry_price": p.entry_price, "current_price": p.current_price,
             "unrealized_pnl": p.unrealized_pnl} for p in positions]

# vnpy webhook
@router.post("/vnpy/webhook")
def vnpy_webhook(data: dict, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    signals = data.get("signals", [])
    results = []
    for sig in signals:
        t = Trade(
            user_id=user.id, exchange=sig.get("exchange", "vnpy"),
            symbol=sig.get("symbol", ""), side=sig.get("direction", "buy"),
            order_type=sig.get("order_type", "market"),
            price=sig.get("price"), amount=sig.get("volume", 0),
            status="pending", source="vnpy"
        )
        db.add(t)
        db.flush()
        results.append({"signal_id": sig.get("id", ""), "trade_id": t.id})
    db.commit()
    return {"status": "ok", "count": len(signals), "results": results}

@router.get("/vnpy/status")
def vnpy_status(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    positions = db.query(Position).filter(Position.user_id == user.id).all()
    return {
        "connected": True,
        "positions": [{"symbol": p.symbol, "side": p.side, "size": p.size, "pnl": p.unrealized_pnl} for p in positions],
        "total_pnl": sum(p.unrealized_pnl or 0 for p in positions)
    }
