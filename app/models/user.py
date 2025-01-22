# from pydantic import BaseModel, EmailStr
# from typing import Optional, Dict
# from datetime import date

# class AuthSchema(BaseModel):
#     client_id: str
#     api_key: Optional[str] = None
#     api_secret: Optional[str] = None
#     access_token: str

# class UserSchema(BaseModel):
#     first_name: str
#     last_name: str
#     user_email: EmailStr
#     user_phone: str
#     activated_on: Optional[date] = None
#     payment_date: Optional[date] = None
#     transaction_id: Optional[str] = None
#     auths: Dict[str, AuthSchema]

#     class Config:
#         orm_mode = True


from sqlalchemy import Column, String, Date, JSON
from sqlalchemy.orm import relationship
from app.utils.database import Base

class User(Base):
    __tablename__ = 'users'

    first_name = Column(String(255))
    last_name = Column(String(255))
    user_email = Column(String(255), primary_key=True)
    user_phone = Column(String(20))
    password = Column(String(255))  # Add password field to store plain text passwords for now
    activated_on = Column(Date, nullable=True)
    payment_date = Column(Date, nullable=True)
    transaction_id = Column(String(100), nullable=True)
    auths = Column(JSON, nullable=True)  # Use JSON type for storing auths

    def __repr__(self):
        return f"<User(id={self.user_phone}, first_name={self.first_name}, last_name={self.last_name}, email={self.user_email})>"

