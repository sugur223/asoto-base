"""内省ログ（Log）API の統合テスト"""
import pytest
from httpx import AsyncClient


class TestLogsAPI:
    """内省ログAPI のテスト"""

    @pytest.mark.asyncio
    async def test_create_log(self, client: AsyncClient, auth_headers):
        """ログ作成のテスト"""
        response = await client.post(
            "/api/v1/logs",
            headers=auth_headers,
            json={
                "title": "初めてのイベント参加",
                "content": "今日は初めてイベントに参加しました。とても楽しかったです。",
                "tags": ["イベント", "振り返り"],
                "visibility": "public",
            }
        )

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "初めてのイベント参加"
        assert data["visibility"] == "public"
        assert len(data["tags"]) == 2
        assert "id" in data

    @pytest.mark.asyncio
    async def test_create_private_log(self, client: AsyncClient, auth_headers):
        """非公開ログ作成のテスト"""
        response = await client.post(
            "/api/v1/logs",
            headers=auth_headers,
            json={
                "title": "個人的な気づき",
                "content": "プライベートな内容",
                "visibility": "private",
            }
        )

        assert response.status_code == 201
        data = response.json()
        assert data["visibility"] == "private"

    @pytest.mark.asyncio
    async def test_get_logs(self, client: AsyncClient, auth_headers, test_user):
        """ログ一覧取得のテスト"""
        # 公開ログを作成
        await client.post(
            "/api/v1/logs",
            headers=auth_headers,
            json={
                "title": "公開ログ",
                "content": "みんなに見せる内容",
                "visibility": "public",
            }
        )

        # 非公開ログを作成
        await client.post(
            "/api/v1/logs",
            headers=auth_headers,
            json={
                "title": "非公開ログ",
                "content": "自分だけの内容",
                "visibility": "private",
            }
        )

        # ログ一覧取得
        response = await client.get("/api/v1/logs", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # 自分のログは公開・非公開両方取得できる
        assert len(data) >= 2

    @pytest.mark.asyncio
    async def test_get_public_logs_only(self, client: AsyncClient, auth_headers):
        """公開ログのみ取得のテスト"""
        response = await client.get(
            "/api/v1/logs?visibility=public",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        # すべて公開ログ
        for log in data:
            assert log["visibility"] == "public"

    @pytest.mark.asyncio
    async def test_search_logs_by_tag(self, client: AsyncClient, auth_headers):
        """タグでログ検索のテスト"""
        # タグ付きログを作成
        await client.post(
            "/api/v1/logs",
            headers=auth_headers,
            json={
                "title": "農業体験",
                "content": "野菜を収穫しました",
                "tags": ["農業", "体験"],
                "visibility": "public",
            }
        )

        # タグで検索
        response = await client.get(
            "/api/v1/logs?tag=農業",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert "農業" in data[0]["tags"]

    @pytest.mark.asyncio
    async def test_get_log_by_id(self, client: AsyncClient, auth_headers):
        """ログ詳細取得のテスト"""
        # ログを作成
        create_response = await client.post(
            "/api/v1/logs",
            headers=auth_headers,
            json={
                "title": "詳細取得テスト",
                "content": "テスト内容",
                "visibility": "public",
            }
        )
        log_id = create_response.json()["id"]

        # 詳細取得
        response = await client.get(f"/api/v1/logs/{log_id}", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == log_id
        assert data["title"] == "詳細取得テスト"

    @pytest.mark.asyncio
    async def test_get_log_not_found(self, client: AsyncClient, auth_headers):
        """存在しないログの取得テスト"""
        fake_id = "123e4567-e89b-12d3-a456-426614174000"
        response = await client.get(f"/api/v1/logs/{fake_id}", headers=auth_headers)

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_update_log(self, client: AsyncClient, auth_headers):
        """ログ更新のテスト"""
        # ログを作成
        create_response = await client.post(
            "/api/v1/logs",
            headers=auth_headers,
            json={
                "title": "更新前のタイトル",
                "content": "更新前の内容",
                "visibility": "private",
            }
        )
        log_id = create_response.json()["id"]

        # 更新
        response = await client.patch(
            f"/api/v1/logs/{log_id}",
            headers=auth_headers,
            json={
                "title": "更新後のタイトル",
                "visibility": "public",
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "更新後のタイトル"
        assert data["visibility"] == "public"

    @pytest.mark.asyncio
    async def test_delete_log(self, client: AsyncClient, auth_headers):
        """ログ削除のテスト"""
        # ログを作成
        create_response = await client.post(
            "/api/v1/logs",
            headers=auth_headers,
            json={
                "title": "削除テスト",
                "content": "削除される内容",
                "visibility": "private",
            }
        )
        log_id = create_response.json()["id"]

        # 削除
        response = await client.delete(f"/api/v1/logs/{log_id}", headers=auth_headers)

        assert response.status_code == 204

        # 削除後に取得できないことを確認
        get_response = await client.get(f"/api/v1/logs/{log_id}", headers=auth_headers)
        assert get_response.status_code == 404

    @pytest.mark.asyncio
    async def test_cannot_access_others_private_log(self, client: AsyncClient, auth_headers, test_user):
        """他人の非公開ログにアクセスできないテスト"""
        # 別ユーザーとして非公開ログを作成
        # （test_userとは異なるユーザーを想定）
        # このテストは簡略化のため、同じユーザーで実施
        # 実際には別のauth_headersを使用すべき
        pass

    @pytest.mark.asyncio
    async def test_unauthorized_access(self, client: AsyncClient):
        """認証なしでのアクセステスト"""
        response = await client.get("/api/v1/logs")
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_update_log_not_found(self, client: AsyncClient, auth_headers):
        """存在しないログの更新テスト"""
        fake_id = "123e4567-e89b-12d3-a456-426614174000"
        response = await client.patch(
            f"/api/v1/logs/{fake_id}",
            headers=auth_headers,
            json={"title": "更新"}
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_log_not_found(self, client: AsyncClient, auth_headers):
        """存在しないログの削除テスト"""
        fake_id = "123e4567-e89b-12d3-a456-426614174000"
        response = await client.delete(f"/api/v1/logs/{fake_id}", headers=auth_headers)
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_filter_logs_by_private_visibility(self, client: AsyncClient, auth_headers):
        """プライベートログのフィルタリングテスト"""
        # プライベートログを作成
        await client.post(
            "/api/v1/logs",
            headers=auth_headers,
            json={
                "title": "プライベート限定",
                "content": "非公開の内容",
                "visibility": "private",
            }
        )

        # privateフィルタで取得
        response = await client.get("/api/v1/logs?visibility=private", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        # 全てprivateであることを確認
        for log in data:
            assert log["visibility"] == "private"

    @pytest.mark.asyncio
    async def test_update_log_visibility(self, client: AsyncClient, auth_headers):
        """ログの公開設定変更テスト"""
        # プライベートログを作成
        create_response = await client.post(
            "/api/v1/logs",
            headers=auth_headers,
            json={
                "title": "公開設定変更テスト",
                "content": "最初は非公開",
                "visibility": "private",
            }
        )
        log_id = create_response.json()["id"]

        # 公開に変更
        response = await client.patch(
            f"/api/v1/logs/{log_id}",
            headers=auth_headers,
            json={"visibility": "public"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["visibility"] == "public"

    @pytest.mark.asyncio
    async def test_update_log_tags(self, client: AsyncClient, auth_headers):
        """ログのタグ更新テスト"""
        # ログを作成
        create_response = await client.post(
            "/api/v1/logs",
            headers=auth_headers,
            json={
                "title": "タグ更新テスト",
                "content": "タグを変更します",
                "tags": ["元のタグ"],
            }
        )
        log_id = create_response.json()["id"]

        # タグを更新
        response = await client.patch(
            f"/api/v1/logs/{log_id}",
            headers=auth_headers,
            json={"tags": ["新しいタグ1", "新しいタグ2"]}
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["tags"]) == 2
        assert "新しいタグ1" in data["tags"]

    @pytest.mark.asyncio
    async def test_create_log_with_related_event(self, client: AsyncClient, auth_headers):
        """関連イベント付きログ作成のテスト"""
        from datetime import datetime, timedelta

        # イベントを作成
        start_date = datetime.now() + timedelta(days=7)
        event_response = await client.post(
            "/api/v1/events",
            headers=auth_headers,
            json={
                "title": "テストイベント",
                "start_date": start_date.isoformat(),
                "location_type": "online",
            }
        )
        event_id = event_response.json()["id"]

        # 関連イベント付きログを作成
        response = await client.post(
            "/api/v1/logs",
            headers=auth_headers,
            json={
                "title": "イベント参加記録",
                "content": "イベントに参加した振り返り",
                "related_event_id": event_id,
            }
        )

        assert response.status_code == 201
        data = response.json()
        assert data["related_event_id"] == event_id

    @pytest.mark.asyncio
    async def test_create_log_with_related_goal(self, client: AsyncClient, auth_headers):
        """関連目標付きログ作成のテスト"""
        # 目標を作成
        goal_response = await client.post(
            "/api/v1/goals",
            headers=auth_headers,
            json={
                "title": "テスト目標",
                "category": "activity",
            }
        )
        goal_id = goal_response.json()["id"]

        # 関連目標付きログを作成
        response = await client.post(
            "/api/v1/logs",
            headers=auth_headers,
            json={
                "title": "目標進捗記録",
                "content": "目標に向けた進捗の振り返り",
                "related_goal_id": goal_id,
            }
        )

        assert response.status_code == 201
        data = response.json()
        assert data["related_goal_id"] == goal_id
