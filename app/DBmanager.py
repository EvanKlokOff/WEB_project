from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from app.config import Config

engine = create_async_engine(
    url=Config.db_url,
    echo=True
)

session_factory = async_sessionmaker(engine, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    __abstract__=True
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    # updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    def __repr__(self)->str:
        columns = [f"{col}={getattr(self, col)}" for col in self.__table__.columns.keys()]
        return f"{self.__class__.__name__} {','.join(columns)}"