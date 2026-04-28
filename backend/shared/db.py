import os
from contextlib import contextmanager
from typing import Generator

import psycopg2
from psycopg2.pool import SimpleConnectionPool
import redis

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
POSTGRES_DB = os.getenv("POSTGRES_DB", "cenconsud2")
POSTGRES_USER = os.getenv("POSTGRES_USER", "cenconsud2_user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "supersecret")

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

_pg_pool: SimpleConnectionPool | None = None
_redis_client: redis.Redis | None = None


def get_pg_pool() -> SimpleConnectionPool:
    global _pg_pool
    if _pg_pool is None:
        _pg_pool = SimpleConnectionPool(
            minconn=1,
            maxconn=10,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            dbname=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
        )
    return _pg_pool


def get_redis_client() -> redis.Redis:
    global _redis_client
    if _redis_client is None:
        _redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    return _redis_client


@contextmanager
def get_db_session() -> Generator:
    pool = get_pg_pool()
    conn = pool.getconn()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        pool.putconn(conn)