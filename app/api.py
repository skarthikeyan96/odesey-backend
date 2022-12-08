from beanie import init_beanie
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseSettings

from app.models.user import User
from app.models.journal import Journal
from app.routes.auth import auth_router
from app.routes.user import user_router
from app.routes.journal import journal_router

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://0.0.0.0:8080",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, tags=["user"], prefix="/user")
app.include_router(auth_router, tags=["auth"], prefix="/auth")
app.include_router(journal_router, tags=["journal"], prefix="/journal")


@app.get("/", tags=["Home"])
def get_root() -> dict:
    return {
        "message": "Odesey Backend"
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
    await init_beanie(client.journal_db, document_models=[User, Journal]) # If model name is not included here we will get an error #CollectionNotInitalised
