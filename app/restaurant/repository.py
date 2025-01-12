from app.restaurant.models import Menu, Table
from app.authorization.models import User_Tables_association, Users
from app.DBmanager import session_factory
from app.authorization.schemas import User_ORM_
from fastapi import HTTPException, status
from app.restaurant.schemas import (Menu_In,
                                    Menu_info,
                                    Menu_out,
                                    Table_config,
                                    Order_Table_in,
                                    User_Tables_association_out,
                                    User_Tables_association_info
                                    )
import app.restaurant as rest
from sqlalchemy import select, delete, cast, Date
from restaurant import LIMIT_OF_TABLE, LIMIT_OF_GUEST_ON_TABLE, MAX_AMOUNT_TABLE_PER_DAY
from typing import List
from app.DBmanager import get_things

from restaurant.schemas import Order_Table_in, Table_config_out

async def change_food_in_menu(menu_info:Menu_info,
                              menu_change: Menu_info) -> None:
    async with session_factory() as session:
        try:
            dict_to_find = {key: value for key, value in menu_info.model_dump().items() if value is not None}
            result = await session.execute(select(Menu).filter_by(**dict_to_find))
            obj = result.scalars().first()
        except Exception as e:
            print(e.__class__, e)
        if obj:
            print(menu_change.model_dump())
            for key, value in menu_change.model_dump().items():
                if value:
                    print(key, value)
                    setattr(obj, key, value)
            await session.commit()
        else:
            raise Exception(f"there are no food {menu_info.model_dump()}")

async def get_all_menus() -> List[dict]:
    menus = await get_things(Menu_out, Menu)
    menus_ = [menu.model_dump() for menu in menus]
    return menus_

async def add_tables(table_quantity: int = LIMIT_OF_TABLE,
                     guest_limit:int = LIMIT_OF_GUEST_ON_TABLE)->None:
    async with session_factory() as session:
        try:
            for i in range(table_quantity):
                table = Table_config(max_guest_amount=guest_limit)
                session.add(Table(**table.model_dump()))
            await session.flush()
            await session.commit()
        except Exception as e:
            print(e.__class__, e)

async def check_constraint(booking_info: Order_Table_in, max_amount_table_on_user: int = MAX_AMOUNT_TABLE_PER_DAY)->bool:
    async with session_factory() as session:
        try:
            order_date = booking_info.order_time.date()  # дата без времени
            # Формируем запрос для занятых столиков на указанную дату
            stmt = (
                select(User_Tables_association)
                .filter(
                    cast(User_Tables_association.order_time, Date) == order_date,
                    User_Tables_association.user_id == booking_info.user_id# Фильтр по дате
                )
            )
            result = await session.execute(stmt)
            tables_info = result.scalars().all()
            return len(tables_info) < max_amount_table_on_user
        except Exception as e:
            print(e.__class__, e)
            raise e


async def book_table(booking_info: Order_Table_in) -> User_Tables_association_out | None:
    async with session_factory() as session:
        try:
            print("БРОНИРОВАНИЕ СТОЛА______________________")
            order_date = booking_info.order_time.date() #дата без времени
            # Формируем запрос для занятых столиков на указанную дату
            stmt = (
                select(User_Tables_association)
                .filter(
                    cast(User_Tables_association.order_time, Date) == order_date  # Фильтр по дате
                )
                .order_by(User_Tables_association.table_id.asc())  # Сортировка по table_id
            )

            # Выполняем запрос
            result = await session.execute(stmt)
            tables_info = result.scalars().all()
            user_table_ass=None

            print(tables_info,[table.__repr__() for table in tables_info])
            if not tables_info: #нет занятых столов на выбранную дату, поэтому добавляем новый занятый стол
                print("нет столов на текущую дату")
                dict_to_add = booking_info.model_dump()
                dict_to_add.update(table_id=1)
                session.add(User_Tables_association(**dict_to_add))
                user_table_ass = User_Tables_association_out.model_validate(dict_to_add)
            else:
                ordered_tables_id = {table.table_id for table in tables_info}
                free_table_id = None
                for i in range(LIMIT_OF_TABLE):
                    if (i+1) not in ordered_tables_id:
                        free_table_id = i + 1
                        break
                # занятые столы есть, поэтому нужно проверить их количество и проверить, что места точно хватит
                if free_table_id:
                    dict_to_add = booking_info.model_dump()
                    dict_to_add.update(table_id=free_table_id)
                    session.add(User_Tables_association(**dict_to_add))
                    user_table_ass = User_Tables_association_out.model_validate(dict_to_add)
                else:
                    await session.rollback()
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=rest.NOT_ENOUGH_FREE_TABLE)
            await session.commit()
            return user_table_ass
        except Exception as e:
            print(e.__class__, e)
            raise e

async def free_table(order_info: User_Tables_association_info) -> None:
    async with session_factory() as session:
        try:
            order_info_ = {k:v for k,v in order_info.model_dump().items() if v is not None}
            delete_stmt=(
                delete(User_Tables_association).filter_by(**order_info_)
            )
            await session.execute(delete_stmt)
            await session.commit()
        except Exception as e:
            print(e.__class__, e)
            raise e

async def change_table_booking(order_info: User_Tables_association_info,
                               booking_info: Order_Table_in) -> None:
   await free_table(order_info)
   await book_table(booking_info)

async def get_all_tables() -> List[dict]:
    tables = await get_all_tables_info()
    tables_=[]
    for table in tables:
        dict_to_add = {
                       "user_table_association": table["user_table_association"].model_dump(),
                       "user":table["user"].model_dump(),
                       "table": table["table"].model_dump()
                       }
        tables_.append(dict_to_add)
    return tables_


async def get_tables_of_user(**kwargs):
    tables = await get_all_tables_info(**kwargs)
    tables_ = []
    for table in tables:
        dict_to_add = {
            "user_table_association": table["user_table_association"].model_dump(),
            "user": table["user"].model_dump(),
            "table": table["table"].model_dump()
        }
        tables_.append(dict_to_add)
    return tables_


async def get_all_tables_info(**kwargs) -> List[dict]:
    async with session_factory() as session:
        stmt =(
            select(User_Tables_association, Table, Users)
            .filter_by(**kwargs)
            .join(Table, User_Tables_association.table_id == Table.id)
            .join(Users, User_Tables_association.user_id == Users.id)
            .order_by(User_Tables_association.order_time.asc())
        )
        result = await session.execute(stmt)
        associations = result.all()
        result_list = list()
        for association in associations:
            user_table_association, table, user = association
            # нужно создать объекты pydantic для user, user_table_association, table
            user_table_association_ = User_Tables_association_out.model_validate(user_table_association)
            table_ = Table_config_out.model_validate(table)
            user_ = User_ORM_.model_validate(user)
            result_list.append(
                                {"user_table_association":user_table_association_,
                                "user":user_,
                                "table": table_
                                 }
                               )
        return result_list

