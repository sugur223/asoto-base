"""イベント（Event）API の統合テスト"""
import pytest
from httpx import AsyncClient
from datetime import datetime, timedelta


class TestEventsAPI:
    """イベントAPI のテスト"""

    @pytest.mark.asyncio
    async def test_create_event(self, client: AsyncClient, auth_headers):
        """イベント作成のテスト"""
        start_date = datetime.now() + timedelta(days=7)
        end_date = start_date + timedelta(hours=3)

        response = await client.post(
            "/api/v1/events",
            headers=auth_headers,
            json={
                "title": "週末農業体験",
                "description": "野菜の収穫を体験します",
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "location_type": "offline",
                "location_detail": "千葉県の農園",
                "max_attendees": 15,
                "tags": ["農業", "体験"],
            }
        )

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "週末農業体験"
        assert data["location_type"] == "offline"
        assert data["status"] == "upcoming"
        assert "id" in data

    @pytest.mark.asyncio
    async def test_create_online_event(self, client: AsyncClient, auth_headers):
        """オンラインイベント作成のテスト"""
        start_date = datetime.now() + timedelta(days=3)

        response = await client.post(
            "/api/v1/events",
            headers=auth_headers,
            json={
                "title": "オンライン読書会",
                "description": "Zoomで実施",
                "start_date": start_date.isoformat(),
                "location_type": "online",
                "location_detail": "Zoom",
                "max_attendees": 10,
                "tags": ["読書", "オンライン"],
            }
        )

        assert response.status_code == 201
        data = response.json()
        assert data["location_type"] == "online"

    @pytest.mark.asyncio
    async def test_get_events(self, client: AsyncClient, auth_headers):
        """イベント一覧取得のテスト"""
        # イベントを2つ作成
        start_date = datetime.now() + timedelta(days=7)
        for i in range(2):
            await client.post(
                "/api/v1/events",
                headers=auth_headers,
                json={
                    "title": f"テストイベント{i+1}",
                    "start_date": start_date.isoformat(),
                    "location_type": "online",
                }
            )

        # 一覧取得
        response = await client.get("/api/v1/events", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 2

    @pytest.mark.asyncio
    async def test_get_event_by_id(self, client: AsyncClient, auth_headers):
        """イベント詳細取得のテスト"""
        # イベントを作成
        start_date = datetime.now() + timedelta(days=7)
        create_response = await client.post(
            "/api/v1/events",
            headers=auth_headers,
            json={
                "title": "詳細取得テスト",
                "start_date": start_date.isoformat(),
                "location_type": "offline",
            }
        )
        event_id = create_response.json()["id"]

        # 詳細取得
        response = await client.get(f"/api/v1/events/{event_id}", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == event_id
        assert data["title"] == "詳細取得テスト"

    @pytest.mark.asyncio
    async def test_update_event(self, client: AsyncClient, auth_headers):
        """イベント更新のテスト"""
        # イベントを作成
        start_date = datetime.now() + timedelta(days=7)
        create_response = await client.post(
            "/api/v1/events",
            headers=auth_headers,
            json={
                "title": "更新前のタイトル",
                "start_date": start_date.isoformat(),
                "location_type": "online",
            }
        )
        event_id = create_response.json()["id"]

        # 更新
        response = await client.patch(
            f"/api/v1/events/{event_id}",
            headers=auth_headers,
            json={
                "title": "更新後のタイトル",
                "max_attendees": 20,
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "更新後のタイトル"
        assert data["max_attendees"] == 20

    @pytest.mark.asyncio
    async def test_delete_event(self, client: AsyncClient, auth_headers):
        """イベント削除のテスト"""
        # イベントを作成
        start_date = datetime.now() + timedelta(days=7)
        create_response = await client.post(
            "/api/v1/events",
            headers=auth_headers,
            json={
                "title": "削除テスト",
                "start_date": start_date.isoformat(),
                "location_type": "online",
            }
        )
        event_id = create_response.json()["id"]

        # 削除
        response = await client.delete(f"/api/v1/events/{event_id}", headers=auth_headers)

        assert response.status_code == 204

        # 削除後に取得できないことを確認
        get_response = await client.get(f"/api/v1/events/{event_id}", headers=auth_headers)
        assert get_response.status_code == 404

    @pytest.mark.asyncio
    async def test_join_event(self, client: AsyncClient, auth_headers):
        """イベント参加のテスト"""
        # イベントを作成
        start_date = datetime.now() + timedelta(days=7)
        create_response = await client.post(
            "/api/v1/events",
            headers=auth_headers,
            json={
                "title": "参加テスト",
                "start_date": start_date.isoformat(),
                "location_type": "online",
                "max_attendees": 10,
            }
        )
        event_id = create_response.json()["id"]

        # イベントに参加
        response = await client.post(
            f"/api/v1/events/{event_id}/join",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "joined"

    @pytest.mark.asyncio
    async def test_join_event_twice(self, client: AsyncClient, auth_headers):
        """同じイベントに2回参加できないテスト"""
        # イベントを作成
        start_date = datetime.now() + timedelta(days=7)
        create_response = await client.post(
            "/api/v1/events",
            headers=auth_headers,
            json={
                "title": "重複参加テスト",
                "start_date": start_date.isoformat(),
                "location_type": "online",
            }
        )
        event_id = create_response.json()["id"]

        # 1回目の参加
        await client.post(f"/api/v1/events/{event_id}/join", headers=auth_headers)

        # 2回目の参加（エラーになるはず）
        response = await client.post(
            f"/api/v1/events/{event_id}/join",
            headers=auth_headers
        )

        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_leave_event(self, client: AsyncClient, auth_headers):
        """イベント離脱のテスト"""
        # イベントを作成
        start_date = datetime.now() + timedelta(days=7)
        create_response = await client.post(
            "/api/v1/events",
            headers=auth_headers,
            json={
                "title": "離脱テスト",
                "start_date": start_date.isoformat(),
                "location_type": "online",
            }
        )
        event_id = create_response.json()["id"]

        # 参加
        await client.post(f"/api/v1/events/{event_id}/join", headers=auth_headers)

        # 離脱
        response = await client.delete(
            f"/api/v1/events/{event_id}/leave",
            headers=auth_headers
        )

        assert response.status_code == 204

    @pytest.mark.asyncio
    async def test_get_participants(self, client: AsyncClient, auth_headers):
        """参加者一覧取得のテスト"""
        # イベントを作成
        start_date = datetime.now() + timedelta(days=7)
        create_response = await client.post(
            "/api/v1/events",
            headers=auth_headers,
            json={
                "title": "参加者一覧テスト",
                "start_date": start_date.isoformat(),
                "location_type": "online",
            }
        )
        event_id = create_response.json()["id"]

        # 参加
        await client.post(f"/api/v1/events/{event_id}/join", headers=auth_headers)

        # 参加者一覧取得
        response = await client.get(
            f"/api/v1/events/{event_id}/participants",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    @pytest.mark.asyncio
    async def test_event_not_found(self, client: AsyncClient, auth_headers):
        """存在しないイベントの取得テスト"""
        fake_id = "123e4567-e89b-12d3-a456-426614174000"
        response = await client.get(f"/api/v1/events/{fake_id}", headers=auth_headers)

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_unauthorized_access(self, client: AsyncClient):
        """認証なしでのアクセステスト"""
        response = await client.get("/api/v1/events")
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_update_event_not_found(self, client: AsyncClient, auth_headers):
        """存在しないイベントの更新テスト"""
        fake_id = "123e4567-e89b-12d3-a456-426614174000"
        response = await client.patch(
            f"/api/v1/events/{fake_id}",
            headers=auth_headers,
            json={"title": "更新"}
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_event_not_found(self, client: AsyncClient, auth_headers):
        """存在しないイベントの削除テスト"""
        fake_id = "123e4567-e89b-12d3-a456-426614174000"
        response = await client.delete(f"/api/v1/events/{fake_id}", headers=auth_headers)
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_join_event_not_found(self, client: AsyncClient, auth_headers):
        """存在しないイベントへの参加テスト"""
        fake_id = "123e4567-e89b-12d3-a456-426614174000"
        response = await client.post(
            f"/api/v1/events/{fake_id}/join",
            headers=auth_headers
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_leave_event_not_found(self, client: AsyncClient, auth_headers):
        """存在しない参加記録の離脱テスト"""
        fake_id = "123e4567-e89b-12d3-a456-426614174000"
        response = await client.delete(
            f"/api/v1/events/{fake_id}/leave",
            headers=auth_headers
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_get_participants_event_not_found(self, client: AsyncClient, auth_headers):
        """存在しないイベントの参加者一覧取得テスト"""
        fake_id = "123e4567-e89b-12d3-a456-426614174000"
        response = await client.get(
            f"/api/v1/events/{fake_id}/participants",
            headers=auth_headers
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_create_hybrid_event(self, client: AsyncClient, auth_headers):
        """ハイブリッドイベント作成のテスト"""
        start_date = datetime.now() + timedelta(days=5)

        response = await client.post(
            "/api/v1/events",
            headers=auth_headers,
            json={
                "title": "ハイブリッド交流会",
                "description": "オンラインとオフライン両方で参加可能",
                "start_date": start_date.isoformat(),
                "location_type": "hybrid",
                "location_detail": "渋谷 + Zoom",
                "max_attendees": 30,
            }
        )

        assert response.status_code == 201
        data = response.json()
        assert data["location_type"] == "hybrid"

    @pytest.mark.asyncio
    async def test_update_event_max_attendees(self, client: AsyncClient, auth_headers):
        """イベント定員の更新テスト"""
        start_date = datetime.now() + timedelta(days=7)
        create_response = await client.post(
            "/api/v1/events",
            headers=auth_headers,
            json={
                "title": "定員変更テスト",
                "start_date": start_date.isoformat(),
                "location_type": "online",
                "max_attendees": 10,
            }
        )
        event_id = create_response.json()["id"]

        # 定員を変更
        response = await client.patch(
            f"/api/v1/events/{event_id}",
            headers=auth_headers,
            json={"max_attendees": 20}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["max_attendees"] == 20
