from sqlalchemy.orm import Mapped, mapped_column

from database.session import Base

class tgUsers(Base):
    __tablename__="tgUsers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tgId: Mapped[int] = mapped_column()
