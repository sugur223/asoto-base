"""認証API の統合テスト"""
import pytest
from httpx import AsyncClient
from app.models.user import User


@pytest.mark.integration
@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    """ユーザー登録のテスト"""
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "newuser@example.com",
            "password": "password123",
            "full_name": "New User"
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["full_name"] == "New User"
    assert "id" in data
    assert "hashed_password" not in data  # パスワードは返さない
    assert data["is_active"] is True


@pytest.mark.integration
@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient, test_user: User):
    """重複メールアドレスでの登録テスト"""
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": test_user.email,
            "password": "password123",
            "full_name": "Duplicate User"
        }
    )

    assert response.status_code == 400
    assert "既に登録されています" in response.json()["detail"]


@pytest.mark.integration
@pytest.mark.asyncio
async def test_register_invalid_email(client: AsyncClient):
    """不正なメールアドレスでの登録テスト"""
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "invalid-email",
            "password": "password123",
            "full_name": "Invalid Email User"
        }
    )

    assert response.status_code == 422  # Validation Error


@pytest.mark.integration
@pytest.mark.asyncio
async def test_login(client: AsyncClient, test_user: User):
    """ログインのテスト"""
    response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": test_user.email,
            "password": "password123"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert len(data["access_token"]) > 0


@pytest.mark.integration
@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient, test_user: User):
    """間違ったパスワードでのログインテスト"""
    response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": test_user.email,
            "password": "wrong_password"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    assert response.status_code == 401
    assert "正しくありません" in response.json()["detail"]


@pytest.mark.integration
@pytest.mark.asyncio
async def test_login_nonexistent_user(client: AsyncClient):
    """存在しないユーザーでのログインテスト"""
    response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "nonexistent@example.com",
            "password": "password123"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    assert response.status_code == 401


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_current_user(client: AsyncClient, test_user: User, auth_headers: dict):
    """現在のユーザー情報取得のテスト"""
    response = await client.get(
        "/api/v1/auth/me",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user.email
    assert data["full_name"] == test_user.full_name
    assert data["id"] == str(test_user.id)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_current_user_unauthorized(client: AsyncClient):
    """認証なしでのユーザー情報取得テスト"""
    response = await client.get("/api/v1/auth/me")

    assert response.status_code == 401


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_current_user_invalid_token(client: AsyncClient):
    """不正なトークンでのユーザー情報取得テスト"""
    response = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Bearer invalid_token"}
    )

    assert response.status_code == 401
