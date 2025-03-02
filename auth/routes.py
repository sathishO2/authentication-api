from datetime import (datetime, timedelta)

from fastapi import (APIRouter, Depends, status,)
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from .schemas import (UserCreateSchema, UserLogingSchema)
from .service import UserService
from database.db import get_db
from .utils import verify_password, create_access_token

auth_router = APIRouter(
    tags=["Auth"],
    prefix="/auth"
)
user_service = UserService()

@auth_router.post("/signup")
def create_user_account(
    user_data: UserCreateSchema, db: Session = Depends(get_db)
):
    email = user_data.email
    user_exists = user_service.user_exists(email,db)

    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User with email already exists",
        )
    new_user = user_service.create_user(user_data, db)
    new_user_info = {
        "id": new_user.id,
        "name": f"{new_user.first_name} {new_user.last_name}",
        "email": new_user.email,
        "is_active": new_user.is_active,
    }
    return JSONResponse(
    status_code=status.HTTP_201_CREATED,
    content={
        "message": "User Created Successfully.",
        "data": new_user_info
    }
)

@auth_router.post("/login")
def login_users(
    login_data: UserLogingSchema, db: Session = Depends(get_db)
):
    email = login_data.email
    password = login_data.password

    user = user_service.get_user_by_email(email, db)
    if user:
        password_valid = verify_password(password, user.password_hash)
        if password_valid:
            access_token =  create_access_token(
                user_data={"email": user.email, "user_id": str(user.id)}
            )
            refresh_token =  create_access_token(
                user_data={"email": user.email, "user_id": str(user.id)},
                refresh=True,
                expiry=timedelta(days=3)
            )

            return JSONResponse(
                content={
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user":{
                        "email": user.email, 
                        "user_id": str(user.id),
                    },
                }
            )


    raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Email Or Password"
        )
