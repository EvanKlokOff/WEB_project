from app.restaurant.models import Menu, Table
from app.authorization.models import User_Tables_association, Users
from app.DBmanager import session_factory
from app.authorization.schemas import User_ORM_
from app.restaurant.schemas import (Menu_In,
                                    Menu_info,
                                    Menu_out,
                                    Table_config,
                                    Order_Table_in,
                                    User_Tables_association_out,
                                    User_Tables_association_info
                                    )
from sqlalchemy import select, delete, cast, Date, update
from restaurant import LIMIT_OF_TABLE, LIMIT_OF_GUEST_ON_TABLE
from typing import List

from restaurant.schemas import Order_Table_in, Table_config_out


async def add_food_to_menu(menu: Menu_In) -> None:
    async with session_factory() as session:
        try:
            menu_dict = menu.model_dump()
            print(menu_dict, "refresh token dict")
            session.add(Menu(**menu_dict))
            await session.flush()
            await session.commit()
        except Exception as e:
            print("we have exception", e)

async def delete_food_from_menu(menu_id: int) -> None:
    async with session_factory() as session:
        try:
            await session.execute(delete(Menu).filter_by(id = menu_id))
            await session.commit()
        except Exception as e:
            print(e.__class__, e)
            print("we have exception", e)


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
    menus = await get_menu()
    menus_ = [menu.model_dump() for menu in menus]
    return menus_

async def get_menu(**menu_data) -> List[Menu_out]:
    async with session_factory() as session:
        try:
            querry = select(Menu).filter_by(**menu_data)
            result = await session.execute(querry)
            menu_info = result.scalars().all()

            menus = list()
            for menu in menu_info:
                menus.append(Menu_out.model_validate(menu))
            return menus
        except Exception as e:
            print(e.__class__, e)

async def add_table(guest_limit:int = LIMIT_OF_GUEST_ON_TABLE)->None:
    async with session_factory() as session:
        try:
            table = Table_config(max_guest_amount=guest_limit)
            session.add(Table(**table.model_dump()))
            await session.flush()
            await session.commit()
        except Exception as e:
            print(e.__class__, e)

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

async def book_table(booking_info: Order_Table_in) -> User_Tables_association_out | None:
    async with session_factory() as session:
        try:
            order_date = booking_info.order_time.date() #дата без времени
            # Формируем запрос для поиска свободных столиков на указанную дату
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
            if not tables_info: #нет никаких столов, поэтому добавляем новый занятый стол
                dict_to_add = booking_info.model_dump()
                dict_to_add.update(is_free=False, table_id=1)
                session.add(User_Tables_association(**dict_to_add))
                user_table_ass = User_Tables_association_out.model_validate(dict_to_add)
            else:
                #столы есть, но мы не знаем их статус
                #поэтому перебираем все найденные столы, если среди них найдётся свободный, то занимаем
                for table in tables_info:
                    if (table.is_free):
                        table_to_book = tables_info
                        user_table_ass = User_Tables_association_out(
                                                                     order_time=booking_info.order_time,
                                                                     guest_amount=booking_info.guests_number,
                                                                     extra_wishes=booking_info.extra_wishes,
                                                                     is_free=False,
                                                                     user_id=booking_info.user_id,
                                                                     table_id=table_to_book.table_id
                                                                     )
                        # Обновляем запись, чтобы пометить столик как занятый
                        update_stmt = (
                            update(User_Tables_association)
                            .filter_by(table_id=table_to_book.id)
                            .values(
                                **user_table_ass.model_dump()
                            )
                        )
                        await session.execute(update_stmt)
                        break
                # если свободный не найдётся, то в зависимости от кол-ва столов, можно добавить ещё один стол
                # либо сказать, что свободных мест нет
                if not user_table_ass:
                    if(len(tables_info)) <= LIMIT_OF_TABLE:
                        dict_to_add = booking_info.model_dump()
                        dict_to_add.update(is_free=False, table_id=tables_info[-1].table_id+1)
                        session.add(User_Tables_association(**dict_to_add))
                        user_table_ass = User_Tables_association_out.model_validate(dict_to_add)
                    else:
                        raise Exception("Not enough free tables")
            await session.commit()
            return user_table_ass
        except Exception as e:
            print(e.__class__, e)

async def free_table(order_info: User_Tables_association_info) -> None:
    async with session_factory() as session:
        try:
            select_stmt=(
                select(User_Tables_association).filter_by(**order_info.model_dump())
            )
            result = await session.execute(select_stmt)
            booked_table = result.scalar_one()
            booked_table.is_free=True

            await session.flush()
            await session.commit()
        except Exception as e:
            print(e.__class__, e)

async def change_table_booking(order_info: User_Tables_association_info,
                               booking_info: Order_Table_in) -> None:
   await free_table(order_info)
   await book_table(booking_info)

async def get_all_tables():
    tables = await get_tables_info()
    tables_=[]
    for table in tables:
        dict_to_add = {
                       "user_table_association": table["user_table_association"].model_dump(),
                       "user":table["user"].model_dump(),
                       "table": table["table"].model_dump()
                       }
        tables_.append(dict_to_add)
    return tables_

async def get_tables_info(**kwargs) -> List[dict]:
    async with session_factory() as session:
        stmt =(
            select(User_Tables_association, Table, Users)
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

