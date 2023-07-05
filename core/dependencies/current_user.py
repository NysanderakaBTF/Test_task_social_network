from datetime import datetime

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy import select
from starlette import status

from app.users.models.user import User
from core.db.db_config import provide_session
from core.utils.token import TokenHelper

reusable_oauth = OAuth2PasswordBearer(
    tokenUrl="/user/login",
    scheme_name="JWT"
)


async def get_current_user(token: str = Depends(reusable_oauth)) -> User:
    async with provide_session() as session:
        try:
            payload = TokenHelper.decode(token)
            if datetime.fromtimestamp(payload.get('exp')) < datetime.now():
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
        except (jwt.JWTError, ValidationError):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        user = await session.execute(select(User).where(User.id == payload.get('user_id')))

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Could not find user",
            )
        return user.scalar()