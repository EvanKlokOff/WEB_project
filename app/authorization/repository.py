from app.authorization.schemas import (User_API_in,
                                       User_ORM_out,
                                       User_info,
                                       Refresh_token,
                                       User_ORM_)
from app.DBmanager import session_factory
from app.authorization.models import (Users,
                                      Session)
from sqlalchemy import (select,
                        delete)
import app.authorization.utils as utils
from datetime import datetime
from typing import List


async def get_refresh_token_by_property(**kwargs) -> Refresh_token | None:
    async with session_factory() as session:
        try:
            stmt = select(Session).filter_by(**kwargs)
            result = await session.execute(stmt)
            item = result.scalars().one_or_none()
            if item:
                try:
                    return Refresh_token.model_validate(item)
                except Exception as e:
                    print(e.__class__)
        except Exception as e:
            print(e.__class__, e)
            return None

async def add_refresh_token_by(token: str|bytes) -> None:
    async with session_factory() as session:
        try:
            token_dict = utils.decode_jwt(token)
            print(token_dict, "refresh token dict")
            dict_to_add={
                'user_id': int(token_dict.get('sub')),
                'refresh_token': token,
                'expire_in': datetime.fromtimestamp(token_dict.get('exp')),
                'created_at': datetime.fromtimestamp(token_dict.get('iat'))
                }

            session.add(Session(**dict_to_add))
            await session.flush()
            await session.commit()
        except Exception as e:
            print("we have exception", e.__class__, e)
            raise e


async def delete_refresh_token_by_property(**kwargs) -> None:
    async with session_factory() as session:
        try:
            stmt = delete(Session).filter_by(**kwargs)
            await session.execute(stmt)
            await session.commit()
        except Exception as e:
            print(e.__class__, e)
            raise e

async def get_user_by_property(**kwargs) -> User_ORM_out | None:
    async with session_factory() as session:
        try:
            stmt = select(Users).filter_by(**kwargs)
            result = await session.execute(stmt)
            item = result.scalars().one_or_none()
            if item:
                try:
                    return User_ORM_out.model_validate(item)
                except Exception as e:
                    print(e.__class__)
        except Exception as e:
            print(e.__class__, e, "ошибка при выборке")
            return None

async def get_all_users() -> List[dict]:
    users = await get_users_by_property()
    users_ = [menu.model_dump() for menu in users]
    return users_

async def get_users_by_property(**kwargs) -> List[User_ORM_]:
    async with session_factory() as session:
        try:
            stmt = select(Users).filter_by(**kwargs)
            result = await session.execute(stmt)
            users_info = result.scalars().all()
            users=list()
            for user in users_info:
                users.append(User_ORM_out.model_validate(user))
            return users
        except Exception as e:
            print(e.__class__, e)
            raise e

async def get_user_by_email_and_name(user: User_API_in) -> User_ORM_out | None:
    return await get_user_by_property(user_name = user.user_name,email_address = user.email_address)

async def change_user(user_info: User_info,
                      new_data:User_info) -> None:
    async with session_factory() as session:
        try:
            dict_to_find = {key: value for key, value in user_info.model_dump().items() if value is not None}
            result = await session.execute(select(Users).filter_by(**dict_to_find))
            obj = result.scalars().first()
        except Exception as e:
            print(e.__class__, e)
        if obj:
            dict_to_update = new_data.model_dump()
            if new_data.password:
                dict_to_update.update(
                    hashed_password=utils.hash_password(new_data.password)
                )
                del dict_to_update["password"]

            for key, value in dict_to_update.items():
                if value:
                    print(key, value)
                    setattr(obj, key, value)
            await session.commit()
        else:
            raise ValueError(f"there are no user {user_info.model_dump()}")

async def add_new_user(user: User_API_in) -> None:
    async with session_factory() as session:
        try:
            user_dict = user.model_dump()
            user_dict.update(
                hashed_password = utils.hash_password(user.password)
            )
            del user_dict['password']
            print(user_dict, "user_dict")
            session.add(Users(**user_dict))
            await session.flush()
            await session.commit()
        except Exception as e:
            print(e.__class__, e)
            raise e

async def delete_user(user: User_info):
    async with session_factory() as session:
        try:
            dict_to_find = {key: value for key, value in user.model_dump().items() if value is not None}
            stmt = delete(Users).filter_by(**dict_to_find)
            await session.execute(stmt)
            await session.commit()
        except Exception as e:
            print(e.__class__, e)
            raise e
