import pymongo
from dotenv import dotenv_values
from fastapi import APIRouter, HTTPException, status
from passlib.context import CryptContext

from app.models.user import User
from app.schema.user import UserAuth

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
config = dotenv_values(".env")

user_router = APIRouter()



def get_password(password: str) -> str: 
    return password_context.hash(password)

def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


@user_router.post("/create", summary='create user', status_code=status.HTTP_201_CREATED)
async def create_user(data: UserAuth):
    try:
        print(data)
        user = User(
            username=data.username,
            email=data.email,
            hashed_password=get_password(data.password)
        )
        print("user", user)
        response = await user.save()
        print(response)
        return {"message": "user created"}
    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="username or email already exists"
        )


