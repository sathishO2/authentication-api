from fastapi import (APIRouter, Depends, status,)
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from .schemas import UserCreateSchema #, UserSchema
from .service import UserService
from database.db import get_db
from sqlalchemy.orm import Session

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
    }
    return JSONResponse(
    status_code=status.HTTP_201_CREATED,
    content={
        "message": "User Created Successfully.",
        "data": new_user_info
    }
)
