from fastapi import APIRouter, Request, Depends, HTTPException, status

import DBmanager
import app.restaurant.repository as rest_rep
import app.authorization.repository as auth_rep
from app.pages.utils import send_page_with_context, send_page
from app.authorization.utils import get_current_user, get_admin, get_tokens
from app.authorization.schemas import User_ORM_
from app.restaurant.schemas import (
                                    Menu_In_Base_64,
                                    Menu_In,
                                    Menu_info,
                                    Menu_In_Base_64_info,
                                    User_Tables_association_info)
from app.restaurant.utils import store_image_in,delete_image_in
from app.restaurant.schemas import Order_Table, Order_Table_in
import app.DBmanager
from app.restaurant.models import Menu


router = APIRouter(prefix="/restaurant",
                   tags=["Restaurant"]
                   )

#
@router.get("/restaurant_main_page.html", tags=["root"])
async def show_main_page(request: Request):
    try:
        tokens = get_tokens(request)
        user = await get_current_user(tokens)
        admin = await get_admin(user)
        context=dict
        if admin:
            context={"role":"ADMIN"}
        elif user:
            context = {"role": "AUTHORIZED_USER"}
        return send_page_with_context("restaurant/restaurant_main_page.html", request, context)
    except Exception as e:
        print(e.__class__, e)
        raise e


#для всех пользователей
@router.get('/menu.html', status_code=status.HTTP_200_OK)
async def get_all_menu_html(request: Request,
                            menus: [dict] = Depends(rest_rep.get_all_menus),
                            ):
    page_context = {"menus": menus}
    return send_page_with_context("restaurant/menu.html", request, page_context)

@router.post('/add_new_menu', status_code=status.HTTP_202_ACCEPTED, dependencies=[Depends(get_admin)])
async def add_new_menu(menu: Menu_In_Base_64):
    try:
        file_path = store_image_in(menu.food_image, menu.food_name)
        dict_to_add = menu.model_dump()
        del dict_to_add["food_image"]
        menu_to_add = Menu_In(**dict_to_add, food_photo_path=file_path)
        await DBmanager.add_thing(menu_to_add, Menu)
    except Exception as e:
        print(e.__class__, e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="something go bad")

@router.delete('/delete_menu', status_code=status.HTTP_202_ACCEPTED, dependencies=[Depends(get_admin)])
async def delete_menu(menu_info: Menu_info):
    try:
        delete_image_in(menu_info.food_photo_path)
        await DBmanager.delete_thing(menu_info, Menu)
    except Exception as e:
        print(e.__class__, e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="something go bad")

@router.put('/change_menu', status_code=status.HTTP_202_ACCEPTED, dependencies=[Depends(get_admin)])
async def change_menu(menu_info:Menu_info,
                      change_menu_info: Menu_In_Base_64_info
                      ):
    try:
        if change_menu_info.food_image:
            delete_image_in(menu_info.food_photo_path)
            if change_menu_info.food_name:
                file_path=store_image_in(change_menu_info.food_image, change_menu_info.food_name)
            else:
                file_path=store_image_in(change_menu_info.food_image, menu_info.food_name)
            change_menu_info_ = Menu_info(id=change_menu_info.id,
                                          food_name=change_menu_info.food_name,
                                          food_cost=change_menu_info.food_cost,
                                          food_description=change_menu_info.food_description,
                                          food_type=change_menu_info.food_type,
                                          food_photo_path=file_path
                                          )
        await rest_rep.change_food_in_menu(menu_info, change_menu_info_)
    except Exception as e:
        print(e.__class__, e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="something go bad")


#для авторизованных пользователей
@router.get("/book_table.html", status_code=status.HTTP_200_OK, dependencies=[Depends(get_current_user)])
async def show_book_page(request: Request):
    try:
        return send_page('restaurant/book_table.html', request)
    except HTTPException as http_e:
        print(http_e.__class__, http_e, http_e.detail, http_e.args)
    except Exception as e:
        print(e.__class__, e)

#метод для админа
@router.get("/admin_panel.html", dependencies=[Depends(get_admin)])
async def get_admin_panel(request: Request,
                          menus: [dict] = Depends(rest_rep.get_all_menus),
                          users: [dict] = Depends(auth_rep.get_all_users),
                          tables: [dict] = Depends(rest_rep.get_all_tables)
                          ):
    context = {"menus": menus,
               "users": users,
               "tables": tables
               }
    return send_page_with_context("restaurant/admin_panel.html", request, context)

#метод для авторизованных пользователей
@router.post('/book_table/', status_code=status.HTTP_202_ACCEPTED)
async def book_table(booking_info: Order_Table, user:User_ORM_=Depends(get_current_user)):
    try:
        for k, v in booking_info.model_dump().items():
            print(k, v)
        await rest_rep.book_table(Order_Table_in(**booking_info.model_dump(), user_id=user.id))
    except Exception as e:
        print(e.__class__, e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="something_go_bad_in_booking")

@router.delete('/free_table/', dependencies=[Depends(get_admin)])
async def free_table_by(order_info: User_Tables_association_info):
    try:
        for k, v in order_info.model_dump().items():
            print(k, v)

        await rest_rep.free_table(order_info)
    except Exception as e:
        print(e.__class__, e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="something_go_bad")

@router.put('/change_table/', dependencies=[Depends(get_admin)])
async def change_table(order_info:User_Tables_association_info,
                       booking_info: Order_Table_in):
    try:
        for k, v in order_info.model_dump().items():
            print(k,v)
        for k, v in booking_info.model_dump().items():
            print(k, v)
        await rest_rep.change_table_booking(order_info, booking_info)
    except Exception as e:
        print(e.__class__, e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="something_go_bad")