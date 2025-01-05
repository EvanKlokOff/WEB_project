from typing import Annotated
from typing_extensions import Self
from pydantic import (Field,
                      BeforeValidator,
                      model_validator,
                      BaseModel,
                      ConfigDict
                      )
from app.authorization.roles import Roles

class User(BaseModel):
    user_name: str = Field(min_length=2)
    email_address: str = Field(min_length=5)
    model_config = ConfigDict(from_attributes=True)

class User_ORM_(User):
    user_role: Roles
    id: int

def is_valid_role(value)->Roles:
    try:
        if isinstance(value, str):
            try:
                return Roles(value)
            except:
                raise ValueError("string is not Role")
    except Exception as e:
        print(e.__class__, e)

class User_API_in(User):
    password: str
    user_role: Annotated[Roles, BeforeValidator(is_valid_role)] = Field(Roles.AUTHORIZED_USER)

class User_ORM_out(User_ORM_):
    hashed_password: bytes

class User_info(BaseModel):
    id: None|int = Field(None)
    user_name: str|None = Field(None, min_length=2)
    password: str|None = Field(None)
    email_address: str|None = Field(None, min_length=5)
    user_role: str|None = Field(None)

    @model_validator(mode='after')
    def not_null_field(self) -> Self:
        if not any(self.__dict__.values()):
            raise ValueError("Fields are None")
        return self

class Refresh_token(BaseModel):
    refresh_token: str|bytes
    model_config = ConfigDict(from_attributes=True)

class JWT_tokens(BaseModel):
    access_token: str|bytes
    refresh_token: str|bytes
