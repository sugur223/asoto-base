from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.security import verify_password, get_password_hash, create_access_token, decode_access_token
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, Token
router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    """現在のユーザーを取得（依存性注入用）"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="認証情報を検証できませんでした",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception

    return user


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="ユーザー登録",
    description="新しいユーザーアカウントを作成します。メールアドレスは一意である必要があります。",
    responses={
        201: {
            "description": "ユーザー登録成功",
            "content": {
                "application/json": {
                    "example": {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "email": "user@example.com",
                        "full_name": "山田太郎",
                        "is_active": True,
                        "created_at": "2025-11-13T10:00:00Z"
                    }
                }
            }
        },
        400: {"description": "メールアドレスが既に登録されています"},
        422: {"description": "入力データの検証エラー"}
    }
)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    """ユーザー登録"""
    # メールアドレス重複チェック
    result = await db.execute(select(User).filter(User.email == user_in.email))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="このメールアドレスは既に登録されています"
        )

    # ユーザー作成
    hashed_password = get_password_hash(user_in.password)
    user = User(
        email=user_in.email,
        full_name=user_in.full_name,
        hashed_password=hashed_password
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user


@router.post(
    "/login",
    response_model=Token,
    summary="ログイン",
    description="メールアドレスとパスワードでログインし、OAuth2形式のフォームデータを受け付けてJWTトークンを返します。",
    responses={
        200: {
            "description": "ログイン成功",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "token_type": "bearer"
                    }
                }
            }
        },
        401: {"description": "メールアドレスまたはパスワードが正しくありません"},
        400: {"description": "アカウントが無効です"}
    }
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """ログイン"""
    # FastAPIのOAuth2PasswordRequestFormはusernameフィールドを使用するため、emailを設定
    result = await db.execute(select(User).filter(User.email == form_data.username))
    user = result.scalar_one_or_none()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="メールアドレスまたはパスワードが正しくありません",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="このアカウントは無効です"
        )

    # JWTトークン生成
    access_token = create_access_token(data={"sub": str(user.id)})

    return {"access_token": access_token, "token_type": "bearer"}


@router.get(
    "/me",
    response_model=UserResponse,
    summary="現在のユーザー情報取得",
    description="JWTトークンを使用して、ログイン中のユーザー情報を取得します。",
    responses={
        200: {
            "description": "ユーザー情報取得成功",
            "content": {
                "application/json": {
                    "example": {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "email": "user@example.com",
                        "full_name": "山田太郎",
                        "is_active": True,
                        "created_at": "2025-11-13T10:00:00Z"
                    }
                }
            }
        },
        401: {"description": "認証が必要です"}
    }
)
async def get_me(current_user: User = Depends(get_current_user)):
    """現在のユーザー情報を取得"""
    return current_user
