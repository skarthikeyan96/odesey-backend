from pydantic import BaseModel, EmailStr, Field


class UserAuth(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """        
    email: EmailStr = Field(..., description="user email")
    username: str = Field(...,min_length=5, max_length=25, description="username")
    password: str = Field(..., min_length=5, max_length=24)