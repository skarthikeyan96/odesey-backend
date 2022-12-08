""" Summary: deps import """
from datetime import timedelta
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from app.deps.auth_deps import get_current_user
from app.models.user import User
from app.utils import create_access_token, verify_password


class Token(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """
    access_token: str
    token_type: str

class UserData(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """
    user_id: UUID
    username: str
    email: str

# create the router variable

auth_router = APIRouter()
ACCESS_TOKEN_EXPIRE_MINUTES = 30

@auth_router.post('/login')
# using oauth2PasswordRequestForm as a dependency
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    """_summary_

    Args:
        response (Response): _description_
        form_data (OAuth2PasswordRequestForm, optional): _description_. Defaults to Depends().

    Raises:
        HTTPException: _description_
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
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

    return {"access_token": access_token, "token_type": "bearer"} # temporarily sending the access token in the API response.

@auth_router.get('/user/me', response_model =UserData)
async def get_current_active_user(user: User = Depends(get_current_user)):
    """_summary_

    Args:
        user (User, optional): _description_. Defaults to Depends(get_current_user).

    Returns:
        _type_: _description_
    """
    return user


@auth_router.delete('/user/{username}', response_description="delete the user")
async def delete_user(username, user: User = Depends(get_current_user)):
    """_summary_

    Args:
        username (_type_): _description_
        user (User, optional): _description_. Defaults to Depends(get_current_user).

    Returns:
        _type_: _description_
    """ 
    user = await User.find_one(User.username == username)
    if user:
        await user.delete()
        return {"message": "success"}
    # pass