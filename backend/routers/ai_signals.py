"""
QuantAI - AI交易信号收集API
用于记录用户的AI交易信号和执行结果，构建数据飞轮
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import json

from database import get_db
from models import AISignal, User
from auth import get_current_active_user

router = APIRouter(prefix="/api/ai-signals", tags=["AI Signals"])


# ============ Schema ============
class SignalCreate(BaseModel):
    """创建交易信号"""
    signal_type: str = ""           # "buy" | "sell" | "hold"
    symbol: str = ""
    amount: float = 0
    reason: str = ""
    market_snapshot: dict = {}     # 市场快照
    source: str = "ai_advisor"     # 来源


class SignalResultUpdate(BaseModel):
    """更新信号执行结果"""
    executed: bool = False
    execution_result: str = ""    # "success" | "cancelled" | "failed"
    pnl_result: float = 0.0      # 实盘盈亏


# ============ API ============
@router.post("/")
async def create_signal(
    data: SignalCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """记录AI交易信号"""
    signal = AISignal(
        user_id=current_user.id,
        signal_type=data.signal_type,
        symbol=data.symbol,
        amount=data.amount,
        reason=data.reason,
        market_snapshot=json.dumps(data.market_snapshot, ensure_ascii=False),
        source=data.source,
        model_version="v1"
    )
    db.add(signal)
    db.commit()
    db.refresh(signal)
    
    return {"success": True, "signal_id": signal.id}


@router.put("/{signal_id}/result")
async def update_signal_result(
    signal_id: int,
    data: SignalResultUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """更新信号执行结果（用户执行后调用）"""
    signal = db.query(AISignal).filter(
        AISignal.id == signal_id,
        AISignal.user_id == current_user.id
    ).first()
    
    if not signal:
        raise HTTPException(status_code=404, detail="信号不存在")
    
    signal.executed = data.executed
    signal.execution_result = data.execution_result
    signal.pnl_result = data.pnl_result
    signal.result_updated_at = datetime.utcnow()
    
    db.commit()
    
    return {"success": True, "signal_id": signal_id}


@router.get("/")
async def get_signals(
    limit: int = 50,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取当前用户的信号历史"""
    signals = db.query(AISignal).filter(
        AISignal.user_id == current_user.id
    ).order_by(AISignal.created_at.desc()).limit(limit).all()
    
    return {
        "success": True,
        "signals": [{
            "id": s.id,
            "signal_type": s.signal_type,
            "symbol": s.symbol,
            "amount": s.amount,
            "reason": s.reason,
            "executed": s.executed,
            "execution_result": s.execution_result,
            "pnl_result": s.pnl_result,
            "source": s.source,
            "created_at": s.created_at.isoformat() if s.created_at else None,
            "result_updated_at": s.result_updated_at.isoformat() if s.result_updated_at else None
        } for s in signals]
    }


@router.get("/stats")
async def get_signal_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取信号统计数据（用于分析模型效果）"""
    total = db.query(AISignal).filter(AISignal.user_id == current_user.id).count()
    executed = db.query(AISignal).filter(
        AISignal.user_id == current_user.id,
        AISignal.executed == True
    ).count()
    
    # 计算胜率
    wins = db.query(AISignal).filter(
        AISignal.user_id == current_user.id,
        AISignal.executed == True,
        AISignal.execution_result == "success",
        AISignal.pnl_result > 0
    ).count()
    
    win_rate = (wins / executed * 100) if executed > 0 else 0
    
    return {
        "success": True,
        "stats": {
            "total_signals": total,
            "executed": executed,
            "win_count": wins,
            "win_rate": round(win_rate, 2)
        }
    }