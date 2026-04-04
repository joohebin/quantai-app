"""
QuantAI - 用户路由：注册/登录/账户管理
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
import models
import schemas
import auth

router = APIRouter(prefix="/api/auth", tags=["认证"])
user_router = APIRouter(prefix="/api/user", tags=["用户"])
admin_router = APIRouter(prefix="/api/admin", tags=["管理"])


# ─────────── 注册 ───────────

@router.post("/register", response_model=schemas.TokenOut, status_code=201)
def register(payload: schemas.UserRegister, db: Session = Depends(get_db)):
    print(f"=== REGISTER: {payload.email} ===")
    try:
        # 检查邮箱/用户名是否已存在
        if db.query(models.User).filter(models.User.email == payload.email).first():
            print("Email already exists")
            raise HTTPException(status_code=400, detail="该邮箱已注册")
        if db.query(models.User).filter(models.User.username == payload.username).first():
            print("Username already exists")
            raise HTTPException(status_code=400, detail="用户名已被占用")

        # 创建用户
        user = models.User(
            email=payload.email,
            username=payload.username,
            hashed_password=auth.hash_password(payload.password),
            full_name=payload.full_name or "",
            preferred_language=payload.preferred_language or "zh",
        )
        db.add(user)
        db.flush()
        print(f"User created: {user.id}")

        # 创建默认风控设置
        risk = models.RiskSettings(user_id=user.id)
        db.add(risk)
        db.commit()
        db.refresh(user)
        print(f"Registration successful for {user.email}")

        # 生成 Token
        access_token = auth.create_access_token({"sub": user.id})
        refresh_token = auth.create_refresh_token({"sub": user.id})

        return schemas.TokenOut(
            access_token=access_token,
            refresh_token=refresh_token,
            user=user
        )
    except Exception as e:
        print(f"Registration error: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"注册失败: {str(e)}")


# ─────────── 登录 ───────────

@router.post("/login", response_model=schemas.TokenOut)
def login(payload: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == payload.email).first()
    if not user or not auth.verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="邮箱或密码错误"
        )
    if not user.is_active:
        raise HTTPException(status_code=403, detail="账户已被禁用")

    access_token = auth.create_access_token({"sub": user.id})
    refresh_token = auth.create_refresh_token({"sub": user.id})

    return schemas.TokenOut(
        access_token=access_token,
        refresh_token=refresh_token,
        user=user
    )


# ─────────── 刷新 Token ───────────

@router.post("/refresh", response_model=dict)
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    payload = auth.decode_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="无效的刷新令牌")

    user_id = payload.get("sub")
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="用户不存在")

    new_access_token = auth.create_access_token({"sub": user.id})
    return {"access_token": new_access_token, "token_type": "bearer"}


# ─────────── 当前用户信息 ───────────

@user_router.get("/me", response_model=schemas.UserOut)
def get_me(current_user: models.User = Depends(auth.get_current_active_user)):
    return current_user


@user_router.put("/me", response_model=schemas.UserOut)
def update_me(
    payload: schemas.UserUpdate,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    if payload.full_name is not None:
        current_user.full_name = payload.full_name
    if payload.phone is not None:
        current_user.phone = payload.phone
    if payload.preferred_language is not None:
        current_user.preferred_language = payload.preferred_language
    db.commit()
    db.refresh(current_user)
    return current_user


# ─────────── 风控设置 ───────────

@user_router.get("/risk", response_model=schemas.RiskSettingsOut)
def get_risk_settings(
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    risk = db.query(models.RiskSettings).filter(
        models.RiskSettings.user_id == current_user.id
    ).first()
    if not risk:
        risk = models.RiskSettings(user_id=current_user.id)
        db.add(risk)
        db.commit()
        db.refresh(risk)
    return risk


@user_router.put("/risk", response_model=schemas.RiskSettingsOut)
def update_risk_settings(
    payload: schemas.RiskSettingsUpdate,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    risk = db.query(models.RiskSettings).filter(
        models.RiskSettings.user_id == current_user.id
    ).first()
    if not risk:
        risk = models.RiskSettings(user_id=current_user.id)
        db.add(risk)

    update_data = payload.model_dump(exclude_none=True)
    for k, v in update_data.items():
        setattr(risk, k, v)

    db.commit()
    db.refresh(risk)
    return risk


# ─────────── 子账户管理 ───────────

@admin_router.get("/users", response_model=list)
def list_users(
    skip: int = 0,
    limit: int = 50,
    role: str = None,
    is_active: bool = None,
    db: Session = Depends(get_db)
):
    """获取所有用户列表（管理员）"""
    query = db.query(models.User)
    if role:
        query = query.filter(models.User.role == role)
    if is_active is not None:
        query = query.filter(models.User.is_active == is_active)
    users = query.offset(skip).limit(limit).all()
    return users


@admin_router.get("/users/stats")
def get_user_stats(db: Session = Depends(get_db)):
    """获取用户统计"""
    total = db.query(models.User).count()
    active = db.query(models.User).filter(models.User.is_active == True).count()
    by_role = db.query(
        models.User.role,
        func.count(models.User.id).label("count")
    ).group_by(models.User.role).all()
    
    # 订阅分布
    by_tier = db.query(
        models.User.subscription_tier,
        func.count(models.User.id).label("count")
    ).group_by(models.User.subscription_tier).all()
    
    return {
        "total": total,
        "active": active,
        "inactive": total - active,
        "by_role": {r: c for r, c in by_role},
        "by_tier": {t: c for t, c in by_tier}
    }


@admin_router.post("/subaccount", response_model=schemas.SubAccountOut, status_code=201)
def create_subaccount(
    payload: schemas.SubAccountCreate,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """创建子账户"""
    # 检查权限
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(status_code=403, detail="需要管理员或经理权限")
    
    # 检查子账户数量限制
    current_count = db.query(models.User).filter(
        models.User.parent_id == current_user.id
    ).count()
    
    if current_user.max_subaccounts > 0 and current_count >= current_user.max_subaccounts:
        raise HTTPException(status_code=400, detail=f"已达子账户上限 ({current_user.max_subaccounts})")
    
    # 检查邮箱/用户名是否已存在
    if db.query(models.User).filter(models.User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="该邮箱已注册")
    if db.query(models.User).filter(models.User.username == payload.username).first():
        raise HTTPException(status_code=400, detail="用户名已被占用")
    
    # 创建子账户
    subaccount = models.User(
        email=payload.email,
        username=payload.username,
        hashed_password=auth.hash_password(payload.password),
        full_name=payload.full_name or "",
        role=payload.role,
        max_subaccounts=payload.max_subaccounts,
        parent_id=current_user.id,
        subscription_tier=current_user.subscription_tier,
    )
    db.add(subaccount)
    db.flush()
    
    # 创建默认风控设置
    risk = models.RiskSettings(user_id=subaccount.id)
    db.add(risk)
    db.commit()
    db.refresh(subaccount)
    
    return subaccount


@admin_router.get("/subaccounts", response_model=list)
def list_subaccounts(
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取当前用户的子账户列表"""
    subaccounts = db.query(models.User).filter(
        models.User.parent_id == current_user.id
    ).all()
    return subaccounts


@admin_router.get("/subaccounts/{subaccount_id}", response_model=schemas.SubAccountOut)
def get_subaccount(
    subaccount_id: int,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取子账户详情"""
    subaccount = db.query(models.User).filter(
        models.User.id == subaccount_id,
        models.User.parent_id == current_user.id
    ).first()
    if not subaccount:
        raise HTTPException(status_code=404, detail="子账户不存在")
    return subaccount


@admin_router.put("/subaccounts/{subaccount_id}", response_model=schemas.SubAccountOut)
def update_subaccount(
    subaccount_id: int,
    payload: schemas.UserUpdate,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """更新子账户信息"""
    subaccount = db.query(models.User).filter(
        models.User.id == subaccount_id,
        models.User.parent_id == current_user.id
    ).first()
    if not subaccount:
        raise HTTPException(status_code=404, detail="子账户不存在")
    
    if payload.full_name is not None:
        subaccount.full_name = payload.full_name
    if payload.phone is not None:
        subaccount.phone = payload.phone
    if payload.preferred_language is not None:
        subaccount.preferred_language = payload.preferred_language
    
    db.commit()
    db.refresh(subaccount)
    return subaccount


@admin_router.patch("/subaccounts/{subaccount_id}/status")
def toggle_subaccount_status(
    subaccount_id: int,
    is_active: bool,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """启用/禁用子账户"""
    subaccount = db.query(models.User).filter(
        models.User.id == subaccount_id,
        models.User.parent_id == current_user.id
    ).first()
    if not subaccount:
        raise HTTPException(status_code=404, detail="子账户不存在")
    
    subaccount.is_active = is_active
    db.commit()
    return {"success": True, "is_active": is_active}


@admin_router.delete("/subaccounts/{subaccount_id}")
def delete_subaccount(
    subaccount_id: int,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """删除子账户"""
    subaccount = db.query(models.User).filter(
        models.User.id == subaccount_id,
        models.User.parent_id == current_user.id
    ).first()
    if not subaccount:
        raise HTTPException(status_code=404, detail="子账户不存在")
    
    db.delete(subaccount)
    db.commit()
    return {"success": True, "message": "子账户已删除"}


@admin_router.post("/subaccounts/{subaccount_id}/reset-password")
def reset_subaccount_password(
    subaccount_id: int,
    new_password: str,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """重置子账户密码"""
    if len(new_password) < 6:
        raise HTTPException(status_code=400, detail="密码至少6位")
    
    subaccount = db.query(models.User).filter(
        models.User.id == subaccount_id,
        models.User.parent_id == current_user.id
    ).first()
    if not subaccount:
        raise HTTPException(status_code=404, detail="子账户不存在")
    
    subaccount.hashed_password = auth.hash_password(new_password)
    db.commit()
    return {"success": True, "message": "密码已重置"}
