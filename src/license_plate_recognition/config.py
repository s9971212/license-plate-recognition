import os
from pathlib import Path

from dotenv import load_dotenv

# 專案根目錄
BASE_DIR = Path(__file__).resolve().parents[2]

# 載入 .env
ENV_FILE = BASE_DIR / ".env"

load_dotenv(
    dotenv_path=ENV_FILE,
    override=True
)


class Config:
    # =========================
    # Application
    # =========================

    DEBUG = os.getenv("DEBUG", "false").lower() == "true"

    # =========================
    # Database
    # =========================

    DB_HOST = os.getenv("DB_HOST", "")
    DB_PORT = int(os.getenv("DB_PORT", "1433"))
    DB_NAME = os.getenv("DB_NAME", "")
    DB_USER = os.getenv("DB_USER", "")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")

    # =========================
    # Branch
    # =========================

    BRANCH_ID = os.getenv("BRANCH_ID", "")

    # =========================
    # Gate
    # =========================

    GATES = [
        gate.strip()
        for gate in os.getenv("GATES", "").split(",")
        if gate.strip()
    ]

    # =========================
    # Reconnect Interval
    # =========================

    RECONNECT_INTERVAL = float(os.getenv("RECONNECT_INTERVAL", "5.0"))

    # =========================
    # Frame Interval
    # =========================

    FRAME_INTERVAL = float(os.getenv("FRAME_INTERVAL", "1.0"))

    # =========================
    # Vehicle Confidence
    # =========================

    VEHICLE_CONFIDENCE = float(os.getenv("VEHICLE_CONFIDENCE", "0.5"))

    # =========================
    # PaddleOCR
    # =========================

    OCR_DETECTION_MODEL = "PP-OCRv5_server_det"

    OCR_RECOGNITION_MODEL = "PP-OCRv5_server_rec"

    # =========================
    # Model
    # =========================

    MODEL_DIR = BASE_DIR / "models"

    YOLO_MODEL_PATH = MODEL_DIR / "yolo26n.pt"

    LICENSE_PLATE_MODEL_PATH = MODEL_DIR / "license_plate.pt"

    # =========================
    # Storage
    # =========================

    DATA_DIR = BASE_DIR / "data"

    RECOGNITION_IMAGE_DIR = DATA_DIR / "recognition"

    # =========================
    # Log
    # =========================

    LOG_PATH = BASE_DIR / "logs" / "app.log"
