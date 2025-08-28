from sqlalchemy import select

from database.session import engine, Base, async_session
from database.models import tgUsers

#Создание таблицы
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

#Добавление в таблицу tgUsers
async def set_user(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(select(tgUsers).where(tgUsers.tgId == tg_id))

        if not user:
            session.add(tgUsers(tgId=tg_id))
            await session.commit()