import pytest
from fastapi import HTTPException
from httpx import AsyncClient

from main import app


@pytest.mark.asyncio
async def test_get_all_posts():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        posts = await client.get("/posts/all")
        assert posts.status_code == 200


@pytest.mark.asyncio
async def test_create_post_unauthorized():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.post("/posts/", data={
            "title": "Test Post",
            "content": "Test Content"
        })
        assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_my_posts_unauthorized():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as test_app:
        response = await test_app.get("/posts/my")
        assert response.status_code == 401


@pytest.mark.asyncio
async def test_delete_posts_unauthorized():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as test_app:
        response = await test_app.delete("/posts/4")
        assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_post():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as test_app:
        auth = await test_app.post(url="/user/login", data={
            "username": "test",
            "password": "testtest"
        })
        print(auth.status_code)
        if auth.status_code == 404:
            qqq = await test_app.post(url="/user/signup", json={
                "username": "test",
                "password1": "testtest",
                "password2": "testtest",
                "email": "kave7771@outlook.com"
            })
            print(qqq.json)
        auth2 = await test_app.post(url="/user/login", data={
            "username": "test",
            "password": "testtest"
        })
        print(auth2.json())
        response = await test_app.post(url="/posts/",
                                       json={
                                           "title": "Test Post",
                                           "content": "Test Content"
                                       },
                                       headers={"Authorization": f"Bearer {auth2.json()['access_token']}",
                                                "accept": "application/json",
                                                "Content-Type": "application/json"
                                                })
        assert response.status_code == 200
        resss = response.json()
        assert resss["title"] == "Test Post"
        assert resss["content"] == "Test Content"


@pytest.mark.asyncio
async def test_get_my_posts():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as test_app:
        auth = await test_app.post(url="/user/login", data={
            "username": "test",
            "password": "testtest"
        })
        response = await test_app.get("/posts/my",
                                      headers={"Authorization": f"Bearer {auth.json()['access_token']}"})
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_post():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as test_app:
        auth = await test_app.post("/user/login", data={
            "username": "test",
            "password": "testtest"
        })
        response = await test_app.post("/posts/",
                                       json={
                                           "title": "Test Post",
                                           "content": "Test Content"
                                       },
                                       headers={"Authorization": f"Bearer {auth.json()['access_token']}"
                                                })
        info = response.json()
        print(info)
        getted = await test_app.get(f"/posts/{info['id']}")
        assert getted.status_code == 200
        expected = dict(
            post=info,
            likes=0,
            dislikes=0
        )
        assert getted.json() == expected


@pytest.mark.asyncio
async def test_delete_posts():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as test_app:
        auth = await test_app.post("/user/login", data={
            "username": "test",
            "password": "testtest"
        })
        response = await test_app.post("/posts/",
                                       json={
                                           "title": "Test Post",
                                           "content": "Test Content"
                                       },
                                       headers={"Authorization": f"Bearer {auth.json()['access_token']}",
                                                "accept": "application/json",
                                                "Content-Type": "application/json"
                                                })
        info = response.json()

        response2 = await test_app.delete(f"/posts/{info['id']}",
                                          headers={"Authorization": f"Bearer {auth.json()['access_token']}"})
        assert response2.status_code == 204


@pytest.mark.asyncio
async def test_update_post():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as test_app:
        auth = await test_app.post("/user/login", data={
            "username": "test",
            "password": "testtest"
        })
        response = await test_app.post("/posts/",
                                       json={
                                           "title": "Test Post",
                                           "content": "Test Content"
                                       },
                                       headers={"Authorization": f"Bearer {auth.json()['access_token']}",
                                                "accept": "application/json",
                                                "Content-Type": "application/json"
                                                })
        info = response.json()
        assert info['title'] == "Test Post"
        response = await test_app.put(f"/posts/{info['id']}",
                                      json={
                                          "title": "New Title",
                                          "content": "New Content"
                                      },
                                      headers={"Authorization": f"Bearer {auth.json()['access_token']}",
                                               "accept": "application/json",
                                               "Content-Type": "application/json"
                                               }
                                      )
        ans = response.json()

        assert ans['title'] == "New Title"
        assert ans['content'] == "New Content"