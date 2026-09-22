from datetime import datetime
from pathlib import Path

import cv2

from ..config import settings


class ImageStorage:

    def __init__(
            self,
            base_dir: Path | None = None,
    ):

        # =========================
        # Base Directory
        # =========================

        self.base_dir = (
                base_dir
                or settings.recognition_image_dir
        )

    def save(
            self,
            image,
            gate_id: str,
            plate_number: str | None = None,
            timestamp: datetime | None = None,
    ) -> Path:
        """
        儲存辨識圖片
        """

        if timestamp is None:
            timestamp = datetime.now()

        output_dir = (
                self.base_dir
                / timestamp.strftime("%Y")
                / timestamp.strftime("%m")
                / timestamp.strftime("%d")
                / gate_id
        )

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S_%f")

        if plate_number:
            safe_plate_number = self._sanitize_filename(plate_number)

            filename = (
                f"{timestamp_str}"
                f"_{safe_plate_number}.jpg"
            )

        else:
            filename = f"{timestamp_str}.jpg"

        output_path = output_dir / filename

        success = cv2.imwrite(
            str(output_path),
            image,
        )

        if not success:
            raise IOError(
                f"圖片儲存失敗: path=%s"
                f"{output_path}"
            )

        return output_path

    @staticmethod
    def _sanitize_filename(
            value: str,
    ) -> str:
        """
        清理不能出現在檔名中的字元
        """

        invalid_chars = '<>:"/\\|?*'

        for char in invalid_chars:
            value = value.replace(
                char,
                "_",
            )

        return value.strip()
