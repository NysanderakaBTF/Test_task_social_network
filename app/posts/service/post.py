from sqlalchemy import select, func, and_
from starlette.responses import Response

from app.posts.models.posts import Post
from app.posts.models.reactions import Reaction
from app.posts.schemas.posts import CreatePostRequestSchema, UpdatePostRequestSchema

from app.users.models.user import User
from core.db.db_config import provide_session

from fastapi.exceptions import HTTPException


class PostService:

    @staticmethod
    async def get_posts_by_user(user: User, limit: int = 10, offset: int = 0):
        async with provide_session() as session:
            res = await session.execute(
                select(Post,
                       func.count(Reaction.id).label("reactions"))
                .outerjoin(Reaction, and_(Reaction.is_like == False, Reaction.post_id == Post.id))
                .group_by(Post.id)
                .order_by(Post.updated_at)
                .limit(limit)
                .offset(offset)
            )
            ans1 = res.unique().fetchall()

            res2 = await session.execute(
                select(Post,
                       func.count(Reaction.id).label("reactions"))
                .outerjoin(Reaction, and_(Reaction.is_like == True, Reaction.post_id == Post.id))
                .group_by(Post.id)
                .order_by(Post.updated_at)
                .limit(limit)
                .offset(offset)
            )

            ans2 = res2.unique().fetchall()

            posts_with_likes_dislikes = []
            for i in range(len(ans1)):
                posts_with_likes_dislikes.append({
                    'post': ans1[i][0],
                    "dislikes": ans1[i][1],
                    "likes": ans2[i][1]
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
                            func.count(Reaction.id).label("reactions"))
                     .outerjoin(Reaction, and_(Reaction.is_like == False, Reaction.post_id == Post.id))
                     .group_by(Post.id)
                     .where(Post.id == post_id)
                     )
            res = await session.execute(
                query
            )
            ans = res.fetchone()
            res2 = await session.execute(
                select(Post,
                       func.count(Reaction.id).label("reactions"))
                .outerjoin(Reaction, and_(Reaction.is_like == True, Reaction.post_id == Post.id))
                .group_by(Post.id)
                .where(Post.id == post_id)
            )

            ans2 = res2.fetchone()

            result = {"post": ans[0],
                      "dislikes": ans[1],
                      "likes": ans2[1]}
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
