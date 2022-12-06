from fastapi import FastAPI
from pydantic import BaseSettings
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models.user import User
from app.routes.user import user_router
app = FastAPI()


app.include_router(user_router, tags=["user"], prefix="/user")


@app.get("/", tags=["Home"])
def get_root() -> dict:
    return {
        "message": "Welcome to the okteto's app."
    }

class Settings(BaseSettings):
    MONGODB_URI: str

    class Config:
        env_file = ".env"

settings = Settings()


@app.on_event("startup")
async def startup_db():
    print(settings)
    # print(settings)
    conn_str = settings.MONGODB_URI
    client = AsyncIOMotorClient(conn_str, serverSelectionTimeoutMS=10000)
    await init_beanie(client.journal_db, document_models=[User]) # If model name is not included here we will get an error #CollectionNotInitalised
