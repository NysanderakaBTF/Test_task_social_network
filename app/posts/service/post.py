import http

from sqlalchemy import select, func, delete, case, and_
from sqlalchemy.orm import joinedload, defer, selectinload
from starlette.responses import Response

from app.posts.models.posts import Post
from app.posts.models.reactions import Reaction
from app.posts.schemas.posts import CreatePostRequestSchema, UpdatePostRequestSchema, CreatePostResponseSchema, \
    RetrivePostResponseSchema

from app.users.models.user import User
from core.db.db_config import provide_session

from fastapi.exceptions import HTTPException


class PostService:

    @staticmethod
    async def get_posts_by_user(user: User, limit: int = 10, offset: int = 0):
        async with provide_session() as session:
            res = await session.execute(
                select(Post)
                .where(Post.owner_id == user.id)
                .order_by(Post.updated_at)
                .limit(limit)
                .offset(offset)
            )
            ans1 = res.scalars().all()
            print(ans1)
            posts_with_likes_dislikes = []
            for i in ans1:
                res2 = await session.execute(
                    select(func.count())
                    .where(and_(Reaction.post_id == i.id, Reaction.is_like == True))
                )
                res3 = await session.execute(
                    select(func.count())
                    .where(and_(Reaction.post_id == i.id, Reaction.is_like == False))
                )
                posts_with_likes_dislikes.append({
                    'post': i,
                    "likes": res2.scalar(),
                    "dislikes": res3.scalar()
                })

            return posts_with_likes_dislikes

    @staticmethod
    async def create_post(post: CreatePostRequestSchema, user: User) -> Post:
        async with provide_session() as session:
            post = Post(**post.dict(), owner_id=user.id)
            session.add(post)
            await session.commit()
            await session.refresh(post)
        return post

    @staticmethod
    async def get_post(post_id: int):
        async with provide_session() as session:
            query = (select(Post)
                     .where(Post.id == post_id)
                     )
            res = await session.execute(
                query
            )
            ans = res.scalar()

            res2 = await session.execute(
                select(func.count())
                .where(and_(Reaction.post_id == post_id, Reaction.is_like == True))
            )
            res3 = await session.execute(
                select(func.count())
                .where(and_(Reaction.post_id == post_id, Reaction.is_like == False))
            )
            result = {"post": ans,
                      "likes": res2.scalar(),
                      "dislikes": res3.scalar()}
            if not ans:
                raise HTTPException(status_code=404, detail="No post found")
            return result

    @staticmethod
    async def get_all_posts(limit: int = 10, offset: int = 0):
        async with provide_session() as session:
            res = await session.execute(
                select(Post)
                .order_by(Post.updated_at)
                .limit(limit)
                .offset(offset)
            )
            return res.scalars().all()

    @staticmethod
    async def delete_post(user: User, post_id: int):
        async with provide_session() as session:
            post = await session.execute(select(Post).where(Post.id == post_id))
            post = post.scalar()
            if post:
                if post.owner_id == user.id:
                    await session.delete(post)
                else:
                    raise HTTPException(status_code=403, detail="You are not allowed to delete this post")
            else:
                raise HTTPException(status_code=404, detail="No such post")
        return Response(status_code=204)

    @staticmethod
    async def update_post(user: User, post_id: int, post_data: UpdatePostRequestSchema):
        async with provide_session() as session:
            post = await session.execute(select(Post).where(Post.id == post_id))
            post = post.scalar()
            if not post:
                raise HTTPException(status_code=404, detail="No post found")
            if post.owner_id != user.id:
                raise HTTPException(status_code=403, detail="Ypu can not modify this post")
            for key, value in post_data.dict().items():
                setattr(post, key, value)
            await session.commit()
            await session.refresh(post)
        return post
