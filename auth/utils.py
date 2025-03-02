from datetime import (datetime, timedelta,)
import uuid

import jwt
from passlib.context import CryptContext

passwd_context = CryptContext(
    schemes=['bcrypt']
)

JWT_SECRET = "HelloWorld"
JWT_ALGORITHM = "HS256"

def generate_password_hash(password: str) -> str:
    return passwd_context.hash(password)

def verify_password(password:str, hash: str) -> bool:
    return passwd_context.verify(password, hash)

def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool = False) -> str:
    payload = {
        "user": user_data,
        "exp": datetime.now() + (expiry if expiry else timedelta(minutes=60)),
        "jit": str(uuid.uuid4()),
        "refresh": refresh,
    }
    token = jwt.encode(
        payload=payload,
        key=JWT_SECRET,
        algorithm=JWT_ALGORITHM,
    )
    return token

def decode_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
            jwt=token,
            algorithms=[JWT_ALGORITHM],
        )
        return token_data
    except jwt.PyJWTError as jwte:
        print(jwte,"*******************************")
        return None
    except Exception as e:
        print(e,"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        return None