from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database.session import Base

class tgUsers(Base):
    __tablename__="tgUsers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tgId: Mapped[int] = mapped_column()


class Subject(Base):
    __tablename__ = "subject"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True,nullable=True)

class Lecture(Base):
    __tablename__ = "lectures"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    subject: Mapped[str] = mapped_column(nullable=False)
    date: Mapped[str] = mapped_column(nullable=False)
    file_id: Mapped[str] = mapped_column(nullable=False)

class Admin(Base):
    __tablename__ = "admins"
    user_id: Mapped[str] = mapped_column(primary_key=True)

class Teacher(Base):
    __tablename__ = "teachers"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    teacher : Mapped[str] = mapped_column()
    mood: Mapped[str] = mapped_column()
    subject: Mapped[str] = mapped_column()

class Schedule(Base):
    __tablename__ = "schedule"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    week : Mapped[str] = mapped_column()
    day : Mapped[str] = mapped_column()
    hour : Mapped[str] = mapped_column()
    subgroup : Mapped[int] = mapped_column()
    subject : Mapped[str] = mapped_column()
    classroom : Mapped[str] = mapped_column()
    teacher : Mapped[str] = mapped_column()

class Subgroup(Base):
    __tablename__ = "subgroup"

    id : Mapped[int] = mapped_column(primary_key=True, index=True)
    tgId : Mapped[int] = mapped_column()
    subgroup : Mapped[int] = mapped_column()