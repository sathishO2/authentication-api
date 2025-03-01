import re
from datetime import datetime

from sqlalchemy import (Column, Integer, String, DateTime, Boolean, func,)
from sqlalchemy.orm import validates
from .db import Base


class DefaultColumns(Base):
    __abstract__ = True
    __table_args__ = {'extend_existing': True}

    
    is_active = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.now,)
    updated_at = Column(DateTime, default=datetime.now,)

class User(DefaultColumns):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True,)
    username = Column(String, unique=True, nullable=False,)
    first_name = Column(String, nullable=True,)
    last_name = Column(String, nullable=True,)
    email = Column(String, unique=True, nullable=False,)
    password_hash = Column(String, nullable=False,)

    @validates('email')
    def validate_email(self, key, email:str):
        # Validate email format
        email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(email_pattern, email):
            raise ValueError("Invalid email format")
        return email.lower()