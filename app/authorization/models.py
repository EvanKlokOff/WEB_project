from datetime import datetime
from app.DBmanager import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.authorization.roles import Roles

class User_Tables_association(Base):
    __tablename__ = "user_table_association"
    order_time: Mapped[datetime]
    guest_amount: Mapped[int]
    extra_wishes: Mapped[str|None]
    is_free: Mapped[bool] = mapped_column(default=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"))
    table_id: Mapped[int] = mapped_column(ForeignKey('tables.id', ondelete="CASCADE"))

class Users(Base):
    __tablename__ = 'users'
    user_name: Mapped[str]
    email_address: Mapped[str]=mapped_column(unique=True)
    hashed_password: Mapped[bytes]
    user_role: Mapped[Roles] = mapped_column(default=Roles.AUTHORIZED_USER)
    sessions:Mapped['Session'] = relationship(back_populates='users', uselist=False)
    tables: Mapped[list['Table']] = relationship(  # Связь многие ко многим
        secondary='user_table_association',  # Указываем ассоциативную таблицу
        back_populates='users'  # Обратная связь
    )
class Session(Base):
    __tablename__ = 'Sessions'
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), unique=True)
    refresh_token: Mapped[str]
    expire_in: Mapped[datetime]
    created_at: Mapped[datetime]
    users:Mapped['Users'] = relationship(back_populates='sessions', uselist=False)
