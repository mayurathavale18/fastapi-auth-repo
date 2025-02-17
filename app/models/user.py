from sqlalchemy import Column, String, Date, JSON, DateTime, Float, ForeignKey, Integer, func
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

    #Adding user_holdings model relation:
    holdings = relationship("UserHoldings", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.user_phone}, first_name={self.first_name}, last_name={self.last_name}, email={self.user_email})>"


class UserHoldings(Base):
    __tablename__ = 'user_holdings'

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String(255), ForeignKey("users.user_email", ondelete="CASCADE"))
    user_access_token = Column(String, nullable=False)  # 🔥 Required for Dhan API
    security_id = Column(String(20), nullable=False)
    trading_symbol = Column(String(50), nullable=False)
    stop_loss = Column(Float, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="holdings")