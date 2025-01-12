from fastapi import (
    status,
    HTTPException,
    Request
)
from fastapi.params import Depends
import app
from app.authorization import USER_ACCESS_TOKEN
from app.authorization.config import auth_jwt, jwt_parametres
from datetime import (
    datetime,
    timedelta,
    timezone
)

from app.authorization.roles import Roles
from app.authorization.schemas import (
    User_API_in,
    User_ORM_
)

import app.authorization.repository as rep
import bcrypt
import jwt

from authorization import USER_REFRESH_TOKEN
from app.authorization.schemas import (JWT_tokens,
                                       User_creadential_schema)
from functools import singledispatch

JWT_TOKEN_TYPE="type"
JWT_ACCESS_TOKEN="access"
JWT_REFRESH_TOKEN="refresh"

def encode_jwt(
    payload:dict,
    private_key:str = auth_jwt.jwt_private_path.read_text(),
    algorithm:str = auth_jwt.algorithm,
    expire_time: timedelta = jwt_parametres.jwt_token_default_expire_time
) -> str:
    now = datetime.now(timezone.utc)
    payload.update(
        exp = now + expire_time,
        iat = now
    )
    encoded = jwt.encode(
        payload=payload,
        key=private_key,
        algorithm=algorithm
    )
    return encoded

def decode_jwt(
    token: str | bytes,
    public_key: str = auth_jwt.jwt_open_path.read_text(),
    algorithm:str = auth_jwt.algorithm,
) -> dict[str,str]:
    decoded = jwt.decode(
        jwt=token,
        key=public_key,
        algorithms=[algorithm]
    )
    return decoded

def create_jwt_token(token_type:str,
                     token_data:dict,
                     expire_time: timedelta)->str|bytes:
    jwt_payload = {JWT_TOKEN_TYPE: token_type}
    jwt_payload.update(token_data)
    return encode_jwt(jwt_payload, expire_time=expire_time)

def create_access_token(user: User_ORM_) -> str|bytes:
    jwt_payload = {
        "sub": str(user.id)
    }

    return create_jwt_token(JWT_ACCESS_TOKEN,
                            jwt_payload,
                            expire_time=jwt_parametres.jwt_access_token_expire_time
                            )

async def create_refresh_token(user: User_ORM_)-> str|bytes|None:
    try:
        jwt_payload = {
            "sub": str(user.id)
        }
        refresh_token = create_jwt_token(JWT_REFRESH_TOKEN,
                                jwt_payload,
                                expire_time=jwt_parametres.jwt_refresh_token_expire_time
                                )
        await rep.delete_refresh_token_by_property(user_id=user.id)
        await rep.add_refresh_token_by(refresh_token)
        return refresh_token
    except Exception as e:
        print(e.__class__, e)
        return None

def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)

def validate_password(password: str,hashed_password: bytes) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password
    )

def get_tokens(request: Request) -> JWT_tokens:
    access_token = request.cookies.get(USER_ACCESS_TOKEN)
    refresh_token = request.cookies.get(USER_REFRESH_TOKEN)
    if access_token and refresh_token:
        return JWT_tokens(access_token=access_token, refresh_token=refresh_token)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail=app.token_is_invalid
    )

async def get_current_user(tokens: JWT_tokens = Depends(get_tokens)) -> User_ORM_:
    try:
        payload = decode_jwt(tokens.access_token)
    except jwt.exceptions.ExpiredSignatureError:
        return await authenticate_tokens(tokens)
    except Exception as e:
        print(e.__class__, e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=app.token_is_invalid)

    user_id = int(payload.get("sub"))
    user = await rep.get_user_by_property(id = user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=app.token_is_invalid)

    return user

async def authenticate_tokens(tokens:JWT_tokens = Depends(get_tokens)) -> User_ORM_:
    try:
        payload = decode_jwt(tokens.refresh_token)
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=app.token_is_invalid)

    user_id = int(payload.get("sub"))
    token = await rep.get_refresh_token_by_property(user_id=user_id)
    if (not token) or (not user_id) or (token.refresh_token != tokens.refresh_token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=app.token_is_invalid)

    return await rep.get_user_by_property(id=user_id)

async def get_admin(user: User_ORM_ = Depends(get_current_user)) -> User_ORM_:
    try:
        if user.user_role == Roles.ADMIN:
            return user
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=app.u_have_not_enough_rights)
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=app.token_is_invalid)


async def authenticate_user(user: User_API_in) -> None | User_ORM_:
    print("первый метод")
    user_ = await rep.get_user_by_property(user_name = user.user_name,
                                           email_address = user.email_address)
    if user_:
        if validate_password(user.password, user_.hashed_password):
            return User_ORM_(**user_.model_dump())
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=app.wrong_password_or_login
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=app.wrong_password_or_login
        )

async def authenticate_user_by_id(user: User_creadential_schema) -> None | User_ORM_:
    print("Второй метод")
    print(user)
    try:
        user_ = await rep.get_user_by_property(id = user.id)
    except Exception as e:
        print("ошибка при получении пользователя с бд")
        raise e
    if user_:
        if validate_password(user.password, user_.hashed_password):
            return User_ORM_(**user_.model_dump())
        else:
            print("пароль не совпал")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=app.wrong_password_or_login
            )
    else:
        print("пользователя с таким id нет")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=app.wrong_password_or_login
        )