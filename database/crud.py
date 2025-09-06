from typing import List, Dict, Optional

from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from database.session import engine, Base, async_session
from database.models import tgUsers, Subject, Lecture, Admin, Teacher, Schedule, Subgroup

from sqlalchemy import select
from typing import List, Dict

# Создание таблиц
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Добавление в таблицу tgUsers
async def set_user(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(select(tgUsers).where(tgUsers.tgId == tg_id))

        if not user:
            session.add(tgUsers(tgId=tg_id))
            await session.commit()

async def get_subjects():
    async with async_session() as session:
        result = await session.execute(select(Subject))
        return result.scalars().all()

async def get_photos_for_subject_date(subject, date):
    async with async_session() as session:
        result = await session.execute(
            select(Lecture.file_id).where(Lecture.subject == subject, Lecture.date == date)
        )
        return result.scalars().all()

async def add_subject(name):
    async with async_session() as session:
        exists = await session.scalar(
            select(Subject).where(Subject.name == name)
        )
        if exists:
            return False
        new_subject = Subject(name=name)
        session.add(new_subject)
        await session.commit()
        return True

async def delete_subject(subject):
    async with async_session() as session:
        subject_obj = await session.scalar(
            select(Subject).where(Subject.name == subject)
        )
        if subject_obj:
            await session.execute(
                delete(Lecture).where(Lecture.subject == subject)
            )
            await session.delete(subject_obj)
            await session.commit()
            return True
        return False

async def get_dates_for_subject(subject):
    async with async_session() as session:
        result = await session.execute(
            select(Lecture.date).where(Lecture.subject == subject).distinct()
        )
        return result.scalars().all()

async def add_lecture(subject, date, file_id):
    async with async_session() as session:
        lecture = Lecture(subject=subject, date=date, file_id=file_id)
        session.add(lecture)
        await session.commit()  # Добавлен await
        await session.refresh(lecture)  # Опционально: обновляем объект
        return lecture

async def is_admin(user_id: str) -> bool:
    async with async_session() as session:
        result = await session.execute(select(Admin).where(Admin.user_id == user_id))
        return result.scalar_one_or_none() is not None

async def add_admin(user_id: str) -> bool:
    async with async_session() as session:
        admin = Admin(user_id=user_id)
        session.add(admin)
        try:
            await session.commit()
            return True
        except IntegrityError:
            await session.rollback()
            return False

async def get_admins() -> list[str]:
    async with async_session() as session:
        result = await session.execute(select(Admin.user_id))
        return [row[0] for row in result.all()]


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Dict


async def get_day(week: str, day: str, subgroup: int) -> List[Dict]:
    async with async_session() as session:
        from sqlalchemy import select

        # Запрашиваем ВСЕ поля которые есть в модели
        stmt = select(
            Schedule.subject,
            Schedule.hour,
            Schedule.classroom,  # Добавляем classroom
            Schedule.teacher  # Добавляем teacher
        ).where(
            Schedule.week == week,
            Schedule.day == day,
            Schedule.subgroup == subgroup
        ).order_by(Schedule.hour)

        result = await session.execute(stmt)
        records = result.all()

        return [
            {
                "subject": subject,
                "hour": hour,
                "classroom": classroom or "Не указано",  # Защита от None
                "teacher": teacher or "Не указан"  # Защита от None
            }
            for subject, hour, classroom, teacher in records
        ]


async def get_day_full(week: str, day: str, subgroup: int) -> List[Dict]:
    """
    Возвращает полное расписание со всеми полями
    """
    async with async_session() as session:
        stmt = select(Schedule).where(
            Schedule.week == week,
            Schedule.day == day,
            Schedule.subgroup == subgroup
        ).order_by(Schedule.hour)

        result = await session.execute(stmt)
        schedules = result.scalars().all()

        return [
            {
                "subject": schedule.subject,
                "hour": schedule.hour,
                "classroom": schedule.classroom,
                "teacher": schedule.teacher,
                "week": schedule.week,
                "day": schedule.day,
                "subgroup": schedule.subgroup
            }
            for schedule in schedules
        ]


async def check_tgid_exists(tgId: int) -> bool:
    """
    Проверяет, существует ли пользователь с указанным tgId в базе данных

    Args:
        tgId: ID пользователя в Telegram

    Returns:
        bool: True если пользователь существует, False если нет
    """
    async with async_session() as session:
        try:
            # Создаем запрос
            stmt = select(Subgroup).where(Subgroup.tgId == tgId)

            # Выполняем запрос
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()

            # Возвращаем True если пользователь найден, False если нет
            return user is not None

        except Exception as e:
            print(f"Ошибка при проверке пользователя: {e}")
            return False

async def get_subgroup(tgId: int) -> Optional[int]:
    """
    Возвращает подгруппу пользователя по его tgId

    Args:
        tgId: ID пользователя в Telegram

    Returns:
        int: номер подгруппы или None если не найден
    """
    async with async_session() as session:
        try:
            # Создаем запрос
            stmt = select(Subgroup.subgroup).where(Subgroup.tgId == tgId)

            # Выполняем запрос
            result = await session.execute(stmt)
            subgroup = result.scalar_one_or_none()

            return subgroup

        except Exception as e:
            print(f"Ошибка при получении подгруппы: {e}")
            return None


async def set_subgroup(tgId: int, subgroup: int) -> bool:
    """
    Устанавливает или изменяет подгруппу пользователя

    Args:
        tgId: ID пользователя в Telegram
        subgroup: Номер подгруппы (1 или 2)

    Returns:
        bool: True если успешно, False если ошибка
    """
    async with async_session() as session:
        try:
            # Проверяем существование пользователя
            stmt = select(Subgroup).where(Subgroup.tgId == tgId)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()

            if user:
                # Обновляем существующую запись
                user.subgroup = subgroup
                await session.commit()
                return True
            else:
                # Создаем новую запись
                new_user = Subgroup(tgId=tgId, subgroup=subgroup)
                session.add(new_user)
                await session.commit()
                return True

        except Exception as e:
            print(f"❌ Ошибка установки подгруппы: {e}")
            await session.rollback()
            return False

async def fill_schedule(data: List[Dict]):
    """
    Заполняет таблицу schedule данными с новой структурой
    """
    async with AsyncSession(engine) as session:
        for item in data:
            # Проверяем, существует ли уже запись
            stmt = select(Schedule).where(
                Schedule.week == item['week'],
                Schedule.day == item['day'],
                Schedule.hour == item['hour'],
                Schedule.subgroup == item['subgroup']
            )
            result = await session.execute(stmt)
            existing = result.scalar_one_or_none()

            if not existing:
                # Создаем новую запись с учетом всех полей
                schedule = Schedule(
                    week=item['week'],
                    day=item['day'],
                    hour=item['hour'],
                    subgroup=item['subgroup'],
                    subject=item['subject'],
                    classroom=item['classroom'],
                    teacher=item['teacher']
                )
                session.add(schedule)

        await session.commit()

async def get_teacher():
    async with async_session() as session:
        stmt = select(Teacher)
        result = await session.execute(stmt)
        teachers = result.scalars().all()
        return [teacher.__dict__ for teacher in teachers]

async def set_teacher(teacher: str, mood: str, subject: str) -> bool:
    async  with async_session() as session:
        teacher = Teacher(teacher = teacher, mood = mood, subject = subject)

        session.add(teacher)
        try:
            await session.commit()
            return True
        except IntegrityError:
            await session.rollback()
            return False
