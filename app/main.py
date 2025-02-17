import os
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
import asyncio
import httpx
from contextlib import asynccontextmanager
from app.routes import user, instruments, holdings
from app.utils.database import init_db
from app.utils.cron import scheduler  # Import the cron job
import pandas as pd
from app.middleware.headers import AddHeadersMiddleware
from app.utils.websocket import DhanWebSocketClient


ws_client = DhanWebSocketClient()  # Initialize WebSocket Client

COMPACT_FILE_PATH = os.getenv("COMPACT_FILE_PATH")
DETAILED_FILE_PATH = os.getenv("DETAILED_FILE_PATH")

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    task = asyncio.create_task(cyclic_func())

    # Starting the scheduler only if it's not already running
    if not scheduler.running:
        scheduler.start()

    app.state.holdings = {}
    
    if os.path.exists(COMPACT_FILE_PATH):
        app.state.compact_df = pd.read_csv(COMPACT_FILE_PATH, keep_default_na=False, low_memory=False)
    else:
        app.state.compact_df = None

    if os.path.exists(DETAILED_FILE_PATH):
        app.state.detailed_df = pd.read_csv(DETAILED_FILE_PATH, keep_default_na=False, low_memory=False)
    else:
        app.state.detailed_df = None

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

#MiddleWaress
app.add_middleware(AddHeadersMiddleware)

#Routes
app.include_router(user.router, prefix="/user", tags=["User"])
app.include_router(instruments.router, prefix="/instruments", tags=["Data"])
app.include_router(holdings.router, prefix="/holdings", tags=["holdings"])

@app.get("/")
def root():
    return {"FastAPI with Dhan WebSocket Running 🚀"}

