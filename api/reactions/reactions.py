from typing import Annotated

from fastapi import APIRouter, Depends, Body

from app.posts.schemas.reaction import CreateReactionRequestSchema
from app.posts.service.reactions import ReactionService
from app.users.models import User
from core.dependencies.current_user import get_current_user

reaction_router = APIRouter(tags=['reaction'], prefix='/posts/{post_id}')


@reaction_router.post("/react",
                      summary="Leave reaction on a post",
                      description="Leave reaction on a post")
async def react(
        reaction: Annotated[CreateReactionRequestSchema, Body()],
        user: User = Depends(get_current_user),

):
    return await ReactionService.leave_reation(user, reaction)


@reaction_router.delete("/react",
                        summary="Remove reaction on a post",
                        description="Remove reaction on a post")
async def unreact(
        post_id: int,
        user: User = Depends(get_current_user),
):
    return await ReactionService.delete_reaction(user, post_id)
