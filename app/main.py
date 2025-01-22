from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes import user
from app.utils.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield  # Let the app run

app = FastAPI(lifespan=lifespan)

app.include_router(user.router, prefix="/user", tags=["User"])

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI Authentication App"}

