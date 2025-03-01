from fastapi import FastAPI

from database.db import Base, engine
from auth.routes import auth_router

Base.metadata.create_all(engine)

app = FastAPI(
    title="Autentication"
)

app.include_router(auth_router)

@app.get("/")
async def home():
    return {
        "message": "Welcome Home!"
    }
