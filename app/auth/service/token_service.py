from jose import JWTError

from app.auth.schemas.token import JWTTokenSchema
from core.utils.token import TokenHelper


class JWTTokenService:

    @classmethod
    async def create_access_token(cls, data: dict):
        return TokenHelper.encode(payload=data)

    @classmethod
    async def create_refresh_token(cls, token: str,
                                   refresh_token: str):
        token = TokenHelper.decode(token=token)
        refresh_token = TokenHelper.decode(token=refresh_token)
        if refresh_token.get("sub") != "refresh":
            raise JWTError("Invalid refresh token")
        return JWTTokenSchema(
            token=TokenHelper.encode(payload={"user_id": token.get("user_id")}),
            refresh_token=TokenHelper.encode(payload={"sub": "refresh"}),
        )

    @classmethod
    async def verify_token(cls, token: str):
        return TokenHelper.decode(token=token)
