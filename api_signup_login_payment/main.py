from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from database import engine, Base
from routers import users, payment

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(payment.router)
