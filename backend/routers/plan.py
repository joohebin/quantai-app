"""Plan management router"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_db, PlanOrder, PnLRecord
from main import get_current_user, User, PLANS, calc_revenue_share
from datetime import datetime, timedelta

router = APIRouter()

class UpgradeReq(BaseModel):
    plan_id: str
    period_months: Optional[int] = 1

@router.post("/plan/upgrade")
def upgrade_plan(req: UpgradeReq, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if req.plan_id not in PLANS:
        raise HTTPException(400, f"Invalid plan: {req.plan_id}")
    plan_info = PLANS[req.plan_id]
    
    order = PlanOrder(
        user_id=user.id, plan_id=req.plan_id,
        amount=plan_info["price"] * req.period_months,
        period_months=req.period_months, status="paid"
    )
    db.add(order)
    user.plan = req.plan_id
    user.plan_expires = datetime.utcnow() + timedelta(days=30 * req.period_months)
    user.nodes = json.dumps(plan_info.get("nodes", ["default"]))
    db.commit()
    return {"status": "ok", "plan": req.plan_id, "expires": user.plan_expires.isoformat()}

@router.get("/plan/current")
def current_plan(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    plan_info = PLANS.get(user.plan, PLANS["free"])
    return {
        "plan": user.plan,
        "name": plan_info.get("name", ""),
        "price": plan_info.get("price", 0),
        "features": plan_info.get("features", {}),
        "nodes": json.loads(user.nodes or "[]"),
        "addons": json.loads(user.addons or "[]"),
        "expires": user.plan_expires.isoformat() if user.plan_expires else None
    }

@router.post("/plan/addons")
def update_addons(addons: list, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user.addons = json.dumps(addons)
    db.commit()
    return {"status": "ok"}

@router.post("/plan/nodes")
def update_nodes(nodes: list, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if user.plan == "pro" and len(nodes) > 2:
        raise HTTPException(400, "Pro max 2 nodes")
    user.nodes = json.dumps(nodes)
    db.commit()
    return {"status": "ok"}

@router.get("/plan/billing")
def billing_history(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    orders = db.query(PlanOrder).filter(PlanOrder.user_id == user.id).order_by(PlanOrder.created_at.desc()).limit(12).all()
    return [{"id": o.id, "plan_id": o.plan_id, "amount": o.amount, "status": o.status, "created_at": o.created_at.isoformat()} for o in orders]

@router.get("/plan/pnl")
def pnl_summary(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    month = datetime.utcnow().strftime("%Y-%m")
    record = db.query(PnLRecord).filter(PnLRecord.user_id == user.id, PnLRecord.month == month).first()
    if not record:
        record = PnLRecord(user_id=user.id, month=month)
        db.add(record)
        db.commit()
        db.refresh(record)
    share_info = calc_revenue_share(record.total_pnl)
    return {"month": month, "total_pnl": record.total_pnl, "revenue_share": share_info["total_share"], "effective_rate": share_info["effective_rate"]}
