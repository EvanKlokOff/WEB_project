from fastapi import (
     APIRouter,
     Response,
     HTTPException,
     status,
     Request
     )
from fastapi.params import Depends
import app
from app.authorization import USER_ACCESS_TOKEN, USER_REFRESH_TOKEN

from app.authorization.utils import (
     get_admin,
     get_current_user,
     authenticate_user,
     create_access_token,
     create_refresh_token,
     authenticate_tokens
     )

import app.authorization.repository as rep

from app.authorization.schemas import (
    User_API_in,
    User_ORM_,
    User_info
    )
from pages.utils import send_page

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

@router.get("/{page_name}")
async def show_login_page(page_name:str, requset: Request):
    return send_page(f"/auth/{page_name}", requset)

@router.post('/register/', status_code=status.HTTP_201_CREATED)
async def register_user(user: User_API_in):
    try:
        registered_user = await rep.get_user_by_email_and_name(user)
        print(registered_user, "<- is user")
        if registered_user:
            raise HTTPException(
                                status_code=status.HTTP_403_FORBIDDEN
                                ,detail=app.this_user_already_exist
                                )
        await rep.add_new_user(user)
    except Exception as e:
        raise e

@router.post('/login/', status_code=status.HTTP_202_ACCEPTED)
async def login_user(response: Response, user: User_ORM_ = Depends(authenticate_user)):
    #удаление предыдущего токена
    response.delete_cookie(key=USER_ACCESS_TOKEN)
    response.delete_cookie(key=USER_REFRESH_TOKEN)
    await rep.delete_refresh_token_by_property(user_id=user.id)
    try:
        access_token = create_access_token(user)
        refresh_token = await create_refresh_token(user)

        response.set_cookie(key=USER_ACCESS_TOKEN,
                            value=access_token
                            )

        response.set_cookie(key=USER_REFRESH_TOKEN,
                            value=refresh_token,
                            httponly=True
                            )
        return user
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_403_INTERNAL_SERVER_ERROR
            , detail=app.wrong_password_or_login
        )
    except User_doesnt_exist:
        raise HTTPException(
            status_code=status.HTTP_403_INTERNAL_SERVER_ERROR
            , detail=app.wrong_password_or_login
        )

@router.post('/logout/', status_code=status.HTTP_200_OK)
async def logout_user(response: Response, user: User_ORM_ = Depends(get_current_user)):
    try:
        response.delete_cookie(key=USER_ACCESS_TOKEN)
        response.delete_cookie(key=USER_REFRESH_TOKEN)
        await rep.delete_refresh_token_by_property(user_id=user.id)
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            ,detail=app.server_error
        )

@router.post('/refresh/', status_code=status.HTTP_200_OK)
async def auth_refresh_jwt(response: Response, user: User_ORM_ = Depends(authenticate_tokens)):
    try:
        print("start refresh jwt")
        new_access_token = create_access_token(user)
        new_refresh_token = await create_refresh_token(user)
        response.set_cookie(key = USER_ACCESS_TOKEN, value=new_access_token)
        response.set_cookie(key = USER_REFRESH_TOKEN, value=new_refresh_token)
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=app.server_error
        )

@router.put('/change_user/', status_code=status.HTTP_200_OK, dependencies=[Depends(get_admin)])
async def change_user(user_info: User_info, new_data: User_info):
    try:
        await rep.change_user(user_info,
                              new_data
                              )
    except Exception as e:
        print(e.__class__, e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=app.server_error
        )

@router.delete('/delete_user/', status_code=status.HTTP_200_OK, dependencies=[Depends(get_admin)])
async def delete_user(
        user_info: User_info
):
    try:
        await rep.delete_user(user_info)
    except Exception as e:
        print(e.__class__, e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=app.server_error
        )



