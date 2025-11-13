"""ステップ（Step）API の統合テスト"""
import pytest
from httpx import AsyncClient


class TestStepsAPI:
    """ステップAPI のテスト"""

    @pytest.mark.asyncio
    async def test_create_step(self, client: AsyncClient, auth_headers):
        """ステップ作成のテスト"""
        # まず目標を作成
        goal_response = await client.post(
            "/api/v1/goals",
            headers=auth_headers,
            json={
                "title": "テスト目標",
                "category": "activity",
            }
        )
        goal_id = goal_response.json()["id"]

        # ステップを作成
        response = await client.post(
            f"/api/v1/goals/{goal_id}/steps",
            headers=auth_headers,
            json={
                "title": "ステップ1",
                "description": "最初のステップ",
                "order": 1,
                "estimated_minutes": 30,
            }
        )

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "ステップ1"
        assert data["order"] == 1
        assert data["status"] == "pending"
        assert data["goal_id"] == goal_id

    @pytest.mark.asyncio
    async def test_update_step(self, client: AsyncClient, auth_headers):
        """ステップ更新のテスト"""
        # 目標とステップを作成
        goal_response = await client.post(
            "/api/v1/goals",
            headers=auth_headers,
            json={"title": "テスト目標", "category": "activity"}
        )
        goal_id = goal_response.json()["id"]

        step_response = await client.post(
            f"/api/v1/goals/{goal_id}/steps",
            headers=auth_headers,
            json={"title": "更新前", "order": 1}
        )
        step_id = step_response.json()["id"]

        # ステップを更新
        response = await client.patch(
            f"/api/v1/steps/{step_id}",
            headers=auth_headers,
            json={
                "title": "更新後",
                "status": "in_progress",
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "更新後"
        assert data["status"] == "in_progress"

    @pytest.mark.asyncio
    async def test_complete_step(self, client: AsyncClient, auth_headers):
        """ステップ完了のテスト"""
        # 目標とステップを作成
        goal_response = await client.post(
            "/api/v1/goals",
            headers=auth_headers,
            json={"title": "テスト目標", "category": "activity"}
        )
        goal_id = goal_response.json()["id"]

        step_response = await client.post(
            f"/api/v1/goals/{goal_id}/steps",
            headers=auth_headers,
            json={"title": "完了テスト", "order": 1}
        )
        step_id = step_response.json()["id"]

        # ステップを完了
        response = await client.post(
            f"/api/v1/steps/{step_id}/complete",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "completed"
        assert data["completed_at"] is not None

        # ポイントが付与されていることを確認（10pt）
        # TODO: ポイントAPIが実装されたらテスト追加

    @pytest.mark.asyncio
    async def test_delete_step(self, client: AsyncClient, auth_headers):
        """ステップ削除のテスト"""
        # 目標とステップを作成
        goal_response = await client.post(
            "/api/v1/goals",
            headers=auth_headers,
            json={"title": "テスト目標", "category": "activity"}
        )
        goal_id = goal_response.json()["id"]

        step_response = await client.post(
            f"/api/v1/goals/{goal_id}/steps",
            headers=auth_headers,
            json={"title": "削除テスト", "order": 1}
        )
        step_id = step_response.json()["id"]

        # ステップを削除
        response = await client.delete(
            f"/api/v1/steps/{step_id}",
            headers=auth_headers
        )

        assert response.status_code == 204

    @pytest.mark.asyncio
    async def test_step_not_found(self, client: AsyncClient, auth_headers):
        """存在しないステップの操作テスト"""
        fake_id = "123e4567-e89b-12d3-a456-426614174000"

        response = await client.patch(
            f"/api/v1/steps/{fake_id}",
            headers=auth_headers,
            json={"title": "更新"}
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_create_step_goal_not_found(self, client: AsyncClient, auth_headers):
        """存在しない目標にステップを作成するテスト"""
        fake_goal_id = "123e4567-e89b-12d3-a456-426614174000"
        response = await client.post(
            f"/api/v1/goals/{fake_goal_id}/steps",
            headers=auth_headers,
            json={"title": "ステップ", "order": 1}
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_complete_step_not_found(self, client: AsyncClient, auth_headers):
        """存在しないステップの完了テスト"""
        fake_id = "123e4567-e89b-12d3-a456-426614174000"
        response = await client.post(
            f"/api/v1/steps/{fake_id}/complete",
            headers=auth_headers
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_step_not_found(self, client: AsyncClient, auth_headers):
        """存在しないステップの削除テスト"""
        fake_id = "123e4567-e89b-12d3-a456-426614174000"
        response = await client.delete(
            f"/api/v1/steps/{fake_id}",
            headers=auth_headers
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_update_step_order(self, client: AsyncClient, auth_headers):
        """ステップの順序更新テスト"""
        # 目標とステップを作成
        goal_response = await client.post(
            "/api/v1/goals",
            headers=auth_headers,
            json={"title": "テスト目標", "category": "activity"}
        )
        goal_id = goal_response.json()["id"]

        step_response = await client.post(
            f"/api/v1/goals/{goal_id}/steps",
            headers=auth_headers,
            json={"title": "ステップ1", "order": 1}
        )
        step_id = step_response.json()["id"]

        # 順序を変更
        response = await client.patch(
            f"/api/v1/steps/{step_id}",
            headers=auth_headers,
            json={"order": 2}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["order"] == 2

    @pytest.mark.asyncio
    async def test_create_step_with_due_date(self, client: AsyncClient, auth_headers):
        """期限付きステップ作成のテスト"""
        from datetime import datetime, timedelta

        goal_response = await client.post(
            "/api/v1/goals",
            headers=auth_headers,
            json={"title": "テスト目標", "category": "activity"}
        )
        goal_id = goal_response.json()["id"]

        due_date = (datetime.now() + timedelta(days=7)).isoformat()
        response = await client.post(
            f"/api/v1/goals/{goal_id}/steps",
            headers=auth_headers,
            json={
                "title": "期限付きステップ",
                "order": 1,
                "due_date": due_date,
            }
        )

        assert response.status_code == 201
        data = response.json()
        assert data["due_date"] is not None

    @pytest.mark.asyncio
    async def test_update_step_description(self, client: AsyncClient, auth_headers):
        """ステップの説明更新テスト"""
        # 目標とステップを作成
        goal_response = await client.post(
            "/api/v1/goals",
            headers=auth_headers,
            json={"title": "テスト目標", "category": "activity"}
        )
        goal_id = goal_response.json()["id"]

        step_response = await client.post(
            f"/api/v1/goals/{goal_id}/steps",
            headers=auth_headers,
            json={"title": "ステップ", "order": 1, "description": "元の説明"}
        )
        step_id = step_response.json()["id"]

        # 説明を更新
        response = await client.patch(
            f"/api/v1/steps/{step_id}",
            headers=auth_headers,
            json={"description": "新しい説明"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["description"] == "新しい説明"
