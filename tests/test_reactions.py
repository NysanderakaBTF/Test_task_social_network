import pytest
from httpx import AsyncClient

from main import app


@pytest.mark.asyncio
async def test_create_post_reaction_forbidden():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as test_app:
        auth = await test_app.post("/user/login", data={
            "username": "test",
            "password": "testtest"
        })
        post = await test_app.post("/posts/",
                                   json={
                                       "title": "Test Post",
                                       "content": "Test Content"
                                   },
                                   headers={"Authorization": f"Bearer {auth.json()['access_token']}",
                                            "accept": "application/json",
                                            "Content-Type": "application/json"
                                            })
        response = await test_app.post(f'/posts/{post.json()["id"]}/react',
                                       params={
                                           "reaction": "True"
                                       })
        assert response.status_code == 403


@pytest.mark.asyncio
async def test_create_post_reaction_forbidden():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as test_app:
        auth = await test_app.post("/user/login", data={
            "username": "test",
            "password": "testtest"
        })
        post = await test_app.post("/posts/",
                                   json={
                                       "title": "Test Post",
                                       "content": "Test Content"
                                   },
                                   headers={"Authorization": f"Bearer {auth.json()['access_token']}",
                                            "accept": "application/json",
                                            "Content-Type": "application/json"
                                            })
        response = await test_app.post(f'/posts/{post.json()["id"]}/react',
                                       params={
                                           "reaction": "True"
                                       },
                                       headers={"Authorization": f"Bearer {auth.json()['access_token']}"
                                                })
        assert response.status_code == 403


@pytest.mark.asyncio
async def test_create_post_reaction():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as test_app:
        auth = await test_app.post("/user/login", data={
            "username": "test",
            "password": "testtest"
        })
        auth2 = await test_app.post('/user/signup',
                                    json={
                                        "username": "test2",
                                        "password1": "test2test2",
                                        "password2": "test2test2",
                                        "email": "seregilikorrit@proton.me"
                                    }
                                    )
        auth2 = await test_app.post('/user/login',
                                    data={
                                        "username": "test2",
                                        "password": "test2test2"
                                    })
        post = await test_app.post("/posts/",
                                   json={
                                       "title": "Test Post",
                                       "content": "Test Content"
                                   },
                                   headers={"Authorization": f"Bearer {auth.json()['access_token']}",
                                            "accept": "application/json",
                                            "Content-Type": "application/json"
                                            })
        response = await test_app.post(f'/posts/{post.json()["id"]}/react',
                                       params={
                                           "reaction": "True"
                                       },
                                       headers={"Authorization": f"Bearer {auth2.json()['access_token']}",
                                                "accept": "application/json",
                                                "Content-Type": "application/json"
                                                })
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_unreact_post_reaction():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as test_app:
        auth = await test_app.post("/user/login", data={
            "username": "test",
            "password": "testtest"
        })
        auth2 = await test_app.post('/user/signup',
                                    json={
                                        "username": "test2",
                                        "password1": "test2test2",
                                        "password2": "test2test2",
                                        "email": "seregilikorrit@proton.me"
                                    }
                                    )
        auth2 = await test_app.post('/user/login',
                                    data={
                                        "username": "test2",
                                        "password": "test2test2"
                                    })
        post = await test_app.post("/posts/",
                                   json={
                                       "title": "Test Post",
                                       "content": "Test Content"
                                   },
                                   headers={"Authorization": f"Bearer {auth.json()['access_token']}",
                                            "accept": "application/json",
                                            "Content-Type": "application/json"
                                            })
        response = await test_app.post(f'/posts/{post.json()["id"]}/react',
                                       params={
                                           "reaction": "True"
                                       },
                                       headers={"Authorization": f"Bearer {auth2.json()['access_token']}",
                                                "accept": "application/json",
                                                "Content-Type": "application/json"
                                                })

        response2 = await test_app.delete(f'/posts/{post.json()["id"]}/react',
                                          headers={"Authorization": f"Bearer {auth2.json()['access_token']}"})
        assert response.status_code == 200
