from fastapi import (
     APIRouter,
     Response,
     HTTPException,
     status,
     Request
     )
from fastapi.params import Depends

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

from app.authorization.execptions import (
    User_doesnt_exist,
    Is_existing_user
    )
from app.authorization.schemas import (
    User_API_in,
    User_ORM_,
    User,
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
async def register_user(user: User_API_in) -> dict:
    try:
        registered_user = await rep.get_user_by_email_and_name(user)
        print(registered_user, "<- is user")
        if registered_user:
            raise HTTPException(
                                status_code=status.HTTP_403_FORBIDDEN
                                ,detail='this user already exist'
                                )
        await rep.add_new_user(user)
        return {
            "message": "you successfully registered"
        }
    except Is_existing_user:
        print("registration is invalid")
        raise HTTPException(
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                            ,detail='this user already exist'
                            )
    except Exception as e:
        print(e.__class__, e)

@router.post('/login/', status_code=status.HTTP_202_ACCEPTED, response_model=User_ORM_)
async def login_user(response: Response,
                     user: User_ORM_ = Depends(authenticate_user)
                     ):
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
            , detail='wrong password'
        )
    except User_doesnt_exist:
        raise HTTPException(
            status_code=status.HTTP_403_INTERNAL_SERVER_ERROR
            , detail='user doesnt exist'
        )

@router.post('/logout/', status_code=status.HTTP_200_OK)
async def logout_user(response: Response, user: User_ORM_ = Depends(get_current_user)) -> dict:
    try:
        response.delete_cookie(key=USER_ACCESS_TOKEN)
        response.delete_cookie(key=USER_REFRESH_TOKEN)
        await rep.delete_refresh_token_by_property(user_id=user.id)
        return {
            'message': "you successfully logout"
            }
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            ,detail="server error"
        )

@router.post('/refresh/', status_code=status.HTTP_200_OK, response_model=User_ORM_)
async def auth_refresh_jwt(response: Response, user: User_ORM_ = Depends(authenticate_tokens)):
    try:
        print("start refresh jwt")
        new_access_token = create_access_token(user)
        new_refresh_token = await create_refresh_token(user)
        response.set_cookie(key = USER_ACCESS_TOKEN, value=new_access_token)
        response.set_cookie(key = USER_REFRESH_TOKEN, value=new_refresh_token)

        return user
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='something bad happens'
        )

@router.put('/change_user/', status_code=status.HTTP_200_OK, dependencies=[Depends(get_admin)])
async def change_user(
        user_info: User_info,
        new_data: User_info
)->dict:
    for k,v in user_info.model_dump().items():
        print(k , v)

    for k,v in new_data.model_dump().items():
        print(k, v)
    try:
        await rep.change_user(user_info,
                              new_data
                              )
        return {
            "message":"change has complited"
        }
    except Exception as e:
        print(e.__class__, e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="server error"
        )

@router.delete('/delete_user/', status_code=status.HTTP_200_OK, dependencies=[Depends(get_admin)])
async def delete_user(
        user_info: User_info
):
    try:
        await rep.delete_user(user_info)
    except Exception as e:
        print(e.__class__, e)



