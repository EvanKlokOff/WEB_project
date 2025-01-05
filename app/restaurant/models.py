from app.DBmanager import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.restaurant.food_type import food_types

class Menu(Base):
    __tablename__ = 'menus'
    food_name: Mapped[str] = mapped_column(unique=True)
    food_cost: Mapped[float]
    food_description: Mapped[str|None]
    food_type: Mapped[food_types|None]
    food_photo_path: Mapped[str] = mapped_column(unique=True)

class Table(Base):
    __tablename__ = 'tables'
    max_guest_amount: Mapped[int]
    users: Mapped[list['Users']] = relationship(  # Связь многие ко многим
        secondary="user_table_association",  # Указываем ассоциативную таблицу
        back_populates='tables'  # Обратная связь
    )