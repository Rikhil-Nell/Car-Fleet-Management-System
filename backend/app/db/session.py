from sqlalchemy.orm import sessionmaker
from app.core.config import ModeEnum, settings
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.pool import NullPool, AsyncAdaptedQueuePool

DB_POOL_SIZE = 83
WEB_CONCURRENCY = 9
POOL_SIZE = max(DB_POOL_SIZE // WEB_CONCURRENCY, 5)

connect_args = {"ssl": "require"}

engine = create_async_engine(
    str(settings.ASYNC_DATABASE_URI),
    echo=False,
    poolclass=NullPool
    if settings.MODE == ModeEnum.testing
    else AsyncAdaptedQueuePool,
    pool_size=POOL_SIZE,
    max_overflow=64,
    connect_args = connect_args
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
