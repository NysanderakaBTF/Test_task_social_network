from sqlalchemy import select, and_, delete
from starlette.responses import Response

from app.posts.models.posts import Post
from app.posts.models.reactions import Reaction
from app.posts.schemas.reaction import CreateReactionRequestSchema, CreateReactionResponseSchema
from app.posts.service.post import PostService
from app.users.models.user import User
from core.db.db_config import provide_session
from fastapi.exceptions import HTTPException


class ReactionService:

    @staticmethod
    async def leave_reation(user: User, reaction_d: CreateReactionRequestSchema):
        reaction_d.user_id = user.id
        async with provide_session() as session:
            rating = await session.execute(select(Reaction).where(and_(
                Reaction.post_id == reaction_d.post_id,
                Reaction.user_id == user.id
            )))
            res = rating.scalar()
            if res:
                res.is_like = reaction_d.is_like
                session.add(res)
                await session.commit()
                await session.refresh(res)
                return res
            else:
                post = await PostService.get_post(reaction_d.post_id)
                if post.user_id == user.id:
                    raise HTTPException(status_code=403, detail="You cant rate yourself")
                reaction = Reaction(**reaction_d.dict())
                session.add(reaction)
                await session.commit()
                await session.refresh(reaction)
                return reaction

    @staticmethod
    async def delete_reaction(user: User, post_id: int):
        async with provide_session() as session:
            await session.execute(delete(Post).where(and_(Reaction.post_id == post_id, Reaction.user_id == user.id)))
        return Response(status_code=204)
