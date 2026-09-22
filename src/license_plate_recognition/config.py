from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# 專案根目錄
BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    # =========================
    # Pydantic Settings
    # =========================

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
    )

    # =========================
    # Application
    # =========================

    debug: bool = False

    # =========================
    # Database
    # =========================

    db_host: str = ""
    db_port: int = 1433
    db_name: str = ""
    db_user: str = ""
    db_password: str = ""

    # =========================
    # Branch
    # =========================

    branch_id: str = ""

    # =========================
    # Gate
    # =========================

    gates: list[str] = Field(default_factory=list)

    # =========================
    # Reconnect Interval
    # =========================

    reconnect_interval: float = 5.0

    # =========================
    # Frame Interval
    # =========================

    frame_interval: float = 1.0

    # =========================
    # Vehicle Confidence
    # =========================

    vehicle_confidence: float = 0.5

    # =========================
    # PaddleOCR
    # =========================

    ocr_detection_model: str = "PP-OCRv5_server_det"

    ocr_recognition_model: str = "PP-OCRv5_server_rec"

    # =========================
    # Model
    # =========================

    model_dir: Path = BASE_DIR / "models"

    yolo_model_path: Path = model_dir / "yolo26n.pt"

    license_plate_model_path: Path = model_dir / "license_plate.pt"

    # =========================
    # Storage
    # =========================

    data_dir: Path = BASE_DIR / "data"

    recognition_image_dir: Path = data_dir / "recognition"

    # =========================
    # Log
    # =========================

    log_path: Path = BASE_DIR / "logs" / "app.log"


settings = Settings()
