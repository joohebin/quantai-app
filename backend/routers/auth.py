"""Auth router"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_db, User, hash_password, verify_password, create_token

router = APIRouter()

class RegisterReq(BaseModel):
    email: str
    password: str
    username: Optional[str] = None

@router.post("/auth/register")
def register(req: RegisterReq, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == req.email).first()
    if existing:
        raise HTTPException(400, "Email already registered")
    user = User(
        email=req.email,
        username=req.username or req.email.split("@")[0],
        password_hash=hash_password(req.password),
        plan="free"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_token(user.id)
    return {
        "access_token": token, "token_type": "bearer",
        "user": {"id": user.id, "email": user.email, "username": user.username, "plan": user.plan}
    }

@router.post("/auth/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(401, "Invalid credentials")
    token = create_token(user.id)
    return {
        "access_token": token, "token_type": "bearer",
        "user": {"id": user.id, "email": user.email, "username": user.username, "plan": user.plan}
    }

@router.get("/auth/me")
def get_me(user: User = Depends(__import__("main", fromlist=["get_current_user"]).get_current_user)):
    import json
    return {
        "id": user.id, "email": user.email, "username": user.username,
        "plan": user.plan,
        "nodes": json.loads(user.nodes or "[]"),
        "addons": json.loads(user.addons or "[]"),
        "avatar": user.avatar,
        "created_at": user.created_at.isoformat()
    }
