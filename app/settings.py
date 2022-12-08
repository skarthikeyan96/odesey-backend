from pydantic import BaseSettings


class Settings(BaseSettings):
    MONGODB_URI: str
    JWT_SECRET: str

    class Config:
        env_file = ".env"
