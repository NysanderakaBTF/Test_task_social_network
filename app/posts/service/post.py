import http

from sqlalchemy import select, func, delete
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
                select(Post,
                       func.count(Reaction.is_like == True).label("num_likes"),
                       func.count(Reaction.is_like == False).label("num_dislikes"),
                       )
                .join(Post.reacted_by_association)
                .options(
                    joinedload(Post.reacted_by_association),
                )
                .filter(Post.owner_id == user.id)
                .group_by(Post.id)
                .order_by(Post.updated_at)
                .limit(limit)
                .offset(offset)
            )
            print(res.fetchall())
            posts_with_likes_dislikes = []
            for post, num_likes, num_dislikes in res.fetchall():
                posts_with_likes_dislikes.append({
                    'post': post,
                    'num_likes': num_likes,
                    'num_dislikes': num_dislikes
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
            query = (select(Post,
                           )
                     .join(Post.reacted_by_association)
                     .where(Post.id == post_id)

                     )
            res = await session.execute(
                query
            )
            print(query)
            ans = res.unique().fetchall()
            print(ans)
            if not ans:
                raise HTTPException(status_code=404, detail="No post found")
            return ans

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
            post = await PostService.get_post(post_id)
            if post:
                if post.user_id == user.id:
                    await session.execute(delete(Post).where(post.id == post_id))
                else:
                    raise HTTPException(status_code=403, detail="You are not allowed to delete this post")
            else:
                raise HTTPException(status_code=404, detail="No such post")
        return Response(status_code=204)

    @staticmethod
    async def update_post(user: User, post_id: int, post_data: UpdatePostRequestSchema):
        async with provide_session() as session:
            post = await session.execute(select(Post).where(Post.id == post_id))
            if not post:
                raise HTTPException(status_code=404, detail="No post found")
            if post.owner_id != user.id:
                raise HTTPException(status_code=403, detail="Ypu can not modify this post")
            for key, value in post_data.dict().items():
                setattr(post, key, value)
            await session.commit()
            await session.refresh(post)
        return post
