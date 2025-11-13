"""ダッシュボード（Dashboard）API の統合テスト"""
import pytest
from httpx import AsyncClient
from datetime import datetime, timedelta


class TestDashboardAPI:
    """ダッシュボードAPI のテスト"""

    @pytest.mark.asyncio
    async def test_get_dashboard(self, client: AsyncClient, auth_headers):
        """ダッシュボード取得のテスト"""
        # テストデータを作成
        # 目標を作成
        await client.post(
            "/api/v1/goals",
            headers=auth_headers,
            json={
                "title": "テスト目標1",
                "category": "activity",
            }
        )

        # ログを作成
        await client.post(
            "/api/v1/logs",
            headers=auth_headers,
            json={
                "title": "テストログ1",
                "content": "ログの内容",
                "visibility": "public",
            }
        )

        # イベントを作成
        start_date = datetime.now() + timedelta(days=7)
        await client.post(
            "/api/v1/events",
            headers=auth_headers,
            json={
                "title": "テストイベント1",
                "start_date": start_date.isoformat(),
                "location_type": "online",
            }
        )

        # ダッシュボード取得
        response = await client.get("/api/v1/dashboard", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()

        # 個人エリアの確認
        assert "personal" in data
        assert "active_goals" in data["personal"]
        assert "recent_logs" in data["personal"]
        assert "total_points" in data["personal"]
        assert isinstance(data["personal"]["active_goals"], list)
        assert isinstance(data["personal"]["recent_logs"], list)
        assert isinstance(data["personal"]["total_points"], int)

        # コミュニティエリアの確認
        assert "community" in data
        assert "upcoming_events" in data["community"]
        assert "recent_public_logs" in data["community"]
        assert isinstance(data["community"]["upcoming_events"], list)
        assert isinstance(data["community"]["recent_public_logs"], list)

    @pytest.mark.asyncio
    async def test_dashboard_with_multiple_goals(self, client: AsyncClient, auth_headers):
        """複数の目標があるダッシュボードのテスト"""
        # 5つの目標を作成（ダッシュボードには最大3件表示）
        for i in range(5):
            await client.post(
                "/api/v1/goals",
                headers=auth_headers,
                json={
                    "title": f"目標{i+1}",
                    "category": "activity",
                }
            )

        response = await client.get("/api/v1/dashboard", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        # 最大3件まで表示
        assert len(data["personal"]["active_goals"]) <= 3

    @pytest.mark.asyncio
    async def test_dashboard_points_calculation(self, client: AsyncClient, auth_headers):
        """ポイント累計のテスト"""
        # ログを作成（5pt）
        await client.post(
            "/api/v1/logs",
            headers=auth_headers,
            json={
                "title": "ポイントテストログ",
                "content": "内容",
            }
        )

        # イベントを作成（50pt）
        start_date = datetime.now() + timedelta(days=7)
        await client.post(
            "/api/v1/events",
            headers=auth_headers,
            json={
                "title": "ポイントテストイベント",
                "start_date": start_date.isoformat(),
                "location_type": "online",
            }
        )

        response = await client.get("/api/v1/dashboard", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        # 5pt + 50pt = 55pt 以上（既存のポイントもある可能性があるため）
        assert data["personal"]["total_points"] >= 55

    @pytest.mark.asyncio
    async def test_dashboard_upcoming_events_only(self, client: AsyncClient, auth_headers):
        """今後のイベントのみ表示されるテスト"""
        # 過去のイベントを作成
        past_date = datetime.now() - timedelta(days=7)
        await client.post(
            "/api/v1/events",
            headers=auth_headers,
            json={
                "title": "過去のイベント",
                "start_date": past_date.isoformat(),
                "location_type": "online",
            }
        )

        # 未来のイベントを作成
        future_date = datetime.now() + timedelta(days=7)
        await client.post(
            "/api/v1/events",
            headers=auth_headers,
            json={
                "title": "未来のイベント",
                "start_date": future_date.isoformat(),
                "location_type": "online",
            }
        )

        response = await client.get("/api/v1/dashboard", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()

        # 今後のイベントのみが表示される
        for event in data["community"]["upcoming_events"]:
            event_start = datetime.fromisoformat(event["start_date"].replace('Z', '+00:00'))
            assert event_start >= datetime.now().replace(tzinfo=event_start.tzinfo)

    @pytest.mark.asyncio
    async def test_dashboard_public_logs_only(self, client: AsyncClient, auth_headers):
        """公開ログのみ表示されるテスト"""
        # プライベートログを作成
        await client.post(
            "/api/v1/logs",
            headers=auth_headers,
            json={
                "title": "プライベートログ",
                "content": "非公開",
                "visibility": "private",
            }
        )

        # 公開ログを作成
        await client.post(
            "/api/v1/logs",
            headers=auth_headers,
            json={
                "title": "公開ログ",
                "content": "公開",
                "visibility": "public",
            }
        )

        response = await client.get("/api/v1/dashboard", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()

        # コミュニティエリアの最近の公開ログは全てpublic
        for log in data["community"]["recent_public_logs"]:
            assert log["visibility"] == "public"

    @pytest.mark.asyncio
    async def test_dashboard_unauthorized(self, client: AsyncClient):
        """認証なしでのアクセステスト"""
        response = await client.get("/api/v1/dashboard")
        assert response.status_code == 403
