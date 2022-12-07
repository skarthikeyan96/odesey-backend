# to create dependcies when accessing the secure data
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import BaseModel, ValidationError

from app.models.user import User
from app.utils import ALGORITHM, SECRET_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login', scheme_name="JWT")

class TokenPayload(BaseModel):
    sub: UUID
    exp: int

async def get_current_user(token: str = Depends(oauth2_scheme)):
    # decode the payload and get the user id
    #
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

        # print(payload)
        user_id = TokenPayload(**payload).sub

        # return payload
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="not able to validate credentials"
        )
    
    user = await User.find_one(User.user_id == user_id)

    if not user:
        raise(HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found"
        ))
    return user
    # pass