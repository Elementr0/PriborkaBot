from config import  DATABASE_URL

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import  DeclarativeBase


class Base(AsyncAttrs, DeclarativeBase):
    pass

engine = create_async_engine(
    url= DATABASE_URL,
    echo=False
)

async_session = async_sessionmaker(
    engine
)