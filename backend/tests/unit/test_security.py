"""セキュリティ関連の単体テスト"""
import pytest
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    decode_access_token
)


@pytest.mark.unit
def test_password_hashing():
    """パスワードハッシュ化のテスト"""
    password = "test_password_123"
    hashed = get_password_hash(password)

    # ハッシュ化されたパスワードは元のパスワードと異なる
    assert hashed != password

    # 正しいパスワードで検証成功
    assert verify_password(password, hashed) is True

    # 間違ったパスワードで検証失敗
    assert verify_password("wrong_password", hashed) is False


@pytest.mark.unit
def test_create_and_decode_token():
    """JWTトークン生成・検証のテスト"""
    user_id = "123e4567-e89b-12d3-a456-426614174000"
    token = create_access_token(data={"sub": user_id})

    # トークンが生成される
    assert token is not None
    assert isinstance(token, str)

    # トークンをデコードできる
    payload = decode_access_token(token)
    assert payload is not None
    assert payload.get("sub") == user_id


@pytest.mark.unit
def test_decode_invalid_token():
    """不正なトークンのテスト"""
    payload = decode_access_token("invalid_token_string")
    assert payload is None


@pytest.mark.unit
def test_token_expiration():
    """トークンに有効期限が含まれることを確認"""
    user_id = "test-user-id"
    token = create_access_token(data={"sub": user_id})
    payload = decode_access_token(token)

    assert payload is not None
    assert "exp" in payload
    assert "sub" in payload
    assert payload["sub"] == user_id
