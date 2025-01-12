from fastapi import HTTPException, status
from typing import Annotated
from typing_extensions import Self
from pydantic import (Field,
                      BeforeValidator,
                      AfterValidator,
                      model_validator,
                      BaseModel,
                      ConfigDict,
                      EmailStr
                      )
from app.authorization.roles import Roles
import app.authorization as auth


def is_valid_name(value) -> str:
    if value:
        if len(value)>=auth.min_name_length:
            return value
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=auth.TOO_SHORT_NAME)
    else:
        return None

def is_valid_role(value)->Roles:
    if value:
        if isinstance(value, str):
            try:
                return Roles(value)
            except:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=auth.INVALID_ROLE_FORMAT)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=auth.INVALID_ROLE_FORMAT)
    else:
        return None

def is_correct_password(value)->str:
    if value:
        if isinstance(value, str):
            if len(value)>=auth.min_password_length:
                return value
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=auth.TOO_SHORT_PASSWORD)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=auth.INVALID_PASSWORD_FORMAT)
    else:
        return None

correct_role = Annotated[Roles, BeforeValidator(is_valid_role)]
correct_name = Annotated[str, AfterValidator(is_valid_name)]
correct_password = Annotated[str, BeforeValidator(is_correct_password)]

class User(BaseModel):
    user_name: correct_name
    email_address: EmailStr
    model_config = ConfigDict(from_attributes=True)

class User_add_schema(User):
    hashed_password: bytes
    user_role: correct_role

class User_ORM_(User):
    user_role: Roles
    id: int


class User_API_in(User):
    password: correct_password
    user_role: correct_role = Field(Roles.AUTHORIZED_USER)

class User_ORM_out(User_ORM_):
    hashed_password: bytes

class User_info(BaseModel):
    id: None|int = Field(None)
    user_name: correct_name|None = Field(None)
    password: correct_password|None = Field(None)
    email_address: EmailStr|None = Field(None)
    user_role: correct_role|None = Field(None)

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

class User_creadential_schema(BaseModel):
    id: int
    password: str = Field(None, min_length=auth.min_password_length)