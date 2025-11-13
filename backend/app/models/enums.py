"""共通のEnum定義"""
import enum


class LocationType(str, enum.Enum):
    """場所タイプ"""
    ONLINE = "online"  # オンライン
    OFFLINE = "offline"  # オフライン
    HYBRID = "hybrid"  # ハイブリッド
