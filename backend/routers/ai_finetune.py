"""
QuantAI - AI信号导出API
用于导出训练数据供模型微调使用
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
import json

from database import get_db
from models import AISignal, User
from auth import get_current_active_user

router = APIRouter(prefix="/api/admin/ai-finetune", tags=["AI Finetune"])


# ============ Schema ============
class ExportParams(BaseModel):
    """导出参数"""
    min_signals: int = 100          # 最少信号数
    source: Optional[str] = None     # 来源筛选
    label: Optional[str] = None       # 标注类型


# ============ 数据清洗函数 ============
def auto_label(signal: AISignal) -> str:
    """自动标注信号质量"""
    if signal.pnl_result > 0:
        return "positive"
    if signal.pnl_result < -5:  # 亏损超过5%为负面
        return "negative"
    return "neutral"


def clean_signals(signals: list) -> list:
    """清洗数据"""
    cleaned = []
    for s in signals:
        # 必须有市场快照
        if not s.market_snapshot:
            continue
        # 必须已执行
        if not s.executed:
            continue
        # 必须有结果
        if not s.result_updated_at:
            continue
        # 排除异常数据
        if s.pnl_result < -1000 or s.pnl_result > 1000:
            continue
        cleaned.append(s)
    return cleaned


def format_training_data(signal: AISignal, label: str) -> dict:
    """格式化为训练数据"""
    market_str = json.loads(signal.market_snapshot) if signal.market_snapshot else {}
    market_text = ", ".join([f"{k}: ${v}" for k, v in market_str.items()])
    
    content = f"""你是QuantAI量化交易助手。当前市场价格：{market_text}

请分析市场并给出交易建议。输出JSON格式：{{"action": "buy|sell|hold", "symbol": "标的", "amount": 数量, "reason": "原因"}}"""

    response = json.dumps({
        "action": signal.signal_type,
        "symbol": signal.symbol,
        "amount": signal.amount,
        "reason": signal.reason
    }, ensure_ascii=False)

    return {
        "messages": [
            {"role": "system", "content": "你是QuantAI量化交易专家，擅长分析市场趋势和寻找交易机会。"},
            {"role": "user", "content": content},
            {"role": "assistant", "content": response}
        ]
    }


# ============ API ============
@router.post("/export")
async def export_training_data(
    params: ExportParams,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """导出训练数据"""
    # 权限检查
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(status_code=403, detail="无权限")
    
    # 查询信号
    query = db.query(AISignal)
    if params.source:
        query = query.filter(AISignal.source == params.source)
    
    signals = query.all()
    
    # 清洗数据
    signals = clean_signals(signals)
    
    if len(signals) < params.min_signals:
        return {
            "success": False,
            "message": f"数据不足：{len(signals)}/{params.min_signals}",
            "count": len(signals)
        }
    
    # 格式化
    training_data = []
    for s in signals:
        label = auto_label(s)
        if params.label and label != params.label:
            continue
        training_data.append(format_training_data(s, label))
    
    return {
        "success": True,
        "count": len(training_data),
        "data": training_data[:params.min_signals]  # 限制数量
    }


@router.get("/stats")
async def get_finetune_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取微调统计数据"""
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(status_code=403, detail="无权限")
    
    total = db.query(AISignal).count()
    executed = db.query(AISignal).filter(AISignal.executed == True).count()
    has_result = db.query(AISignal).filter(AISignal.result_updated_at != None).count()
    
    # 标注分布
    positive = db.query(AISignal).filter(AISignal.pnl_result > 0).count()
    negative = db.query(AISignal).filter(AISignal.pnl_result < -5).count()
    neutral = total - positive - negative
    
    return {
        "success": True,
        "stats": {
            "total_signals": total,
            "executed": executed,
            "has_result": has_result,
            "positive": positive,
            "negative": negative,
            "neutral": neutral,
            "ready_for_training": has_result - negative  # 可用于训练的数量
        }
    }


@router.post("/start")
async def start_finetune(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """发起微调任务（待实现）"""
    if current_user.role not in ["admin"]:
        raise HTTPException(status_code=403, detail="仅管理员可操作")
    
    # 检查数据量
    has_result = db.query(AISignal).filter(
        AISignal.result_updated_at != None,
        AISignal.pnl_result > -1000
    ).count()
    
    if has_result < 100:
        return {
            "success": False,
            "message": f"数据不足：{has_result}条，需要100+条"
        }
    
    # TODO: 调用OpenRouter微调API
    return {
        "success": True,
        "message": f"已准备{has_result}条训练数据，请配置OpenRouter API Key后发起微调"
    }