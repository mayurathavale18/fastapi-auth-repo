from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.models.user import User  # SQLAlchemy model
from app.schemas.user import UserCreateSchema, UserSignUpSchema  # Pydantic schema
from app.cruds.user import get_db
from app.cruds.user import get_user_by_email
from app.schemas.orders import OrderSchema
import os
import httpx
import json

router = APIRouter()

@router.post('/')
async def place_orders(order: OrderSchema):
    base_url = os.getenv("BASE_URL")
    if not base_url:
        return {"error": "BASE_URL is not set"}

    url = f"{base_url}/orders"
    
    data = order.dict()
    print(json.dumps(data))
    

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "access-token": os.getenv("DHAN_ACCESS_TOKEN"),  # Ensure non-null value
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, data=data)
        message = response.json()
    return {
        "message" : message
    }
    