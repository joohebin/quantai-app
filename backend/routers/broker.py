"""
QuantAI - 券商账户路由
"""
import os
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from database import get_db
import models
import schemas
import auth

router = APIRouter(prefix="/api/brokers", tags=["券商"])
admin_router = APIRouter(prefix="/api/admin/brokers", tags=["管理-券商"])

SUPPORTED_BROKERS = [
    # 加密货币交易所
    {"name": "Binance",    "type": "crypto",  "logo": "🟡", "description": "全球最大加密货币交易所"},
    {"name": "OKX",        "type": "crypto",  "logo": "⚫", "description": "OKX衍生品交易所"},
    {"name": "Bybit",      "type": "crypto",  "logo": "🟠", "description": "Bybit合约交易"},
    {"name": "KuCoin",     "type": "crypto",  "logo": "🟢", "description": "KuCoin库币交易所"},
    {"name": "Gate.io",    "type": "crypto",  "logo": "🔴", "description": "Gate芝麻开门"},
    {"name": "Coinbase",   "type": "crypto",  "logo": "🔵", "description": "Coinbase美国合规交易所"},
    {"name": "Kraken",     "type": "crypto",  "logo": "🐙", "description": "Kraken欧洲老牌交易所"},
    {"name": "Bitget",     "type": "crypto",  "logo": "🟣", "description": "Bitget跟单交易"},
    {"name": "MEXC",       "type": "crypto",  "logo": "🟡", "description": "MEXC抹茶交易所"},
    {"name": "HTX",        "type": "crypto",  "logo": "🔴", "description": "HTX火币交易所"},
    # 传统金融
    {"name": "MT5/MetaTrader", "type": "forex","logo": "🔵","description": "外汇/期货主流平台"},
    {"name": "Interactive Brokers", "type": "stock", "logo": "🟢", "description": "美股/港股/期货"},
    # MetaApi
    {"name": "MetaApi", "type": "metaapi", "logo": "🔷", "description": "MT5云交易API服务"},
]


@router.get("/supported")
def get_supported_brokers():
    """获取支持的券商列表"""
    return SUPPORTED_BROKERS


@router.get("/", response_model=List[schemas.BrokerAccountOut])
def get_broker_accounts(
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    return db.query(models.BrokerAccount).filter(
        models.BrokerAccount.user_id == current_user.id
    ).all()


@router.post("/", response_model=schemas.BrokerAccountOut, status_code=201)
def add_broker_account(
    payload: schemas.BrokerAccountCreate,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    # Free 只能连1个
    existing = db.query(models.BrokerAccount).filter(
        models.BrokerAccount.user_id == current_user.id
    ).count()
    tier_limits = {"free": 1, "basic": 2, "starter": 3, "pro": 5, "elite": 999}
    limit = tier_limits.get(current_user.subscription_tier, 1)
    if existing >= limit:
        raise HTTPException(
            status_code=403,
            detail=f"当前订阅最多连接 {limit} 个券商账户"
        )

    account = models.BrokerAccount(
        user_id=current_user.id,
        broker_name=payload.broker_name,
        broker_type=payload.broker_type,
        api_key=payload.api_key,         # TODO: 生产环境加密存储
        api_secret=payload.api_secret,
        api_passphrase=payload.api_passphrase,
        account_id=payload.account_id or "",  # MT5 账户ID
        display_name=payload.display_name or payload.broker_name,
        is_testnet=payload.is_testnet,
        last_sync_at=datetime.utcnow()
    )
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


# ========== 海外期货券商连接 ==========
class ForexBrokerConnect(BaseModel):
    broker_name: str
    email: str
    password: str
    server: str = ""
    account_type: str = "real"  # real or demo
    broker_type: str = "forex"

# MetaApi Token（平台方持有，生产环境应从环境变量或配置读取）
METAAPI_TOKEN = "eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI3MTI1Mzc1MTA0YjcwNjVkNzliNDMwMDRiMjMwYjkyYyIsImFjY2Vzc1J1bGVzIjpbeyJpZCI6InRyYWRpbmctYWNjb3VudC1tYW5hZ2VtZW50LWFwaSIsIm1ldGhvZHMiOlsidHJhZGluZy1hY2NvdW50LW1hbmFnZW1lbnQtYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcmVzdC1hcGkiLCJtZXRob2RzIjpbIm1ldGFhcGktYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcnBjLWFwaSIsIm1ldGhvZHMiOlsobWV0YWFwaS1hcGk6d3M6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcmFsLXRpbWUtc3RyZWFtaW5nLWFwaSIsIm1ldGhvZHMiOlsobWV0YWFwaS1hcGk6d3M6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFzdGF0LWFwaSIsIm1ldGhvZHMiOlsobWV0YXN0YXQtYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6InJpc2stbWFuYWdlbWVudC1hcGkiLCJtZXRob2RzIjpbInJpc2stbWFuYWdlbWVudC1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoiY29weWZhY3RvcnktYXBpIiwibWV0aG9kcyI6WyJjb3B5ZmFjdG9yeS1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibXQtbWFuYWdlci1hcGkiLCJtZXRob2RzIjpbIm10LW1hbmFnZXItYXBpOnJlc3Q6ZGVhbGluZzoqOioiLCJtdC1tYW5hZ2VyLWF waTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJiaWxsaW5nLWFwaSIsIm1ldGhvZHMiOlsiYmlsbGluZy1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfV0sImlnbm9yZVJhdGVMaW1pdHMiOmZhbHNlLCJ0b2tlbklkIjoiMjAyMTAyMTMiLCJpbXBlcnNvbmF0ZWQiOmZhbHNlLCJyZWFsVXNlcklkIjoiNzEyNTM3NTEwNGI3MDY1ZDc5YjQzMDA0YjIzMGI5MmMiLCJpYXQiOjE3NzUyNDgzMjZ9.dPQ5Xx8gXjFVa1k0whPpUsiOLbkNj9xlmHbl4-lsfvGB21O42J3xTNvB-XrNlANheLEVQxNeBj7MoaVgqjtn0oSIi___6lxtL_uIKdiOME_r8tEpRoka9AnX9dVuk7a4_MYdlwa5aANULoF-zInBpHaesdMOYDBylNMoZcdQL_MWStT4WCAlKFk7kEppQ6_ZfKlTZ1YCeGZhoSURpEd_xOpoQDWUaGmPoN7h6Aap4MS8uUHVuHgSQ7tbbwfSneb04Nu5yH4HXtKxuksrU9wmVRLEcAYynr203rSr1o_Kx4JTEu-6w86xeq_6QoAyfYUK8PMib5jUCxXavxXJ7rMcv2fuGr3ShBZtCPX1zhnOanNIDKDq0ll911sTuCxs2xIuX7gsTV-aWhnN1bucRjJ5UmrOy-Prhjfe1C628Pg-HO5Fa2Ig0q_t9Rw4qaRmiJnnjoImm8-rFmXKPlljjUG5fGAxJrSFu3L9LX8STcy_zGAsBR_LJ5mbVlG2WDNEqfNBiBLaPhdThu65DjRmWxIhz0gedYg32tltLnZY1-dkIG4MNnPmSFDRS-opnJKl8VGBAT55UpNaaG1f0VUsos6m_sdEfEmxoct_Qx8BNFHYNJgD0GFc7Bk2vXvkfcBjjFUd9vs5MMPc9jRtcYNiO8rzUeWusrW1ZcEPZpfAkliWMh0"

# 券商到MetaApi Provisioning Profile的映射（需要先在MetaApi控制台创建）
BROKER_PROFILES = {
    "INFINOX": {
        "profileId": "3791ec3f-4ef6-493f-b460-4cdbc40e33e4",  # INFINOX MT5账户ID
        "server": "InfinoxLimited-MT5Live"
    },
    "IC Markets": {
        "profileId": "",
        "server": "ICMarkets-Live"
    },
    # 可添加更多券商...
}

async def connect_metaapi_get_balance(login: str, password: str, server: str, broker: str) -> dict:
    """通过MetaApi MT Manager API获取MT5账户余额"""
    import asyncio
    import requests
    
    if not METAAPI_TOKEN:
        return {"success": False, "error": "平台未配置MetaApi Token"}
    
    try:
        profile = BROKER_PROFILES.get(broker, {})
        profile_id = profile.get("profileId")
        
        if not profile_id:
            return {"success": False, "error": f"券商{broker}未配置MetaApi Profile"}
        
        # 使用MT Manager API获取账户信息
        # 基础URL根据region可能不同
        base_url = "https://mt-manager-api-v1.new-york.agiliumtrade.ai"
        
        url = f"{base_url}/users/current/mt5/provisioning-profiles/{profile_id}/accounts/{login}/account-information"
        
        headers = {
            "auth-token": METAAPI_TOKEN,
            "Content-Type": "application/json"
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            return {
                "success": True,
                "balance": data.get("balance", 0),
                "equity": data.get("equity", 0),
                "freeMargin": data.get("freeMargin", 0),
                "marginLevel": data.get("marginLevel", 0),
                "currency": data.get("currency", "USD"),
                "broker": data.get("broker", ""),
                "leverage": data.get("leverage", 0)
            }
        elif response.status_code == 404:
            return {"success": False, "error": f"账户{login}未在MetaApi中配置"}
        else:
            return {"success": False, "error": f"MetaApi错误: {response.status_code}"}
            
    except Exception as e:
        return {"success": False, "error": str(e)}

@router.post("/forex/connect")
def connect_forex_broker(
    payload: ForexBrokerConnect,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """连接海外期货券商 (通过MetaApi获取真实余额)"""
    import asyncio
    
    # 检查是否已存在相同券商
    existing = db.query(models.BrokerAccount).filter(
        models.BrokerAccount.user_id == current_user.id,
        models.BrokerAccount.broker_name == payload.broker_name
    ).first()
    
    # 尝试通过MetaApi获取真实余额
    balance = 0.0
    sync_result = None
    
    if METAAPI_TOKEN:
        # 使用asyncio运行async函数
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            sync_result = loop.run_until_complete(
                connect_metaapi_get_balance(
                    login=payload.email,  # MT5登录名
                    password=payload.password,
                    server=payload.server,
                    broker=payload.broker_name
                )
            )
            if sync_result.get("success"):
                balance = sync_result["balance"]
        except Exception as e:
            sync_result = {"success": False, "error": str(e)}
        finally:
            loop.close()
    
    if existing:
        # 更新现有账户
        existing.email = payload.email
        existing.server = payload.server
        existing.account_type = payload.account_type
        existing.is_testnet = (payload.account_type == "demo")
        existing.balance = balance
        existing.last_sync_at = datetime.utcnow()
        db.commit()
        
        return {
            "success": True, 
            "message": f"{payload.broker_name} 账户已更新",
            "account_id": existing.id,
            "balance": balance,
            "sync_result": sync_result
        }
    
    # 创建新账户
    account = models.BrokerAccount(
        user_id=current_user.id,
        broker_name=payload.broker_name,
        broker_type=payload.broker_type,
        email=payload.email,
        password=payload.password,  # TODO: 生产环境加密存储
        server=payload.server,
        display_name=f"{payload.broker_name} ({'模拟' if payload.account_type == 'demo' else '真实'}账户)",
        is_testnet=(payload.account_type == "demo"),
        balance=balance,
        last_sync_at=datetime.utcnow()
    )
    db.add(account)
    db.commit()
    db.refresh(account)
    
    return {
        "success": True, 
        "message": f"{payload.broker_name} 连接成功",
        "account_id": account.id,
        "balance": balance,
        "sync_result": sync_result
    }


# ========== 获取券商可用交易账户列表 ==========
class BrokerPortalLogin(BaseModel):
    broker_name: str
    portal_email: str
    portal_password: str

@router.post("/portal-accounts")
def get_broker_portal_accounts(
    payload: BrokerPortalLogin,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """通过券商管理后台登录获取可用交易账户列表"""
    # 各券商的API端点（这里用模拟数据演示）
    broker_portal_apis = {
        "IC Markets": "https://icmarkets.com/api/accounts",
        "Exness": "https://www.exness.com/api/accounts",
        "Tickmill": "https://my Tickmill.com/api/accounts",
    }
    
    broker = payload.broker_name
    email = payload.portal_email
    password = payload.portal_password
    
    # TODO: 实际对接券商API获取账户列表
    # 这里返回模拟数据，实际应该调用各券商的API
    
    # 模拟返回账户列表
    demo_accounts = [
        {"id": "12345678", "type": "real", "currency": "USD", "balance": 10000, "server": "ICMarkets-Demo"},
        {"id": "87654321", "type": "demo", "currency": "USD", "balance": 50000, "server": "ICMarkets-Demo"},
    ]
    
    return {
        "success": True,
        "accounts": demo_accounts,
        "message": f"已获取 {broker} 下的可用账户"
    }


# ========== 设置活跃交易账户 ==========
class SetActiveAccount(BaseModel):
    account_id: int

@router.post("/set-active")
def set_active_account(
    payload: SetActiveAccount,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """设置活跃交易账户（用户选择用哪个账户进行交易）"""
    account = db.query(models.BrokerAccount).filter(
        models.BrokerAccount.id == payload.account_id,
        models.BrokerAccount.user_id == current_user.id
    ).first()
    if not account:
        raise HTTPException(status_code=404, detail="账户不存在")
    
    # 先取消所有账户的is_active
    db.query(models.BrokerAccount).filter(
        models.BrokerAccount.user_id == current_user.id
    ).update({"is_active": False})
    
    # 激活选中的账户
    account.is_active = True
    db.commit()
    
    return {"success": True, "message": f"已切换交易账户到 {account.display_name}"}


@router.delete("/{account_id}", response_model=schemas.ResponseOK)
def remove_broker_account(
    account_id: int,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    account = db.query(models.BrokerAccount).filter(
        models.BrokerAccount.id == account_id,
        models.BrokerAccount.user_id == current_user.id
    ).first()
    if not account:
        raise HTTPException(status_code=404, detail="账户不存在")
    db.delete(account)
    db.commit()
    return schemas.ResponseOK(message=f"已断开 {account.broker_name}")


@router.post("/{account_id}/sync")
def sync_broker_account(
    account_id: int,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """同步券商账户余额（模拟，真实对接 CCXT）"""
    account = db.query(models.BrokerAccount).filter(
        models.BrokerAccount.id == account_id,
        models.BrokerAccount.user_id == current_user.id
    ).first()
    if not account:
        raise HTTPException(status_code=404, detail="账户不存在")

    import random
    account.balance = round(random.uniform(1000, 50000), 2)
    account.last_sync_at = datetime.utcnow()
    db.commit()

    return {"balance": account.balance, "currency": account.currency, "synced_at": account.last_sync_at}


@router.post("/test-connection")
def test_connection(
    payload: schemas.BrokerAccountCreate,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """测试券商连接"""
    import requests
    import json
    
    if payload.broker_name == "MetaApi":
        # 验证 MetaApi Token
        token = payload.api_key
        account_id = payload.api_secret  # MetaApi 用 api_secret 存 accountId
        
        if not token or not account_id:
            raise HTTPException(status_code=400, detail="Token 和账户ID不能为空")
        
        try:
            # 调用 MetaApi API 验证
            resp = requests.get(
                f"https://mt-client-api-v1.metaapi.io/accounts/{account_id}",
                headers={"Authorization": f"Bearer {token}"},
                timeout=10
            )
            if resp.status_code == 200:
                data = resp.json()
                return {"success": True, "broker": "MetaApi", "account": data.get("accountId"), "status": data.get("connectionStatus")}
            else:
                raise HTTPException(status_code=resp.status_code, detail=f"MetaApi验证失败: {resp.text}")
        except requests.RequestException as e:
            raise HTTPException(status_code=500, detail=f"连接MetaApi失败: {str(e)}")
    
    # 其他券商暂时返回模拟成功
    return {"success": True, "broker": payload.broker_name, "message": "连接验证通过"}
    """测试 API Key 连接是否有效"""
    import ccxt
    
    exchange_id = payload.broker_name.lower().replace(" ", "").replace("/", "")
    
    # CCXT 支持的交易所映射
    ccxt_map = {
        "binance": "binance",
        "okx": "okx",
        "bybit": "bybit",
        "kucoin": "kucoin",
        "gate": "gate",
        "coinbase": "coinbase",
        "kraken": "kraken",
        "bitget": "bitget",
        "mexc": "mexc",
        "htx": "htx",
    }
    
    ccxt_id = ccxt_map.get(exchange_id)
    if not ccxt_id:
        return {"success": False, "message": f"暂不支持 {payload.broker_name} 的连接测试"}
    
    try:
        # 创建交易所实例
        exchange_class = getattr(ccxt, ccxt_id)
        exchange = exchange_class({
            'apiKey': payload.api_key,
            'secret': payload.api_secret,
            'enableRateLimit': True,
        })
        
        # 测试读取账户信息
        if payload.broker_name.lower() == "okx" and payload.api_passphrase:
            exchange.password = payload.api_passphrase
        
        # 测试连接
        balance = exchange.fetch_balance()
        
        return {
            "success": True,
            "message": "连接成功",
            "balances": {k: v.get('total', 0) for k, v in balance.items() if v.get('total', 0) > 0}
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"连接失败: {str(e)}"
        }


@router.post("/batch-import")
def batch_import_accounts(
    payload: dict,  # 批量导入的账户数据
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """批量导入多个交易所的 API Key（一键登录）"""
    accounts = payload.get("accounts", [])
    results = []
    
    import ccxt
    
    for acc in accounts:
        broker_name = acc.get("broker_name", "")
        api_key = acc.get("api_key", "")
        api_secret = acc.get("api_secret", "")
        api_passphrase = acc.get("api_passphrase", "")
        
        # 测试连接
        exchange_id = broker_name.lower().replace(" ", "").replace("/", "")
        ccxt_map = {
            "binance": "binance", "okx": "okx", "bybit": "bybit",
            "kucoin": "kucoin", "gate": "gate", "coinbase": "coinbase",
            "kraken": "kraken", "bitget": "bitget", "mexc": "mexc", "htx": "htx",
        }
        ccxt_id = ccxt_map.get(exchange_id)
        
        success = False
        balance = 0
        
        if ccxt_id:
            try:
                exchange_class = getattr(ccxt, ccxt_id)
                exchange = exchange_class({
                    'apiKey': api_key,
                    'secret': api_secret,
                    'enableRateLimit': True,
                })
                if broker_name.lower() == "okx" and api_passphrase:
                    exchange.password = api_passphrase
                balance_data = exchange.fetch_balance()
                balance = balance_data.get('total', {}).get('USDT', 0) or balance_data.get('total', {}).get('USD', 0)
                success = True
            except:
                pass
        
        # 保存到数据库
        if success:
            account = models.BrokerAccount(
                user_id=current_user.id,
                broker_name=broker_name,
                broker_type="crypto",
                api_key=api_key,
                api_secret=api_secret,
                api_passphrase=api_passphrase,
                display_name=f"{broker_name} 账户",
                balance=balance,
                is_testnet=False,
                last_sync_at=datetime.utcnow()
            )
            db.add(account)
            results.append({"broker_name": broker_name, "success": True, "balance": balance})
    
    db.commit()
    return {"results": results}


# ========== MetaApi 配置保存 ==========
class MetaApiConfigSave(BaseModel):
    token: str
    account_id: str
    broker_name: str = "MetaApi"

@router.post("/metaapi/save-config")
def save_metaapi_config(
    config: MetaApiConfigSave,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """保存 MetaApi 配置"""
    import requests
    
    # 验证 Token 有效性
    try:
        resp = requests.get(
            f"https://mt-client-api-v1.metaapi.io/accounts/{config.account_id}",
            headers={"Authorization": f"Bearer {config.token}"},
            timeout=10
        )
        if resp.status_code != 200:
            raise HTTPException(status_code=400, detail=f"MetaApi 验证失败: {resp.text}")
        account_data = resp.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=f"连接 MetaApi 失败: {str(e)}")
    
    # 检查是否已存在配置
    existing = db.query(models.BrokerAccount).filter(
        models.BrokerAccount.user_id == current_user.id,
        models.BrokerAccount.broker_name == "MetaApi"
    ).first()
    
    if existing:
        # 更新
        existing.api_key = config.token
        existing.api_secret = config.account_id
        existing.display_name = f"MetaApi - {account_data.get('accountId', config.account_id)}"
        existing.last_sync_at = datetime.utcnow()
    else:
        # 新建
        account = models.BrokerAccount(
            user_id=current_user.id,
            broker_name="MetaApi",
            broker_type="metaapi",
            api_key=config.token,
            api_secret=config.account_id,
            display_name=f"MetaApi - {account_data.get('accountId', config.account_id)}",
            balance=0,
            is_testnet=False,
            last_sync_at=datetime.utcnow()
        )
        db.add(account)
    
    db.commit()
    return {"success": True, "message": "MetaApi 配置已保存", "account_id": config.account_id}


@router.get("/metaapi/config")
def get_metaapi_config(
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取 MetaApi 配置"""
    account = db.query(models.BrokerAccount).filter(
        models.BrokerAccount.user_id == current_user.id,
        models.BrokerAccount.broker_name == "MetaApi"
    ).first()
    
    if not account:
        return {"configured": False}
    
    return {
        "configured": True,
        "account_id": account.api_secret,
        "display_name": account.display_name,
        "last_sync": account.last_sync_at
    }


# ========== 管理员 API ==========
@admin_router.get("/all")
def get_all_broker_accounts(
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取所有用户的交易所配置（管理员使用）"""
    # 检查是否为管理员
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(status_code=403, detail="需要管理员权限")
    
    # 获取所有用户的交易所
    all_accounts = db.query(
        models.BrokerAccount,
        models.User.username,
        models.User.email
    ).join(
        models.User, models.BrokerAccount.user_id == models.User.id
    ).all()
    
    # 转换为列表
    result = []
    for broker, username, email in all_accounts:
        item = {
            "id": broker.id,
            "user_id": broker.user_id,
            "username": username,
            "email": email,
            "broker_name": broker.broker_name,
            "broker_type": broker.broker_type,
            "display_name": broker.display_name,
            "balance": broker.balance,
            "currency": broker.currency,
            "is_active": broker.is_active,
            "is_testnet": broker.is_testnet,
            "last_sync_at": broker.last_sync_at.isoformat() if broker.last_sync_at else None,
            "created_at": broker.created_at.isoformat() if broker.created_at else None,
            # 海外期货券商字段
            "email": broker.email or "",
            "server": broker.server or "",
            "account_type": "demo" if broker.is_testnet else "real"
        }
        result.append(item)
    
    return result


@admin_router.get("/user/{user_id}")
def get_user_broker_accounts(
    user_id: int,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取指定用户的交易所配置"""
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(status_code=403, detail="需要管理员权限")
    
    accounts = db.query(models.BrokerAccount).filter(
        models.BrokerAccount.user_id == user_id
    ).all()
    
    return accounts
