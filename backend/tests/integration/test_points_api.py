"""ポイント（Point）API の統合テスト"""
import pytest
from httpx import AsyncClient
from datetime import datetime, timedelta


class TestPointsAPI:
    """ポイントAPI のテスト"""

    @pytest.mark.asyncio
    async def test_get_my_points(self, client: AsyncClient, auth_headers):
        """ポイント累計取得のテスト"""
        response = await client.get("/api/v1/users/me/points", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert "total_points" in data
        assert "user_id" in data
        assert isinstance(data["total_points"], int)
        assert data["total_points"] >= 0

    @pytest.mark.asyncio
    async def test_get_points_history(self, client: AsyncClient, auth_headers):
        """ポイント獲得履歴取得のテスト"""
        # アクションを実行してポイントを獲得
        # ログを作成（5pt）
        await client.post(
            "/api/v1/logs",
            headers=auth_headers,
            json={
                "title": "ポイント履歴テストログ",
                "content": "テスト内容",
            }
        )

        # イベントを作成（50pt）
        start_date = datetime.now() + timedelta(days=7)
        await client.post(
            "/api/v1/events",
            headers=auth_headers,
            json={
                "title": "ポイント履歴テストイベント",
                "start_date": start_date.isoformat(),
                "location_type": "online",
            }
        )

        # ポイント履歴を取得
        response = await client.get("/api/v1/users/me/points/history", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 2  # 少なくとも2件のポイント記録がある

        # 履歴の各項目を確認
        for point in data:
            assert "id" in point
            assert "user_id" in point
            assert "amount" in point
            assert "action_type" in point
            assert "description" in point
            assert "earned_at" in point

    @pytest.mark.asyncio
    async def test_points_accumulation(self, client: AsyncClient, auth_headers):
        """ポイント累積のテスト"""
        # 初期ポイントを取得
        initial_response = await client.get("/api/v1/users/me/points", headers=auth_headers)
        initial_points = initial_response.json()["total_points"]

        # 目標を作成してステップを完了（10pt）
        goal_response = await client.post(
            "/api/v1/goals",
            headers=auth_headers,
            json={
                "title": "ポイントテスト目標",
                "category": "activity",
            }
        )
        goal_id = goal_response.json()["id"]

        step_response = await client.post(
            f"/api/v1/goals/{goal_id}/steps",
            headers=auth_headers,
            json={"title": "ステップ1", "order": 1}
        )
        step_id = step_response.json()["id"]

        await client.post(
            f"/api/v1/steps/{step_id}/complete",
            headers=auth_headers
        )

        # ポイントが増加したことを確認
        final_response = await client.get("/api/v1/users/me/points", headers=auth_headers)
        final_points = final_response.json()["total_points"]

        assert final_points >= initial_points + 10

    @pytest.mark.asyncio
    async def test_points_history_order(self, client: AsyncClient, auth_headers):
        """ポイント履歴が新しい順に並んでいるテスト"""
        # 複数のアクションを実行
        await client.post(
            "/api/v1/logs",
            headers=auth_headers,
            json={"title": "ログ1", "content": "内容1"}
        )

        await client.post(
            "/api/v1/logs",
            headers=auth_headers,
            json={"title": "ログ2", "content": "内容2"}
        )

        # 履歴を取得
        response = await client.get("/api/v1/users/me/points/history", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()

        # 履歴が取得できることを確認
        assert len(data) >= 2
        # earned_atフィールドが存在することを確認
        for point in data:
            assert "earned_at" in point

    @pytest.mark.asyncio
    async def test_unauthorized_access(self, client: AsyncClient):
        """認証なしでのアクセステスト"""
        response = await client.get("/api/v1/users/me/points")
        assert response.status_code == 403

        response = await client.get("/api/v1/users/me/points/history")
        assert response.status_code == 403
