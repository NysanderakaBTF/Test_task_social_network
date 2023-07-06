from typing import Annotated

from fastapi import APIRouter, Depends, Query, Body

from app.posts.schemas.posts import CreatePostResponseSchema, CreatePostRequestSchema, UpdatePostRequestSchema
from app.posts.service.post import PostService
from app.users.models.user import User
from core.dependencies.current_user import get_current_user

posts_router = APIRouter(tags=['posts'], prefix='/posts')


@posts_router.get('/my',
                  summary="Get user posts",
                  description="Get all user posts with pagination")
async def get_posts_by_user(user: User = Depends(get_current_user),
                            limit: int = Query(default=10),
                            offset: int = Query(default=0)):
    return await PostService.get_posts_by_user(user, limit, offset)


@posts_router.post('/',
                   description="Creating a user, user dependency gurantees authentication",
                   summary="Create post",
                  )
async def new_post(post: Annotated[CreatePostRequestSchema, Body()],
                   user: User = Depends(get_current_user),
                   ):
    return await PostService.create_post(post, user)

@posts_router.get('/all',
                  summary="Get all posts",
                  description="Get all posts with pagination")
async def get_all_posts(limit: int = Query(default=10),
                        offset: int = Query(default=0)):
    return await PostService.get_all_posts(limit, offset)


@posts_router.get('/{post_id}',
                  description="Get a post by id",
                  summary="Retrive post"
                  )
async def get_post(post_id: int):
    return await PostService.get_post(post_id)





@posts_router.delete('/{post_id}',
                     summary="Delete post by id",
                     description="Deleting post by id")
async def delete(post_id:int, user:User = Depends(get_current_user)):
    return await PostService.delete_post(user, post_id)



@posts_router.put('/{post_id}',
                  summary="Updating post by id",
                  description="Updating post by id")
async def update(post_id:int,
                 post_data: Annotated[UpdatePostRequestSchema, Body()],
                 user:User = Depends(get_current_user)):
    return await PostService.update_post(user, post_id, post_data)