from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

from pydantic.types import Annotated

# Pydantic or Schema model for request body 

# Post Schema Models
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse  # Nested UserResponse model

    class Config:
        from_attributes = True

class PostOut(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
            from_attributes = True

# User Schema Models
class UserBase(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=72)

class UserCreate(UserBase):
    pass

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=72)


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: int | None = None
    email: EmailStr | None = None



class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(strict=True, gt=0)]