import pytest
from httpx import AsyncClient

from main import app


@pytest.mark.asyncio
async def test_create_user():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as test_app:
        auth = await test_app.post('/user/login',
                                   data={
                                       "username": "test2",
                                       "password": "test2test2"
                                   }
                                   )
        if auth.status_code != 404:
            await test_app.delete('/user/me',
                                  headers={
                                      "Authorization": f"Bearer {auth.json()['access_token']}"
                                  })
        auth = await test_app.post('/user/signup',
                                   json={
                                       "username": "test2",
                                       "password1": "test2test2",
                                       "password2": "test2test2",
                                       "email": "seregilikorrit@proton.me"
                                   }
                                   )
        assert auth.status_code == 200
        assert auth.json()['username'] == "test2"


@pytest.mark.asyncio
async def test_get_users():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as test_app:
        response = await test_app.get('/user/all')
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_login():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as test_app:
        response = await test_app.post('/user/login',
                                       data={"username": "test2",
                                             "password": "test2test2"
                                             })
        assert response.status_code == 200
        assert response.json()['access_token'] is not None


@pytest.mark.asyncio
async def test_me():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as test_app:
        auth = await test_app.post('/user/login',
                                   data={
                                       "username": "test2",
                                       "password": "test2test2"
                                   }
                                   )
        response = await test_app.get('/user/me',
                                       headers={
                                           "Authorization": f"Bearer {auth.json()['access_token']}"
                                       })
        assert response.status_code == 200
        assert response.json()['username'] == "test2"


@pytest.mark.asyncio
async def test_delete_user():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as test_app:
        auth = await test_app.post('/user/login',
                                   data={
                                       "username": "test2",
                                       "password": "test2test2"
                                   }
                                   )
        response = await test_app.delete('/user/me',
                                         headers={
                                             "Authorization": f"Bearer {auth.json()['access_token']}"
                                         })
        assert response.status_code == 200
