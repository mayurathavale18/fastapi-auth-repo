# from fastapi import Header, HTTPException, Depends, Request
# from app.utils.auth import verify_access_token
# from typing import Optional, Annotated

# async def get_current_user(req: Request):
#     # Extract the token from the Authorization header
#     print("token : ", req.headers["Authorization"])
#     token = req.headers["Authorization"].split(" ")[1]
#     # token = authorization.split(" ")[1]  # "Bearer <token>"
#     try:
#         user = verify_access_token(token)
#         return user  # Return the decoded user data (e.g., user ID)
#     except Exception as e:
#         raise HTTPException(status_code=401, detail=str(e))
