from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict
from datetime import datetime as dt, date, timezone
# from DateTime.DateTime import datetime as dt

class AuthsSchema(BaseModel):
    zerodha: Optional[Dict[str, str]] = {}
    dhan: Optional[Dict[str, str]] = {}
    deltaex: Optional[Dict[str, str]] = {}

class UserCreateSchema(BaseModel):
    first_name: Optional[str] = ""
    last_name: Optional[str] = ""
    user_email: str
    password: Optional[str] = ""
    activated_on: dt = Field(default_factory=lambda: dt.now(timezone.utc))
    payment_date: date = Field(default_factory=lambda: dt.now(timezone.utc).date())
    transaction_id: Optional[str] = ""
    auths: AuthsSchema

    class Config:
        from_attributes = True  # This allows the conversion from SQLAlchemy models to Pydantic models

class UserSignupSchema(BaseModel):
    first_name: Optional[str] = ""
    last_name: Optional[str] = ""
    user_email: str
    password: Optional[str] = ""
    activated_on: dt = Field(default_factory=lambda: dt.now(timezone.utc))
    payment_date: date = Field(default_factory=lambda: dt.now(timezone.utc).date())
    transaction_id: Optional[str] = ""
    auths: AuthsSchema

    class Config:
        from_attributes = True  # This allows the conversion from SQLAlchemy models to Pydantic models


class UserSignUpSchema(BaseModel):
    user_email: str = ""
    user_phone: str = ""

    class Config:
        from_attributes: True

class UserHoldingSchema(BaseModel):
    user_email: str
    user_access_token: str  # 🔥 Required for API calls
    security_id: str
    trading_symbol: str
    stop_loss: float
    created_at: dt = Field(default_factory=lambda: dt.now(timezone.utc))
    updated_at: dt = Field(default_factory=lambda: dt.now(timezone.utc))
    class Config:
        from_attributes = True

# class UserLoginSchema(BaseModel):
#     user_email: EmailStr
#     password: str
#     class Config:
#         from_attributes: True
