from app.utils.database import SessionLocal
from sqlalchemy.orm import Session
from app.models.user import User
# Get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# # Create user function
# def create_user(db: Session, user: UserCreateSchema):
#     db_user = User(
#         user_email=user.user_email,
#         user_phone=user.user_phone,
#         first_name=user.first_name if user.first_name else "",
#         last_name=user.last_name if user.last_name else "",
#         password=user.password if user.password else "",
#         activated_on=user.activated_on,
#         payment_date=user.payment_date,
#         transaction_id=user.transaction_id if user.transaction_id else "",
#         auths=user.auths.model_dump_json() if user.auths else {}  # Serialize the auths as a dictionary
#     )
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.user_email == email).first()