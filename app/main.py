from fastapi import FastAPI
import asyncio
import httpx
from contextlib import asynccontextmanager
from app.routes import user
from app.utils.database import init_db
from app.routes import instruments
from app.utils.cron import scheduler  # Import the cron job

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    task = asyncio.create_task(cyclic_func())

    # Starting the scheduler only if it's not already running
    if not scheduler.running:
        scheduler.start()

    yield  # Let the app run

    task.cancel()

async def cyclic_func():
    while True:
        try:
            async with httpx.AsyncClient() as client:
                await client.get('https://fastapi-auth-repo.onrender.com/')
                await asyncio.sleep(885)  # 15 minutes
        except Exception as e:
            print(f"Error in cyclic_func: {e}")
            await asyncio.sleep(30)  # wait a minute before retrying

app = FastAPI(lifespan=lifespan)

app.include_router(user.router, prefix="/user", tags=["User"])
app.include_router(instruments.router)

@app.get("/")
def root():
    return {"message": "stay awake request successfull!"}

