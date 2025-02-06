from sqlalchemy import Column, String, Date, JSON, DateTime
from sqlalchemy.orm import relationship
from app.utils.database import Base
from datetime import datetime as dt, timezone

class User(Base):
    __tablename__ = 'users'

    first_name = Column(String(255), default="")
    last_name = Column(String(255), default="")
    user_email = Column(String(255), primary_key=True)
    user_phone = Column(String(20))
    password = Column(String(255), default="")  # Add password field to store plain text passwords for now
    activated_on = Column(DateTime, default=lambda: dt.now(timezone.utc))  # Stores full timestamp
    payment_date = Column(Date, default=lambda: dt.now(timezone.utc).date()) 
    transaction_id = Column(String(100), default="")
    auths = Column(JSON, default=dict)  # Use JSON type for storing auths

    def __repr__(self):
        return f"<User(id={self.user_phone}, first_name={self.first_name}, last_name={self.last_name}, email={self.user_email})>"

