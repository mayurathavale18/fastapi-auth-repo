import jwt
from datetime import timedelta, timezone
from DateTime.DateTime import datetime
from typing import Optional
from passlib.context import CryptContext
import os
from dotenv import load_dotenv
# import sendlk
# from sendlk.engine import SMS
# from sendlk.responses import SmsResponse
# from sendlk.exceptions import SendLKException
# from sendlk.options import SendLKVerifyOption, SendLKCodeTemplet
# from fastapi.exceptions import HTTPException
# from starlette.responses import JSONResponse

load_dotenv()

# Secret key for encoding and decoding JWT tokens
SECRET_KEY = os.getenv("SECRET_KEY") 
ALGORITHM = os.getenv("ALGORITHM")  # HMAC using SHA-256 (or you can choose others like RS256 for public/private key)

# # SENDLK
# SENDLK_TOKEN = os.getenv("SENDLK_TOKEN")
# SENDER_ID = os.environ.get("SENDER_ID")
# SECRET = os.getenv("SECRET")

# sendlk.initialize(SENDLK_TOKEN, SECRET)

# class CustomCodeTemplate(SendLKCodeTemplet):
#     def __init__(self):
#         super().__init__()

#     def text(self, code: str) -> str:
#         return f"default code for testing : {code}"

# Function to create an access token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(hours=1)  # Default to 1 hour expiration
    
    to_encode.update({"exp": expire})
    print(type(SECRET_KEY), type(ALGORITHM))
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function to verify the access token and decode the user data
def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # Returns the decoded payload (usually user info)
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.JWTError:
        raise Exception("Token is invalid")
    
# Initialize the password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to hash a password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# # Function to verify password
# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return pwd_context.verify(plain_password, hashed_password)

# def send_verify_token(phone_number: str):
#     try:
#         options: SendLKVerifyOption = SendLKVerifyOption(
#             code_length=4,
#             expires_in=2,
#             sender_id=SENDER_ID,
#             code_template=CustomCodeTemplate()
#         )
#         response = SMS.send_verify_code(number=phone_number, verify_option=options)
#         token = response.data.get("token", None)
#         return token
#     except SendLKException as e:
#         raise HTTPException(status_code=400, details=e.message)
    
# def validate_code(token: str, code: str) -> str:
#     try:
#         # Validate the code
#         response = SMS.validate_verify_code(code=code, token=token)
#         return response.message
#     except SendLKException as e:
#         raise HTTPException(status_code=400, detail=e.message)