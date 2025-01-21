# import json
# from app.utils.database import get_db_connection
# from app.models.user import UserSchema

# def create_user(user: UserSchema):
#     connection = get_db_connection()
#     try:
#         with connection.cursor() as cursor:
#             sql = """
#                 INSERT INTO users (user_email, user_phone, first_name, last_name, activated_on, payment_date, transaction_id, auths)
#                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
#             """
#             values = (
#                 user.user_email, user.user_phone, user.first_name, user.last_name,
#                 user.activated_on, user.payment_date, user.transaction_id, json.dumps(user.auths)
#             )

#             print("Executing SQL:", sql)  # Debugging
#             print("With values:", values)  # Debugging

#             cursor.execute(sql, values)
#             connection.commit()

#             print("✅ User inserted successfully")  # Debugging
#     except Exception as e:
#         print("❌ Error:", e)  # Debugging
#     finally:
#         connection.close()


from app.utils.database import SessionLocal
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreateSchema
# Get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create user function
def create_user(db: Session, user: UserCreateSchema):
    db_user = User(
        user_email=user.user_email,
        user_phone=user.user_phone,
        first_name=user.first_name,
        last_name=user.last_name,
        password=user.password,
        activated_on=user.activated_on,
        payment_date=user.payment_date,
        transaction_id=user.transaction_id,
        auths=user.auths.model_dump_json() if user.auths else None  # Serialize the auths as a dictionary
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.user_email == email).first()