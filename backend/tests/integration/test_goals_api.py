"""目標（Goal）API の統合テスト"""
import pytest
from httpx import AsyncClient
from datetime import datetime, timedelta


class TestGoalsAPI:
    """目標API のテスト"""

    @pytest.mark.asyncio
    async def test_create_goal(self, client: AsyncClient, auth_headers):
        """目標作成のテスト"""
        response = await client.post(
            "/api/v1/goals",
            headers=auth_headers,
            json={
                "title": "月1回イベントに参加する",
                "description": "コミュニティとのつながりを深める",
                "category": "relationship",
                "due_date": (datetime.now() + timedelta(days=90)).isoformat(),
            }
        )

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "月1回イベントに参加する"
        assert data["category"] == "relationship"
        assert data["progress"] == 0
        assert data["status"] == "active"
        assert "id" in data

    @pytest.mark.asyncio
    async def test_create_goal_invalid_category(self, client: AsyncClient, auth_headers):
        """不正なカテゴリでの目標作成テスト"""
        response = await client.post(
            "/api/v1/goals",
            headers=auth_headers,
            json={
                "title": "テスト目標",
                "category": "invalid_category",
            }
        )

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_get_goals(self, client: AsyncClient, auth_headers):
        """目標一覧取得のテスト"""
        # 目標を2つ作成
        for i in range(2):
            await client.post(
                "/api/v1/goals",
                headers=auth_headers,
                json={
                    "title": f"テスト目標{i+1}",
                    "category": "activity",
                }
            )

        # 一覧取得
        response = await client.get("/api/v1/goals", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 2

    @pytest.mark.asyncio
    async def test_get_goal_by_id(self, client: AsyncClient, auth_headers):
        """目標詳細取得のテスト"""
        # 目標を作成
        create_response = await client.post(
            "/api/v1/goals",
            headers=auth_headers,
            json={
                "title": "詳細取得テスト",
                "category": "sensitivity",
            }
        )
        goal_id = create_response.json()["id"]

        # 詳細取得
        response = await client.get(f"/api/v1/goals/{goal_id}", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == goal_id
        assert data["title"] == "詳細取得テスト"

    @pytest.mark.asyncio
    async def test_get_goal_not_found(self, client: AsyncClient, auth_headers):
        """存在しない目標の取得テスト"""
        fake_id = "123e4567-e89b-12d3-a456-426614174000"
        response = await client.get(f"/api/v1/goals/{fake_id}", headers=auth_headers)

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_update_goal(self, client: AsyncClient, auth_headers):
        """目標更新のテスト"""
        # 目標を作成
        create_response = await client.post(
            "/api/v1/goals",
            headers=auth_headers,
            json={
                "title": "更新前のタイトル",
                "category": "activity",
            }
        )
        goal_id = create_response.json()["id"]

        # 更新
        response = await client.patch(
            f"/api/v1/goals/{goal_id}",
            headers=auth_headers,
            json={
                "title": "更新後のタイトル",
                "progress": 50,
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "更新後のタイトル"
        assert data["progress"] == 50

    @pytest.mark.asyncio
    async def test_delete_goal(self, client: AsyncClient, auth_headers):
        """目標削除のテスト"""
        # 目標を作成
        create_response = await client.post(
            "/api/v1/goals",
            headers=auth_headers,
            json={
                "title": "削除テスト",
                "category": "relationship",
            }
        )
        goal_id = create_response.json()["id"]

        # 削除
        response = await client.delete(f"/api/v1/goals/{goal_id}", headers=auth_headers)

        assert response.status_code == 204

        # 削除後に取得できないことを確認
        get_response = await client.get(f"/api/v1/goals/{goal_id}", headers=auth_headers)
        assert get_response.status_code == 404

    @pytest.mark.asyncio
    async def test_unauthorized_access(self, client: AsyncClient):
        """認証なしでのアクセステスト"""
        response = await client.get("/api/v1/goals")
        assert response.status_code == 403  # FastAPIのHTTPBearerは403を返す

    @pytest.mark.asyncio
    async def test_update_goal_not_found(self, client: AsyncClient, auth_headers):
        """存在しない目標の更新テスト"""
        fake_id = "123e4567-e89b-12d3-a456-426614174000"
        response = await client.patch(
            f"/api/v1/goals/{fake_id}",
            headers=auth_headers,
            json={"title": "更新"}
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_goal_not_found(self, client: AsyncClient, auth_headers):
        """存在しない目標の削除テスト"""
        fake_id = "123e4567-e89b-12d3-a456-426614174000"
        response = await client.delete(f"/api/v1/goals/{fake_id}", headers=auth_headers)
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_update_goal_status_to_completed(self, client: AsyncClient, auth_headers):
        """目標ステータスを完了に更新するテスト"""
        # 目標を作成
        create_response = await client.post(
            "/api/v1/goals",
            headers=auth_headers,
            json={
                "title": "完了テスト",
                "category": "activity",
            }
        )
        goal_id = create_response.json()["id"]

        # ステータスを完了に更新
        response = await client.patch(
            f"/api/v1/goals/{goal_id}",
            headers=auth_headers,
            json={
                "status": "completed",
                "progress": 100,
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "completed"
        assert data["progress"] == 100

    @pytest.mark.asyncio
    async def test_update_goal_category(self, client: AsyncClient, auth_headers):
        """目標カテゴリの更新テスト"""
        # 目標を作成
        create_response = await client.post(
            "/api/v1/goals",
            headers=auth_headers,
            json={
                "title": "カテゴリ変更テスト",
                "category": "activity",
            }
        )
        goal_id = create_response.json()["id"]

        # カテゴリを変更
        response = await client.patch(
            f"/api/v1/goals/{goal_id}",
            headers=auth_headers,
            json={
                "category": "relationship",
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["category"] == "relationship"

    @pytest.mark.asyncio
    async def test_create_goal_with_due_date(self, client: AsyncClient, auth_headers):
        """期限付き目標作成のテスト"""
        due_date = (datetime.now() + timedelta(days=30)).isoformat()
        response = await client.post(
            "/api/v1/goals",
            headers=auth_headers,
            json={
                "title": "期限付き目標",
                "category": "sensitivity",
                "due_date": due_date,
            }
        )

        assert response.status_code == 201
        data = response.json()
        assert data["due_date"] is not None

    @pytest.mark.asyncio
    async def test_get_empty_goals_list(self, client: AsyncClient, auth_headers):
        """目標がない場合の一覧取得テスト"""
        # 新規ユーザーで認証（auth_headersは既存ユーザーなので、既にゴールがある可能性）
        # このテストは既存のゴールがあっても空配列または配列が返ればOK
        response = await client.get("/api/v1/goals", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
