from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.user import UserHoldings
from app.schemas.user import UserHoldingSchema
from app.cruds.user import get_db
from datetime import datetime as dt, date, timezone

router = APIRouter()

@router.post("/")
def add_or_update_holding(holding: UserHoldingSchema, db: Session = Depends(get_db)):
    existing_holding = db.query(UserHoldings).filter(
        UserHoldings.user_email == holding.user_email,
        UserHoldings.security_id == holding.security_id
    ).first()

    if existing_holding:
        existing_holding.stop_loss = holding.stop_loss
        existing_holding.user_access_token = holding.user_access_token  # 🔥 Update token
        existing_holding.updated_at = dt.now(timezone.utc)
        db.commit()
        db.refresh(existing_holding)
        return {"message": "Stop Loss updated!", "holding": existing_holding}

    new_holding = UserHoldings(**holding.dict())
    db.add(new_holding)
    db.commit()
    db.refresh(new_holding)
    return {"message": "New Holding added!", "holding": new_holding}

@router.get("/{security_id}")
def get_users_for_stock(security_id: str, db: Session = Depends(get_db)):
    holdings = db.query(UserHoldings).filter(UserHoldings.security_id == security_id).all()
    if not holdings:
        raise HTTPException(status_code=404, detail="No users found for this stock.")

    stock_users = [{holding.user_access_token: holding.stop_loss} for holding in holdings]
    return {security_id: stock_users}
