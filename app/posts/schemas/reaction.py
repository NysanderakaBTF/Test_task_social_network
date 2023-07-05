from pydantic import BaseModel, Field

from app.posts.schemas.posts import RetrivePostResponseSchema
from app.users.schemas.user import RetriveUserResponseSchema


class CreateReactionRequestSchema(BaseModel):
    user_id: int = Field(description='User ID')
    post_id: int = Field(..., description='Post ID')
    is_like: bool = Field(..., description='Reaction type (true = like, false = dislike)')

class CreateReactionResponseSchema(BaseModel):
    id: int = Field(..., description='Reaction id')
    user: RetriveUserResponseSchema = Field(..., description='Who creared reaction')
    post: RetrivePostResponseSchema = Field(..., description='Post')
    is_like: bool = Field(..., description='Reaction type (true = like, false = dislike)')

    class Config:
        orm_mode = True
