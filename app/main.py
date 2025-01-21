from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes import user
from app.utils.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()  # ✅ Initialize the database at startup
    yield  # Let the app run
    print("🔴 Shutting down...")  # (Optional) Cleanup logic can be placed here

app = FastAPI()

app.include_router(user.router, prefix="/user", tags=["User"])

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI Authentication App"}

@app.on_event("startup")
def startup_event():
    init_db()