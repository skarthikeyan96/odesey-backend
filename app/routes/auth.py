from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from app.deps.auth_deps import get_current_user
from uuid import UUID

from app.models.user import User
from app.utils import create_access_token, verify_password
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class UserData(BaseModel):
    user_id: UUID
    username: str
    email: str

# create the router variable

auth_router = APIRouter()
ACCESS_TOKEN_EXPIRE_MINUTES = 30

@auth_router.post('/login')
# using oauth2PasswordRequestForm as a dependency
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    email = form_data.username # entering email in the form
    password = form_data.password

    # get the user by email 
    user = await User.find_one(User.email == email)

    # if user is not present raise an exception
    if not user:
        # raise exception with 400
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"} # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/WWW-Authenticate
        )
    # verify_password() => send in the password entered in the form and password present for the user from db
    if not verify_password(password=password , hashed_pass=user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Email or Password')
    
    # print(user)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(user.user_id,expires_delta=access_token_expires)
    # Store access tokens in cookie from the server
    response.set_cookie('access_token', access_token, 15 * 60,
                        15 * 60, '/', None, False, True, 'lax')

    return {"access_token": access_token, "token_type": "bearer"} # temporarily sending the access token in the API response.

@auth_router.get('/user/me', response_model =UserData)
async def get_current_active_user(user: User = Depends(get_current_user)):
    return user
