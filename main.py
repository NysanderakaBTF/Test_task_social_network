from fastapi import FastAPI

from api.posts.posts import posts_router
from api.reactions.reactions import reaction_router
from api.users.users import user_router

app = FastAPI(
    title='Social network task',
    description="Test task",
    version="0.0.1"
)

app.include_router(user_router)
app.include_router(posts_router)
app.include_router(reaction_router)



