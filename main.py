from app.routers import item_router, user_router
from fastapi import FastAPI

app = FastAPI()

app.include_router(item_router)
app.include_router(user_router)