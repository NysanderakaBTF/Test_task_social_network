from sqlalchemy import select, and_, delete
from starlette.responses import Response

from app.posts.models.posts import Post
from app.posts.models.reactions import Reaction
from app.users.models.user import User
from core.db.db_config import provide_session
from fastapi.exceptions import HTTPException


class ReactionService:

    @staticmethod
    async def leave_reation(user: User, post_id: int, reaction: bool):
        async with provide_session() as session:
            rating = await session.execute(select(Reaction).where(and_(
                Reaction.post_id == post_id,
                Reaction.user_id == user.id
            )))
            res = rating.scalar()
            if res:
                res.is_like = reaction
                session.add(res)
                await session.commit()
                await session.refresh(res)
                return res
            else:
                post = await session.execute(select(Post).where(Post.id == post_id))
                post = post.scalar()
                if not post:
                    raise HTTPException(status_code=404, detail="Post not found")
                if post.owner_id == user.id:
                    raise HTTPException(status_code=403, detail="You cant rate yourself")
                reaction = Reaction(post_id=post_id, user_id=user.id, is_like=reaction)
                session.add(reaction)
                await session.commit()
                await session.refresh(reaction)
                return reaction

    @staticmethod
    async def delete_reaction(user: User, post_id: int):
        async with provide_session() as session:
            await session.execute(delete(Post).where(and_(Reaction.post_id == post_id, Reaction.user_id == user.id)))
        return Response(status_code=204)
