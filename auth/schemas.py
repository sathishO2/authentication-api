from pydantic import BaseModel, Field
from typing import Optional


class UserCreateSchema(BaseModel):
    first_name: str = Field(max_length=25)
    last_name: Optional[str] = Field(max_length=25)
    username: str = Field(max_length=10)
    email: str = Field(max_length=40)
    password: str = Field(min_length=4)

class UserLogingSchema(BaseModel):
    email: str 
    password: str