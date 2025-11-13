"""ユーザープロフィール（UserProfile）API の統合テスト"""
import pytest
from httpx import AsyncClient


class TestUsersAPI:
    """ユーザープロフィールAPI のテスト"""

    @pytest.mark.asyncio
    async def test_get_my_profile(self, client: AsyncClient, auth_headers):
        """自分のプロフィール取得のテスト"""
        # まずプロフィールを作成
        create_response = await client.patch(
            "/api/v1/users/me/profile",
            headers=auth_headers,
            json={"bio": "テストユーザー"}
        )
        assert create_response.status_code == 200

        response = await client.get("/api/v1/users/me/profile", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert "user_id" in data
        assert data["bio"] == "テストユーザー"

    @pytest.mark.asyncio
    async def test_update_my_profile(self, client: AsyncClient, auth_headers):
        """プロフィール更新のテスト"""
        response = await client.patch(
            "/api/v1/users/me/profile",
            headers=auth_headers,
            json={
                "bio": "あそとを楽しんでいます！",
                "skills": ["Python", "FastAPI"],
                "interests": ["農業", "地域活動"]
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["bio"] == "あそとを楽しんでいます！"
        assert "Python" in data["skills"]
        assert "農業" in data["interests"]

    @pytest.mark.asyncio
    async def test_get_user_profile_by_id(self, client: AsyncClient, auth_headers, test_user):
        """他のユーザーのプロフィール取得のテスト"""
        # まず自分のプロフィールを更新
        await client.patch(
            "/api/v1/users/me/profile",
            headers=auth_headers,
            json={"bio": "テストユーザーです"}
        )

        # 自分のプロフィールをIDで取得
        response = await client.get(
            f"/api/v1/users/{test_user.id}/profile",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["bio"] == "テストユーザーです"

    @pytest.mark.asyncio
    async def test_update_profile_avatar(self, client: AsyncClient, auth_headers):
        """アバター画像URL更新のテスト"""
        response = await client.patch(
            "/api/v1/users/me/profile",
            headers=auth_headers,
            json={"avatar_url": "https://example.com/avatar.png"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["avatar_url"] == "https://example.com/avatar.png"

    @pytest.mark.asyncio
    async def test_update_profile_available_time(self, client: AsyncClient, auth_headers):
        """活動可能時間更新のテスト"""
        response = await client.patch(
            "/api/v1/users/me/profile",
            headers=auth_headers,
            json={"available_time": 600}  # 週10時間
        )

        assert response.status_code == 200
        data = response.json()
        assert data["available_time"] == 600

    @pytest.mark.asyncio
    async def test_get_profile_not_found(self, client: AsyncClient, auth_headers):
        """存在しないユーザーのプロフィール取得テスト"""
        fake_id = "123e4567-e89b-12d3-a456-426614174000"
        response = await client.get(
            f"/api/v1/users/{fake_id}/profile",
            headers=auth_headers
        )

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_unauthorized_access(self, client: AsyncClient):
        """認証なしでのアクセステスト"""
        response = await client.get("/api/v1/users/me/profile")
        assert response.status_code == 403
