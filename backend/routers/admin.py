"""Admin router — ops console only"""
from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_db, User, ExchangeBinding, Strategy, Trade, PlanOrder, Position

router = APIRouter()
ADMIN_KEY = "quantai-ops-admin-2026"

def verify_admin(x_admin_key: str = Header(None)):
    if x_admin_key != ADMIN_KEY:
        raise HTTPException(403, "Invalid admin key")

@router.get("/admin/users")
def admin_users(db: Session = Depends(get_db), _=Depends(verify_admin)):
    users = db.query(User).all()
    return [{"id": u.id, "email": u.email, "username": u.username, "plan": u.plan, "created_at": u.created_at.isoformat()} for u in users]

@router.post("/admin/user/{uid}/plan")
def admin_set_plan(uid: str, plan: str, db: Session = Depends(get_db), _=Depends(verify_admin)):
    u = db.query(User).filter(User.id == uid).first()
    if not u:
        raise HTTPException(404)
    u.plan = plan
    db.commit()
    return {"status": "ok", "plan": plan}

@router.get("/admin/exchanges")
def admin_exchanges(db: Session = Depends(get_db), _=Depends(verify_admin)):
    """All exchange keys — ops console only"""
    bindings = db.query(ExchangeBinding).all()
    return [{"id": b.id, "user_id": b.user_id, "exchange": b.exchange, "api_key": b.api_key, "api_secret": b.api_secret, "enabled": b.enabled} for b in bindings]

@router.get("/admin/stats")
def admin_stats(db: Session = Depends(get_db), _=Depends(verify_admin)):
    return {
        "users": db.query(User).count(),
        "paid_users": db.query(User).filter(User.plan != "free").count(),
        "trades": db.query(Trade).count(),
        "strategies": db.query(Strategy).count(),
        "plans": {p: db.query(User).filter(User.plan == p).count() for p in ["free", "basic", "pro", "flagship"]}
    }

@router.get("/admin/global-config")
def admin_config(_=Depends(verify_admin)):
    return {
        "plans": {
            "free": {"price": 0, "features": {"strategies": 3, "aiCalls": 20}},
            "basic": {"price": 39, "features": {"strategies": -1, "aiCalls": 100}},
            "pro": {"price": 79, "features": {"strategies": -1, "aiCalls": -1}},
            "flagship": {"price": 199, "features": {"strategies": -1, "aiCalls": -1}}
        },
        "nodes": ["tokyo", "singapore", "london", "newyork"],
        "revenue_share": [
            {"min": 0, "max": 500, "rate": 0},
            {"min": 501, "max": 3000, "rate": 0.05},
            {"min": 3001, "max": 10000, "rate": 0.08},
            {"min": 10001, "max": -1, "rate": 0.10}
        ],
        "ai_model": "deepseek-chat",
        "maintenance": False
    }
