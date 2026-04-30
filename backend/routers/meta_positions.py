"""
QuantAI - MetaApi 实时数据路由
通过 MetaApi SDK RPC API 获取 MT5 真实账户数据
带重试、缓存和优雅降级机制
"""
import asyncio
import time
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/api/meta", tags=["MetaApi"])

# MetaApi 配置 - 账户专用 Token (2026-04-22 更新)
METAAPI_TOKEN = (
    "eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI3MTI1Mzc1MTA0YjcwNjVkNzliNDMwMDRiMjMwYjkyYyIsImFjY2Vzc1J1bGVzIjpbeyJpZCI6InRyYWRpbmctYWNjb3VudC1tYW5hZ2VtZW50LWFwaSIsIm1ldGhvZHMiOlsidHJhZGluZy1hY2NvdW50LW1hbmFnZW1lbnQtYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiXSwicmVzb3VyY2VzIjpbImFjY291bnQ6JFVTRVJfSUQkOjM3OTFlYzNmLTRlZjYtNDkzZi1iNDYwLTRjZGJjNDBlMzNlNCJdfSx7ImlkIjoibWV0YWFwaS1yZXN0LWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiYWNjb3VudDokVVNFUl9JRCQ6Mzc5MWVjM2YtNGVmNi00OTNmLWI0NjAtNGNkYmM0MGUzM2U0Il19LHsiaWQiOiJtZXRhYXBpLXJwYy1hcGkiLCJtZXRob2RzIjpbIm1ldGFhcGktYXBpOndzOnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyJhY2NvdW50OiRVU0VSX0lEJDozNzkxZWMzZi00ZWY2LTQ5M2YtYjQ2MC00Y2RiYzQwZTMzZTQiXX0seyJpZCI6Im1ldGFhcGktcmVhbC10aW1lLXN0cmVhbWluZy1hcGkiLCJtZXRob2RzIjpbIm1ldGFhcGktYXBpOndzOnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyJhY2NvdW50OiRVU0VSX0lEJDozNzkxZWMzZi00ZWY2LTQ5M2YtYjQ2MC00Y2RiYzQwZTMzZTQiXX0seyJpZCI6Im1ldGFzdGF0cy1hcGkiLCJtZXRob2RzIjpbIm1ldGFzdGF0cy1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciJdLCJyZXNvdXJjZXMiOlsiYWNjb3VudDokVVNFUl9JRCQ6Mzc5MWVjM2YtNGVmNi00OTNmLWI0NjAtNGNkYmM0MGUzM2U0Il19LHsiaWQiOiJyaXNrLW1hbmFnZW1lbnQtYXBpIiwibWV0aG9kcyI6WyJyaXNrLW1hbmFnZW1lbnQtYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiXSwicmVzb3VyY2VzIjpbImFjY291bnQ6JFVTRVJfSUQkOjM3OTFlYzNmLTRlZjYtNDkzZi1iNDYwLTRjZGJjNDBlMzNlNCJdfSx7ImlkIjoiY29weWZhY3RvcnktYXBpIiwibWV0aG9kcyI6WyJjb3B5ZmFjdG9yeS1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiYWNjb3VudDokVVNFUl9JRCQ6KjM3OTFlYzNmLTRlZjYtNDkzZi1iNDYwLTRjZGJjNDBlMzNlNCIsIio6JFVTRVJfSUQkOjM3OTFlYzNmLTRlZjYtNDkzZi1iNDYwLTRjZGJjNDBlMzNlNCIsInN0cmF0ZWd5OiRVU0VSX0lEJDozNzkxZWMzZi00ZWY2LTQ5M2YtYjQ2MC00Y2RiYzQwZTMzZTQiLCJwb3J0Zm9saW86JFVTRVJfSUQkOjM3OTFlYzNmLTRlZjYtNDkzZi1iNDYwLTRjZGJjNDBlMzNlNCIsInN1YnNjcmliZXI6JFVTRVJfSUQkOjM3OTFlYzNmLTRlZjYtNDkzZi1iNDYwLTRjZGJjNDBlMzNlNCJdfSx7ImlkIjoibXQtbWFuYWdlci1hcGkiLCJtZXRob2RzIjpbIm10LW1hbmFnZXItYXBpOnJlc3Q6ZGVhbGluZzoqOioiLCJtdC1tYW5hZ2VyLWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqMzc5MWVjM2YtNGVmNi00OTNmLWI0NjAtNGNkYmM0MGUzM2U0IiwibXQtbWFuYWdlcjokVVNFUl9JRCQ6Mzc5MWVjM2YtNGVmNi00OTNmLWI0NjAtNGNkYmM0MGUzM2U0IiwibXQtYWNjb3VudDokVVNFUl9JRCQ6Mzc5MWVjM2YtNGVmNi00OTNmLWI0NjAtNGNkYmM0MGUzM2U0IiwibXQtZ3JvdXA6JFVTRVJfSUQkOjM3OTFlYzNmLTRlZjYtNDkzZi1iNDYwLTRjZGJjNDBlMzNlNCJdfSx7ImlkIjoiYmlsbGluZy1hcGkiLCJtZXRob2RzIjpbImJpbGxpbmctYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOiozNzkxZWMzZi00ZWY2LTQ5M2YtYjQ2MC00Y2RiYzQwZTMzZTQiXX1dLCJpZ25vcmVSYXRlTGltaXRzIjpmYWxzZSwidG9rZW5JZCI6IjIwMjEwMjEzIiwiaW1wZXJzb25hdGVkIjpmYWxzZSwicmVhbFVzZXJJZCI6IjcxMjUzNzUxMDRiNzA2NWQ3OWI0MzAwNGIyMzBiOTJjIiwiaWF0IjoxNzc2MjY3OTUyfQ.WcqTOYOXcgH81r-UdLyWzUSZjVq2fwnE98HVC6fahDcikYavgTHm4AgdQqytBeYMUcSvxg_7qcjtpvTi6TpRq7TEMFpnwMu8A3jQLzJREkOtxipvrJKG7S8I3M1IWrInkBUodZ1RHKwZl86r9M3WPYhvtPtRnvDrEvBJhLKimYgssPNLVvLsCjX5-9J22H7A0TRQunsCmLt_idHKXBp7wW-zjv2z9agOXEHAsnijpgOy_tg3rDTVVRq6d6T4rxT7uVyJX5WNh4U4AsvN2hO5zAKfWYRN2xqrAw_b_C5YWXzguZ3GvUjkme31MfATBjmVl0IvUlKlUbqEuD_cey0D6IGjKmXW6A9gOckoGkWMFhUKngLlH08j0qAqTfP5sMtCFB8mqGyjHJsg0_wemP0wLafGbM_1n_LXV-2Iu90YBl_Zexv9wTzW1dtUsfNJnxc6F4Ip0zZf1A5ljo26w0rNuh_MQvpw_8j3Hun-YsBcqz1S_tURSFZ4oiUC43xhLO4DV3Uf4hX9CSwLWruRBn8uWMMWc_JcllJmX1YGJP48_1-8HjETuvwrzdw5kYfwbMvR_tfUnENjdgBT4XNDl7CL8ioIyowAGJGbGZ7l2RSF1um-OMBmPkgJ6gX4JPq1cBag1FTZYJLCcyy2z8AmbUrKSbUPlBMjobcs7srD8eRtR5c"
)
ACCOUNT_ID = "3791ec3f-4ef6-493f-b460-4cdbc40e33e4"

# 全局缓存和状态
_cached_data = None
_cache_time = 0
CACHE_TTL = 15  # 15秒缓存
_account_cache = None  # 账户对象长期缓存
_last_fetch_attempt = 0


class MetaPosition(BaseModel):
    id: str
    symbol: str
    type: str
    volume: float
    price: float
    currentPrice: float
    profit: float
    stopLoss: Optional[float] = None
    takeProfit: Optional[float] = None
    openTime: str


class MetaOrder(BaseModel):
    id: str
    symbol: str
    type: str
    volume: float
    price: float
    state: str
    createdAt: str


class DashboardData(BaseModel):
    connected: bool
    account_name: str
    server: str
    balance: float
    equity: float
    margin: float
    free_margin: float
    margin_level: float
    currency: str
    positions: List[MetaPosition]
    orders: List[MetaOrder]
    last_update: str
    error: Optional[str] = None


async def fetch_metaapi_data() -> DashboardData:
    """获取 MetaApi 真实账户数据（带重试和缓存）"""
    global _cached_data, _cache_time, _account_cache, _last_fetch_attempt

    now = time.time()

    # 返回缓存数据
    if _cached_data is not None and (now - _cache_time) < CACHE_TTL:
        return _cached_data

    # 防止并发重复请求（30秒内只请求一次）
    if now - _last_fetch_attempt < 30 and _cached_data is not None:
        return _cached_data
    _last_fetch_attempt = now

    try:
        from metaapi_cloud_sdk import MetaApi

        api = MetaApi(token=METAAPI_TOKEN)
        account = _account_cache

        # 获取账户（带重试）
        if account is None:
            for attempt in range(3):
                try:
                    account = await api.metatrader_account_api.get_account(ACCOUNT_ID)
                    _account_cache = account
                    break
                except Exception as e:
                    print(f"[MetaApi] get_account attempt {attempt+1} failed: {str(e)[:80]}")
                    if attempt < 2:
                        await asyncio.sleep(2 * (attempt + 1))  # 指数退避
                    else:
                        return DashboardData(
                            connected=False, account_name="", server="",
                            balance=0, equity=0, margin=0, free_margin=0, margin_level=0,
                            currency="USD", positions=[], orders=[],
                            last_update=time.strftime("%Y-%m-%d %H:%M:%S"),
                            error=f"Account unavailable after 3 attempts: {str(e)[:200]}"
                        )

        if account is None:
            return DashboardData(
                connected=False, account_name="", server="",
                balance=0, equity=0, margin=0, free_margin=0, margin_level=0,
                currency="USD", positions=[], orders=[],
                last_update=time.strftime("%Y-%m-%d %H:%M:%S"),
                error="Account not found"
            )

        # 建立 RPC 连接
        connection = account.get_rpc_connection()
        await connection.connect()

        # 等待同步（带超时）
        try:
            await asyncio.wait_for(connection.wait_synchronized(), timeout=120)
        except asyncio.TimeoutError:
            print("[MetaApi] Synchronization timeout, using cached data if available")
            if _cached_data is not None:
                return _cached_data

        # 获取账户信息
        info = await connection.get_account_information()

        # 获取持仓
        positions = []
        try:
            mt_positions = await connection.get_positions()
            for p in mt_positions:
                positions.append(MetaPosition(
                    id=str(p.get("id", "")),
                    symbol=p.get("symbol", ""),
                    type=p.get("type", "BUY"),
                    volume=(p.get("volume", 0) or 0) / 100.0,
                    price=p.get("openPrice", 0),
                    currentPrice=p.get("currentPrice", 0),
                    profit=p.get("profit", 0),
                    stopLoss=p.get("stopLoss", 0) or None,
                    takeProfit=p.get("takeProfit", 0) or None,
                    openTime=str(p.get("time", ""))[:19] if p.get("time") else ""
                ))
        except Exception as e:
            print(f"[MetaApi] get_positions error: {e}")

        # 获取订单
        orders = []
        try:
            mt_orders = await connection.get_orders()
            for o in mt_orders:
                orders.append(MetaOrder(
                    id=str(o.get("id", "")),
                    symbol=o.get("symbol", ""),
                    type=o.get("type", ""),
                    volume=(o.get("volume", 0) or 0) / 100.0,
                    price=o.get("currentPrice", 0) or o.get("price", 0),
                    state=o.get("state", ""),
                    createdAt=str(o.get("createdAt", ""))[:19] if o.get("createdAt") else ""
                ))
        except Exception as e:
            print(f"[MetaApi] get_orders error: {e}")

        result = DashboardData(
            connected=True,
            account_name=account.name or "MT5 Account",
            server=info.get("server", account.server or "InfinoxLimited-MT5Live"),
            balance=info.get("balance", 0),
            equity=info.get("equity", 0),
            margin=info.get("margin", 0),
            free_margin=info.get("freeMargin", 0),
            margin_level=info.get("marginLevel", 0),
            currency=info.get("currency", "USD"),
            positions=positions,
            orders=orders,
            last_update=time.strftime("%Y-%m-%d %H:%M:%S"),
            error=None
        )

        _cached_data = result
        _cache_time = now
        return result

    except ImportError as e:
        return DashboardData(
            connected=False, account_name="", server="",
            balance=0, equity=0, margin=0, free_margin=0, margin_level=0,
            currency="USD", positions=[], orders=[],
            last_update=time.strftime("%Y-%m-%d %H:%M:%S"),
            error=f"SDK not found: {str(e)}"
        )
    except Exception as e:
        return DashboardData(
            connected=False, account_name="", server="",
            balance=0, equity=0, margin=0, free_margin=0, margin_level=0,
            currency="USD", positions=[], orders=[],
            last_update=time.strftime("%Y-%m-%d %H:%M:%S"),
            error=str(e)
        )


@router.get("/dashboard", response_model=DashboardData)
async def get_metaapi_dashboard():
    """获取 MetaApi 账户仪表盘数据"""
    return await fetch_metaapi_data()


@router.get("/positions", response_model=List[MetaPosition])
async def get_metaapi_positions():
    """获取 MetaApi MT5 实时持仓"""
    result = await fetch_metaapi_data()
    return result.positions


@router.get("/health")
async def metaapi_health():
    """MetaApi 连接健康检查"""
    result = await fetch_metaapi_data()
    return {
        "connected": result.connected,
        "account": result.account_name,
        "server": result.server,
        "balance": result.balance,
        "equity": result.equity,
        "positions_count": len(result.positions),
        "last_update": result.last_update,
        "error": result.error
    }
