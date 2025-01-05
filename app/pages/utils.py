from fastapi import Request
from typing import Any
from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory="/home/ivanklokov/study/WEB/project/pythonProject/app/templates")

def send_page(page_name:str, request: Request) -> Any:
    try:
        print(page_name)
        return templates.TemplateResponse(name=page_name, context={'request': request})
    except Exception as e:
        print(e.__class__, e)
        raise e

def send_page_with_context(page_name:str,
                           request: Request,
                           page_context:dict) -> Any:
    try:
        contex={'request':request}
        contex.update(**page_context)

        return templates.TemplateResponse(name=page_name,
                                          context=contex)
    except Exception as e:
        print(e.__class__, e)
        raise e
def send_page_with_context_and_status_code(page_name,
                                           request:Request,
                                           page_context:dict,
                                           status_code:int
                                           ):
    try:
        contex = {'request': request}
        contex.update(**page_context)
        return templates.TemplateResponse(
            page_name,
            context=contex,
            status_code=status_code
        )
    except Exception as e:
        print(e.__class__, e)
        raise e