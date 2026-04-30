"""Bot API router — key management + remote command execution"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
import sys, os, json, uuid, hashlib, hmac, time
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_db, User, Strategy, Trade, Position
from main import get_current_user

router = APIRouter()

# In-memory bot key store (for now; migrate to DB later)
_bot_keys = {}

class CreateBotReq(BaseModel):
    name: str = "My Bot"

class BotExecReq(BaseModel):
    cmd: str
    key: str

@router.post("/bot/create")
def create_bot_key(req: CreateBotReq, user: User = Depends(get_current_user)):
    """User creates a new bot key"""
    key = 'qbot_' + hashlib.sha256(f"{user.id}{time.time()}{uuid.uuid4().hex}".encode()).hexdigest()[:32]
    bot = {
        "key": key,
        "user_id": user.id,
        "name": req.name,
        "created": datetime.utcnow().isoformat(),
        "last_used": None,
        "call_count": 0,
        "enabled": True
    }
    _bot_keys[key] = bot
    return {"status": "ok", "key": key, "name": req.name}

@router.get("/bot/list")
def list_bot_keys(user: User = Depends(get_current_user)):
    """List user's bot keys"""
    keys = [b for b in _bot_keys.values() if b["user_id"] == user.id]
    return [{"key": k["key"][:12] + "...", "name": k["name"], "created": k["created"],
             "last_used": k["last_used"], "call_count": k["call_count"]} for k in keys]

@router.delete("/bot/{bot_key}")
def delete_bot_key(bot_key: str, user: User = Depends(get_current_user)):
    if bot_key in _bot_keys and _bot_keys[bot_key]["user_id"] == user.id:
        del _bot_keys[bot_key]
        return {"status": "ok"}
    raise HTTPException(404, "Bot key not found")

@router.post("/bot/exec")
def bot_execute(req: BotExecReq):
    """Execute command via bot key (no auth — key is the auth)"""
    bot = _bot_keys.get(req.key)
    if not bot or not bot["enabled"]:
        raise HTTPException(401, "Invalid or disabled bot key")
    
    bot["last_used"] = datetime.utcnow().isoformat()
    bot["call_count"] += 1
    
    cmd = req.cmd.strip()
    result = {"original": cmd, "action": None, "message": ""}
    
    # Parse commands
    if "持仓" in cmd:
        result["action"] = "view_positions"
        result["message"] = "持仓信息已发送"
    elif "开启" in cmd and ("自动" in cmd or "AI" in cmd):
        result["action"] = "start_auto"
        result["message"] = "自动交易已开启"
    elif "关闭" in cmd and ("自动" in cmd or "AI" in cmd):
        result["action"] = "stop_auto"
        result["message"] = "自动交易已关闭"
    elif "策略" in cmd and "查看" in cmd:
        result["action"] = "view_strategies"
        result["message"] = "策略列表已发送"
    elif "策略" in cmd and "创建" in cmd:
        result["action"] = "create_strategy"
        result["message"] = "策略创建请求已接收"
    elif "买入" in cmd or "卖" in cmd or "开多" in cmd or "开空" in cmd or "平仓" in cmd:
        result["action"] = "order"
        result["message"] = "订单已接收: " + cmd
    else:
        result["action"] = "unknown"
        result["message"] = "无法识别指令。试试: 查看持仓, 买入1BTC, 开启自动交易"
    
    return {"status": "ok", "result": result}
