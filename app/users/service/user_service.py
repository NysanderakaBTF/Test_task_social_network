from typing import List

from fastapi import HTTPException
from sqlalchemy import select, or_, and_
from sqlalchemy.orm import joinedload

from app.auth.schemas.token import JWTTokenSchema
from app.posts.models.reactions import Reaction
from app.users.schemas.user import CreateUserRequestSchema
from app.users.models.user import User
from core.db.db_config import provide_session
from core.utils.email_virifier import EmailVerifier
from core.utils.hasher import PasswordHasher
from core.utils.token import TokenHelper


class UserService:

    @staticmethod
    async def get_all_users(limit: int = 20,
                            offset: int = 0) -> List[User]:
        async with provide_session() as session:
            res = await session.execute(select(User).limit(limit).offset(offset))
        return res.scalars().all()

    @staticmethod
    async def get_user(user_id: int) -> User:
        async with provide_session() as session:
            result = await session.execute(select(User).where(User.id == user_id))
            user = result.scalar()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
        return user

    @staticmethod
    async def create_user(user: CreateUserRequestSchema):
        if user.password1 != user.password2:
            raise HTTPException(status_code=400, detail="Passwords don't match")

        if not await EmailVerifier().verify(user.email):
            raise HTTPException(status_code=400, detail="Invalid email")

        async with provide_session() as session:
            exists = await session.execute(
                select(User).where(or_(User.email == user.email, User.username == user.username)))
            exists = bool(exists.scalar())
            if exists:
                raise HTTPException(status_code=400, detail="Username or email already exists")
            data = user.dict()
            data['password'] = PasswordHasher.hash(data['password1'])
            data.pop('password1')
            data.pop('password2')
            user = User(**data)
            session.add(user)
            await session.commit()
            await session.refresh(user)
            await session.commit()
            return user

    @staticmethod
    async def delete_user(current_user: User):
        async with provide_session() as session:
            await session.delete(current_user)
            await session.commit()

    @staticmethod
    async def authenticate_user(username: str,
                                password: str,
                                ):
        async with provide_session() as session:
            res = await session.execute(select(User).where(User.username == username))
            print(res)
            user = res.scalar()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            if not PasswordHasher.verify(password, user.password):
                raise HTTPException(status_code=401, detail="Incorrect password")
        return JWTTokenSchema(
            access_token=TokenHelper.encode(payload={"user_id": user.id}),
            refresh_token=TokenHelper.encode(payload={"sub": "refresh"})
        )