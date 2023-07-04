from datetime import datetime

from pydantic import BaseModel, Field

from app.users.schemas.user import RetriveUserResponseSchema


class CreatePostRequestSchema(BaseModel):
    title: str = Field(..., description="Post title")
    content: str = Field(..., description="Post content")


class CreatePostResponseSchema(BaseModel):
    id: str = Field(..., description="Post id")
    title: str = Field(..., description="Post title")
    content: str = Field(..., description="Post content")
    owner: RetriveUserResponseSchema = Field(..., description="Post author")

    class Config:
        orm_mode = True


class RetrivePostResponseSchema(CreatePostResponseSchema):
    created_at: datetime = Field(..., description="Post created at")
    updated_at: datetime = Field(..., description="Post updated at")
    likes: int = Field(..., description="Number of likes")
    dislikes: int = Field(..., description="Number of dislikes")
    class Config:
        orm_mode = True

class UpdatePostRequestSchema(BaseModel):
    id: str = Field(..., description="Post id")
    title: str = Field(..., description="Post title")
    content: str = Field(..., description="Post content")

