from sqlalchemy import ForeignKey, String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from datetime import datetime

from config import DB_URL

engine = create_async_engine(url=DB_URL,
                             echo=True)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    balance: Mapped[str] = mapped_column(String(15))


class AIType(Base):
    __tablename__ = 'ai_types'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))


class AIModel(Base):
    __tablename__ = 'ai_model'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))
    ai_type: Mapped[int] = mapped_column(ForeignKey('ai_types.id'))
    price: Mapped[str] = mapped_column(String(25))


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column(String(50))
    user: Mapped[str] = mapped_column(ForeignKey('users.id'))
    amount: Mapped[str] = mapped_column(String(15))
    create_at: Mapped[datetime]
    order: Mapped[str] = mapped_column(String(100))


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
