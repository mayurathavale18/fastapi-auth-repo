from pydantic import BaseModel, EmailStr
from typing import Optional, Dict
from datetime import date

class AuthsSchema(BaseModel):
    zerodha: Optional[Dict[str, str]] = None
    dhan: Optional[Dict[str, str]] = None
    deltaex: Optional[Dict[str, str]] = None

class UserCreateSchema(BaseModel):
    first_name: str
    last_name: str
    user_email: str
    user_phone: str
    password: str
    activated_on: Optional[date] = None
    payment_date: Optional[date] = None
    transaction_id: Optional[str] = None
    auths: Optional[AuthsSchema] = None

    class Config:
        orm_mode = True  # This allows the conversion from SQLAlchemy models to Pydantic models

class UserSignUpSchema(BaseModel):
    user_email: str
    user_phone: str

    class Config:
        orm_mode: True


class UserLoginSchema(BaseModel):
    user_email: EmailStr
    password: str
    class Config:
        orm_mode: True
