from fastapi import FastAPI
from app.utils import lifespan_
from app.authorization.router import router as auth_router
from app.pages.router import router as page_router
import uvicorn
from fastapi.staticfiles import StaticFiles
from app.restaurant.router import router as restaurant_router

app = FastAPI(lifespan=lifespan_)

app.mount("/static", StaticFiles(directory='/home/ivanklokov/study/WEB/project/pythonProject/app/static'),'static')

app.include_router(restaurant_router)
app.include_router(auth_router)
app.include_router(page_router)

if __name__ == '__main__':
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )