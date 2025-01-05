from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from app.config import Config
from pydantic import BaseModel
from typing import List
from sqlalchemy import select, delete

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

async def get_things(out_schema:BaseModel, model:Base, **kwargs) -> List[BaseModel]:
    async with session_factory() as session:
        try:
            query = select(model).filter_by(**kwargs)
            result = await session.execute(query)
            things_info = result.scalars().all()

            things = [out_schema.model_validate(thing) for thing in things_info]
            return things

        except Exception as e:
            print(e.__class__, e)
            raise e

async def delete_thing(schema_info: BaseModel, model: Base):
    async with session_factory() as session:
        try:
            dict_to_find = {key: value for key, value in schema_info.model_dump().items() if value is not None}
            stmt = delete(model).filter_by(**dict_to_find)
            await session.execute(stmt)
            await session.commit()
        except Exception as e:
            print(e.__class__, e)
            raise e

async def add_thing(schema_in: BaseModel, model: Base) -> None:
    async with session_factory() as session:
        try:
            menu_dict = schema_in.model_dump()
            session.add(model(**menu_dict))
            await session.flush()
            await session.commit()
        except Exception as e:
            print("we have exception", e.__class__, e)
            raise e