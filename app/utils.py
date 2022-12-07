# ImportError: cannot import name 'CryptContext' from 'passlib' -> 
# Resolution: from passlib.context import CryptContext not from passlib import CryptContext
from datetime import datetime, timedelta
from typing import Union

from dotenv import dotenv_values
from jose import jwt
from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
config = dotenv_values(".env")


SECRET_KEY = config['JWT_SECRET']
ALGORITHM = "HS256"


def get_password(password: str) -> str: 
    return password_context.hash(password)

def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)

def create_access_token(subject: str, expires_delta: Union[timedelta, None] = None):
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    data_to_encode = {"sub": str(subject) , "exp": expire}
    encoded_jwt = jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)

    # print(encoded_jwt)

    return encoded_jwt
