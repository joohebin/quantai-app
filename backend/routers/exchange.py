"""Exchange bindings router"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_db, ExchangeBinding
from main import get_current_user, User

router = APIRouter()

class BindReq(BaseModel):
    exchange: str
    api_key: str
    api_secret: str
    label: Optional[str] = ""

@router.post("/exchange/bind")
def bind_exchange(req: BindReq, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    existing = db.query(ExchangeBinding).filter(
        ExchangeBinding.user_id == user.id,
        ExchangeBinding.exchange == req.exchange
    ).first()
    if existing:
        existing.api_key = req.api_key
        existing.api_secret = req.api_secret
        existing.label = req.label
    else:
        db.add(ExchangeBinding(user_id=user.id, exchange=req.exchange, api_key=req.api_key, api_secret=req.api_secret, label=req.label))
    db.commit()
    return {"status": "ok", "message": f"{req.exchange} bound"}

@router.get("/exchange/list")
def list_exchanges(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    bindings = db.query(ExchangeBinding).filter(ExchangeBinding.user_id == user.id).all()
    return [{
        "id": b.id, "exchange": b.exchange,
        "api_key": b.api_key[:8] + "****" + b.api_key[-4:] if len(b.api_key) > 12 else b.api_key[:4] + "****",
        "label": b.label, "enabled": b.enabled
    } for b in bindings]

@router.delete("/exchange/{exchange_id}")
def remove_exchange(exchange_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    binding = db.query(ExchangeBinding).filter(ExchangeBinding.id == exchange_id, ExchangeBinding.user_id == user.id).first()
    if not binding:
        raise HTTPException(404, "Not found")
    db.delete(binding)
    db.commit()
    return {"status": "ok"}
