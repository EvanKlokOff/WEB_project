from pydantic import BaseModel, Field, ConfigDict, BeforeValidator, model_validator, validate_email
from app.restaurant.food_type import food_types
import datetime
from typing import Annotated
from typing_extensions import Self
from fastapi import HTTPException, status
from app.restaurant import (LIMIT_OF_GUEST_ON_TABLE,
                            INVALID_DATE_AND_TIME_FORMAT,
                            INVALID_DATE_AND_TIME_VALUES,
                            TOO_MUCH_GUEST,
                            INVALID_GUEST_FORMAT,
                            INVALID_FOOD_TYPE_FORMAT,
                            INVALID_COST_TYPE,
                            INVALID_COST
                            )


def is_valid_food_type(value) -> food_types:
    if value:
        try:
            if isinstance(value, str):
                try:
                    food_type = food_types(value)
                    return food_type
                except:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=INVALID_FOOD_TYPE_FORMAT)
            elif isinstance(value, food_types):
                return value
        except:
            raise ValueError("wrong type")
        return None

def is_valid_cost(value) -> int:
    if value:
        if isinstance(value, float) or isinstance(value, int):
            if value>0:
                return float(value)
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=INVALID_COST)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=INVALID_COST_TYPE)
    else:
        return None

correct_food_type=Annotated[food_types, BeforeValidator(is_valid_food_type)]
correct_cost_type=Annotated[float, BeforeValidator(is_valid_cost)]

class Menu_In_Base_64_info(BaseModel):
    id: int|None = Field(None)
    food_name: None|str = Field(None)
    food_cost: None|correct_cost_type = Field(None)
    food_description:None|str = Field(None)
    food_type: None|correct_food_type = Field(None)
    food_image: None|str = Field(None)
    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode='after')
    def not_null_field(self) -> Self:
        if not any(self.__dict__.values()):
            raise ValueError("Three fields are None")
        return self

class Menu_In_Base_64(BaseModel):
    food_name: str
    food_cost: correct_cost_type
    food_description: str
    food_type: correct_food_type
    food_image: str # это base64 строка
    model_config = ConfigDict(from_attributes=True)

class Menu_In(BaseModel):
    food_name: str
    food_cost: correct_cost_type
    food_description: str
    food_type: correct_food_type
    food_photo_path: str
    model_config = ConfigDict(from_attributes=True)


class Menu_info(BaseModel):
    id: int|None = Field(None)
    food_name: str|None = Field(None)
    food_cost: correct_cost_type|None = Field(None, gt=0)
    food_description: str | None = Field(None)
    food_type: correct_food_type|None = Field(None)
    food_photo_path: str|None = Field(None)

    @model_validator(mode='after')
    def not_null_field(self) -> Self:
        if not any(self.__dict__.values()):
            raise ValueError("Three fields are None")
        return self

class Menu_out(Menu_In):
    id: int

def is_valid_date(value) -> datetime.datetime:
    if value:
        try:
            if isinstance(value, str):
                print(type(value))
                value = datetime.datetime.fromisoformat(value)
                print(type(value), value)
        except Exception as e:
            print (e.__class__, e)
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=INVALID_DATE_AND_TIME_FORMAT)
        if (datetime.datetime.now() > value) or (value > datetime.datetime.now() + datetime.timedelta(days=365*2)):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=INVALID_DATE_AND_TIME_VALUES)
        return value
    return None
def is_valid_amount_guest(value) -> int:
    if value:
        if isinstance(value, int):
            if 1 <= value<=LIMIT_OF_GUEST_ON_TABLE:
                return value
            else:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=TOO_MUCH_GUEST)
        if isinstance(value, str):
            num = int(value)
            if 1 <= num<=LIMIT_OF_GUEST_ON_TABLE:
                return num
            else:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=TOO_MUCH_GUEST)
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=INVALID_GUEST_FORMAT)
    else:
        return None
#обозначает конретный стол с его характеристиками
class Table_config(BaseModel):
    max_guest_amount: int = Field(LIMIT_OF_GUEST_ON_TABLE, gt=0)

class Table_config_out(BaseModel):
    id: int
    model_config = ConfigDict(from_attributes=True)

correct_date = Annotated[datetime.datetime, BeforeValidator(is_valid_date)]
correct_guest_amount = Annotated[int, BeforeValidator(is_valid_amount_guest)]
#обозначают детали бронирования стола
class Order_Table(BaseModel):
    order_time: correct_date  # проверка что нельзя заказать в прошлом
    guest_amount: correct_guest_amount = Field(default=1)  # проверка что нельзя позвать меньше нуля и больше 100
    extra_wishes: str|None = Field(None)

class Order_Table_in(Order_Table):
    user_id: int

class Order_Table_info(BaseModel):
    order_time: None|correct_date = Field(None) # проверка что нельзя заказать в прошлом
    guest_amount: None|correct_guest_amount = Field(None)  # проверка что нельзя позвать меньше нуля и больше 100
    extra_wishes: str|None = Field(None)
    user_id: int

    @model_validator(mode='after')
    def not_null_field(self) -> Self:
        if not any(self.__dict__.values()):
            raise ValueError("Fields are None")
        return self

class User_Tables_association_out(BaseModel):
    order_time: correct_date
    guest_amount: correct_guest_amount = Field(default=1)
    extra_wishes: str|None
    user_id: int
    table_id: int
    model_config = ConfigDict(from_attributes=True)

#без времени, никак не понять, какой стол освободить
#если известно время, то стол можно освободить зная, либо человека, который его занял(user_id)
#т.к можно посмотреть какой стол он занимал, либо номер стола
class User_Tables_association_info(BaseModel):
    order_time: correct_date
    table_id: int|None = Field(None)
    user_id: int|None = Field(None)

    @model_validator(mode='after')
    def not_null_field(self)-> Self:
        if not any(self.__dict__.values()):
            raise ValueError("Fields are None")
        return self

