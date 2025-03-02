from fastapi import (FastAPI, Depends)

from database.db import Base, engine
from auth.routes import auth_router
from auth.dependencies import AccessTokenBearer

Base.metadata.create_all(engine)

app = FastAPI(
    title="Autentication"
)

app.include_router(auth_router)

access_token_bearer = AccessTokenBearer()

@app.get("/")
async def home(
    token_details=Depends(access_token_bearer)
):
    return {
        "message": "Welcome Home!"
    }
