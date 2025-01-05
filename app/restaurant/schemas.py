from pydantic import BaseModel, Field, ConfigDict, BeforeValidator, model_validator
from app.restaurant.food_type import food_types
import datetime
from typing import Annotated
from typing_extensions import Self

from restaurant import LIMIT_OF_TABLE, LIMIT_OF_GUEST_ON_TABLE, DEFAULT_GUEST_QUANTITY


def is_valid_food_type(value) -> food_types:
    try:
        if isinstance(value, str):
            try:
                food_type = food_types(value)
                return food_type
            except:
                raise ValueError("string is not food type")
    except:
        raise ValueError("wrong type")


class Menu_In_Base_64_info(BaseModel):
    id: int|None = Field(None)
    food_name: None|str = Field(None)
    food_cost: None|float = Field(None, gt=0)
    food_description:None|str = Field(None)
    food_type: None|Annotated[food_types, BeforeValidator(is_valid_food_type)] = Field(None)
    food_image: None|str = Field(None)
    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode='after')
    def not_null_field(self) -> Self:
        if not (self.food_name or self.food_cost or self.food_description or self.food_type or self.food_image):
            raise ValueError("Three fields are None")
        return self

class Menu_In_Base_64(BaseModel):
    food_name: str
    food_cost: float = Field(gt=0)
    food_description: str
    food_type: Annotated[food_types, BeforeValidator(is_valid_food_type)]
    food_image: str # это base64 строка
    model_config = ConfigDict(from_attributes=True)

class Menu_In(BaseModel):
    food_name: str
    food_cost: float = Field(gt=0)
    food_description: str
    food_type: food_types
    food_photo_path: str
    model_config = ConfigDict(from_attributes=True)

class Menu_info(BaseModel):
    id: int|None = Field(None)
    food_name: str|None = Field(None)
    food_cost: float|None = Field(None, gt=0)
    food_description: str | None = Field(None)
    food_type: food_types|None = Field(None)
    food_photo_path: str|None = Field(None)

class Menu_out(Menu_In):
    id: int

def is_valid_date(value) -> datetime.datetime:
    try:
        if isinstance(value, str):
            print(type(value))
            value = datetime.datetime.fromisoformat(value)
            print(type(value), value)
    except Exception as e:
        print (e.__class__, e)
        raise ValueError("Дата и время не валидны(неверный формат)")
    if (datetime.datetime.now() > value) or (value > datetime.datetime.now() + datetime.timedelta(days=365*2)):
        raise ValueError("Дата и время не валидны(неверные значения)")
    return value

#обозначает конретный стол с его характеристиками
class Table_config(BaseModel):
    max_guest_amount: int = Field(LIMIT_OF_GUEST_ON_TABLE, gt=0)

class Table_config_out(BaseModel):
    id: int
    model_config = ConfigDict(from_attributes=True)

#обозначают детали бронирования стола
class Order_Table(BaseModel):
    order_time: Annotated[datetime.datetime, BeforeValidator(is_valid_date)] # проверка что нельзя заказать в прошлом
    guest_amount: int = Field(default=1,ge=1, le=100)  # проверка что нельзя позвать меньше нуля и больше 100
    extra_wishes: str|None = Field(None)

class Order_Table_in(Order_Table):
    user_id: int

class Order_Table_info(BaseModel):
    order_time: None|Annotated[datetime.datetime, BeforeValidator(is_valid_date)] = Field(None) # проверка что нельзя заказать в прошлом
    guest_amount: None|int = Field(None, ge=1, le=100)  # проверка что нельзя позвать меньше нуля и больше 100
    extra_wishes: str|None = Field(None)
    user_id: int

    @model_validator(mode='after')
    def not_null_field(self) -> Self:
        if not any(self.__dict__.values()):
            raise ValueError("Fields are None")
        return self

class User_Tables_association_out(BaseModel):
    order_time: datetime.datetime
    guest_amount: int = Field(default=1, ge=1)
    extra_wishes: str|None
    is_free: bool = Field(default=True)
    user_id: int
    table_id: int
    model_config = ConfigDict(from_attributes=True)

#без времени, никак не понять, какой стол освободить
#если известно время, то стол можно освободить зная, либо человека, который его занял(user_id)
#т.к можно посмотреть какой стол он занимал, либо номер стола
class User_Tables_association_info(BaseModel):
    order_time: datetime.datetime
    table_id: int|None = Field(None)
    user_id: int|None = Field(None)
    is_free: bool = Field(False)

    @model_validator(mode='after')
    def not_null_field(self)-> Self:
        if not any(self.__dict__.values()):
            raise ValueError("Fields are None")
        return self

