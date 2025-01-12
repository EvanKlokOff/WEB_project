from fastapi import FastAPI, HTTPException, Request
from app.pages.utils import send_page_with_context_and_status_code
from app.utils import lifespan_
from app.authorization.router import router as auth_router
from app.pages.router import router as page_router
import uvicorn
from fastapi.staticfiles import StaticFiles
from app.restaurant.router import router as restaurant_router
from app.send_emails.router import router as email_router
from fastapi import status

app = FastAPI(lifespan=lifespan_)

app.mount("/static", StaticFiles(directory='/home/ivanklokov/study/WEB/project/pythonProject/app/static'),'static')

app.include_router(restaurant_router)
app.include_router(auth_router)
app.include_router(page_router)
#app.include_router(email_router)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):

    return send_page_with_context_and_status_code(
        "error_page/error_page.html",
        request,
        {"error_message": exc.detail},
        exc.status_code
    )

@app.exception_handler(ValueError)
async def http_exception_handler(request: Request, exc: ValueError):

    return send_page_with_context_and_status_code(
        "error_page/error_page.html",
        request,
        {"error_message": exc.args[0]},
        status_code=status.HTTP_403_FORBIDDEN
    )
if __name__ == '__main__':
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )