from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.user import User  # SQLAlchemy model
from app.schemas.user import UserCreateSchema, UserSignUpSchema  # Pydantic schema
from app.cruds.user import create_user, get_db
from app.utils.dependencies import get_current_user
from app.utils.auth import create_access_token
from app.cruds.user import get_user_by_email

router = APIRouter()

# Static OTP endpoint
@router.post("/signup")
def signup(user: UserSignUpSchema, db: Session = Depends(get_db)):
    # print(db.)
     # Check if the user already exists
    existing_user = db.query(User).filter(User.user_email == user.user_email).first()
    print("Existing user found : ", existing_user)
    if existing_user:
        return {
            "user": existing_user, 
            "otp": "123456", 
            "status": "User Already Created!" }

    # Create a minimal user record with default values
    new_user = User(
        user_email=user.user_email,
        user_phone=user.user_phone
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # # Generate access token
    # access_token_expires = timedelta(hours=1)
    # access_token = create_access_token(
    #     data={"sub": new_user.user_email, "user_id": new_user.user_phone}, expires_delta=access_token_expires
    # )

    return {
        "user": new_user,
        "otp": "123456",
        "status": "New User Created!"
    }

# Create user in MySQL
@router.post("/create_user")
def create_new_user(user: UserCreateSchema, db: Session = Depends(get_db)):
    try:
        created_user = create_user(db=db, user=user)
        return {"message": "User created successfully", "user": created_user}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/update_user")
def update_user(user: UserCreateSchema, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # Check if the user already exists in the database
    db_user = get_user_by_email(db=db, email=user.user_email)
    auths_dict = user.auths.model_dump_json() if user.auths else None
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update user details
    db_user.first_name = user.first_name
    db_user.last_name = user.last_name
    db_user.activated_on = user.activated_on
    db_user.password = user.password
    db_user.payment_date = user.payment_date
    db_user.transaction_id = user.transaction_id
    db_user.auths = auths_dict

    db.commit()
    db.refresh(db_user)

    # Create new auth token for the user after updating
    access_token_expires = timedelta(hours=1)
    access_token = create_access_token(
        data={"sub": user.user_email, "user_id": db_user.user_phone}, expires_delta=access_token_expires
    )

    return {"message": "User updated successfully", "access_token": access_token}
    
# @router.post("/login")
# async def login(user: UserLoginSchema, db: Session = Depends(get_db)):
#     user_in_db = get_user_by_email(db=db, email=user.user_email)
    
#     if not user_in_db or user_in_db.password != user.password: # Assuming phone is used as password
#         raise HTTPException(status_code=401, detail="Invalid credentials")

#     # Create new access token
#     access_token_expires = timedelta(hours=0.5)
#     access_token = create_access_token(
#         data={"sub": user_in_db.user_email, "user_id": user_in_db.user_phone}, expires_delta=access_token_expires
#     )

#     return {
#         "access_token": access_token,
#         "token_type": "bearer",
#     }
