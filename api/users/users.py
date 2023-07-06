from typing import List, Annotated

from fastapi import APIRouter, Query, Body, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.schemas.token import JWTTokenSchema
from app.users.models.user import User
from app.users.schemas.user import RetriveUserResponseSchema, UserCreateResponceSchema, CreateUserRequestSchema
from app.users.service.user_service import UserService
from core.dependencies.current_user import get_current_user

user_router = APIRouter(tags=["user"], prefix='/user')


@user_router.get('/all',
                 description="Get a list of users (paginated)",
                 summary="Get all users",
                 response_model=List[RetriveUserResponseSchema])
async def get_all_users(
        limit: int = Query(default=20),
        offset: int = Query(default=0)
):
    return await UserService.get_all_users(limit, offset)


@user_router.delete('/me',
                    summary="Delete account",
                    description="Delete account")
async def delete(current_user: User = Depends(get_current_user)):
    return await UserService.delete_user(current_user)


@user_router.get("/me",
                 summary="Get info about current user",
                 description="Get info about current user",
                 response_model=RetriveUserResponseSchema
                 )
async def get_current_user(current_user: User = Depends(get_current_user)):
    return current_user


@user_router.get('/{user_id}',
                 description="Get full info about user",
                 summary="Get one users",
                 response_model=RetriveUserResponseSchema
                 )
async def get_user(user_id: int):
    return await UserService.get_user(user_id)


@user_router.post("/signup",
                  response_model=UserCreateResponceSchema,
                  description="Create new user",
                  summary="Creation of user")
async def create_user(user: Annotated[CreateUserRequestSchema, Body()],
                      ):
    return await UserService.create_user(user=user)


@user_router.post("/login",
                  summary="User login",
                  description="Login with username and password",
                  response_model=JWTTokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                ):
    token = await UserService().authenticate_user(
        username=form_data.username,
        password=form_data.password)
    return token