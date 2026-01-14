# app/core/permission_cache.py
from app.core.redis import redis_client


def perm_cache_key(user_id: int, app_code: str) -> str:
    return f"perm:{user_id}:{app_code}"


def invalidate_user_permission(user_id: int, app_code: str):
    key = perm_cache_key(user_id, app_code)
    redis_client.delete(key)


def invalidate_user_app_permission(user_id: int, app_code: str):
    key = perm_cache_key(user_id, app_code)
    redis_client.delete(key)


def invalidate_user_all_permissions(user_id: int):
    pattern = f"perm:{user_id}:*"
    keys = redis_client.keys(pattern)
    if keys:
        redis_client.delete(*keys)


def invalidate_user_all_apps(user_id: int):
    pattern = f"perm:{user_id}:*"
    keys = redis_client.keys(pattern)
    if keys:
        redis_client.delete(*keys)


def invalidate_role_permissions(role_id: int, app_code: str):
    """
    Kalau role berubah → semua user dengan role tsb harus di-invalidate.
    (dipakai di admin permission assignment)
    """
    # ⚠️ di sini JANGAN query DB user langsung
    # trigger di service yang sudah tahu user mana saja
    pass
