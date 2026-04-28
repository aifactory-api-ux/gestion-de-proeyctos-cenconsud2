import json
import logging
from functools import wraps
from typing import Any, Callable

from .db import get_redis_client

logger = logging.getLogger(__name__)


def cache_result(key_prefix: str, ttl: int = 300) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            cache_key = f"{key_prefix}:{json.dumps(args)}:{json.dumps(kwargs)}"
            redis_client = get_redis_client()
            cached = redis_client.get(cache_key)
            if cached:
                logger.debug(f"Cache hit for {cache_key}")
                return json.loads(cached)
            result = await func(*args, **kwargs)
            redis_client.setex(cache_key, ttl, json.dumps(result))
            return result
        return wrapper
    return decorator


def format_currency(amount: float) -> str:
    return f"${amount:,.2f}"


def setup_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )