from pydantic import BaseModel , EmailStr, Field

class UserAuth(BaseModel):
    email: EmailStr = Field(..., description="user email")
    username: str = Field(...,min_length=5, max_length=25, description="username")
    password: str = Field(..., min_length=5, max_length=24)