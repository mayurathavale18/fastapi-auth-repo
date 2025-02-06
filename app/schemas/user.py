from pydantic import BaseModel, EmailStr
from typing import Optional, Dict
from datetime import date, timezone
from DateTime.DateTime import datetime as dt

class AuthsSchema(BaseModel):
    zerodha: Optional[Dict[str, str]] = {}
    dhan: Optional[Dict[str, str]] = {}
    deltaex: Optional[Dict[str, str]] = {}

class UserCreateSchema(BaseModel):
    first_name: str = ""
    last_name: str = ""
    user_email: str
    password: str = ""
    activated_on: Optional[date] = dt.now(timezone.utc)
    payment_date: Optional[date] = dt.now(timezone.utc)
    transaction_id: Optional[str] = ""
    auths: Optional[AuthsSchema] = {}

    class Config:
        from_attributes = True  # This allows the conversion from SQLAlchemy models to Pydantic models

class UserSignupSchema(BaseModel):
    first_name: Optional[str] = ""
    last_name: Optional[str] = ""
    user_email: str
    password: Optional[str] = ""
    activated_on: Optional[date] = dt.now(timezone.utc)
    payment_date: Optional[date] = dt.now(timezone.utc)
    transaction_id: Optional[str] = ""
    auths: Optional[AuthsSchema] = {}

    class Config:
        from_attributes = True  # This allows the conversion from SQLAlchemy models to Pydantic models


class UserSignUpSchema(BaseModel):
    user_email: str = ""
    user_phone: str = ""

    class Config:
        from_attributes: True


# class UserLoginSchema(BaseModel):
#     user_email: EmailStr
#     password: str
#     class Config:
#         from_attributes: True
