from fastapi import APIRouter, Request, status
from app.authorization.utils import get_admin
from app.pages import utils

router = APIRouter(
    tags = ['frontend']
)

@router.get("/", tags=["root"])
async def root(request: Request):
    try:
        user = get_admin()
        return utils.send_page()
    except:
        return utils.send_page("restaurant/restaurant_main_page.html", request)