import logging
import re
import threading
import time

from ..camera.video_stream import VideoStream
from ..config import settings
from ..detector.detector import PlateDetector
from ..ocr.ocr import OCR
from ..storage.image_storage import ImageStorage

logger = logging.getLogger(__name__)


class GateRunner:

    def __init__(
            self,
            gate,
    ):

        # =========================
        # Gate
        # =========================

        self.gate = gate

        # =========================
        # Components
        # =========================

        self.camera = VideoStream(gate)

        self.detector = PlateDetector()

        self.ocr = OCR()

        self.image_storage = ImageStorage()

        # =========================
        # Threads
        # =========================

        self.stop_event = threading.Event()

    def run(self):
        """
        啟動 Gate Runner
        """

        if self.stop_event.is_set():
            logger.warning(
                "Gate Runner 已經啟動: %s - %s",
                self.gate.gate_id,
                self.gate.gate_name,
            )
            return

        self.stop_event.set()

        try:
            self.camera.run()

            logger.info(
                "啟動 Camera: %s - %s",
                self.gate.gate_id,
                self.gate.gate_name,
            )

            while self.stop_event.is_set():
                start = time.monotonic()

                try:
                    frame = self.camera.read()

                    if frame is not None:
                        self.process_frame(frame)

                except Exception:
                    logger.exception(
                        "Frame 處理發生錯誤: %s - %s",
                        self.gate.gate_id,
                        self.gate.gate_name,
                    )

                elapsed = time.monotonic() - start
                remaining = settings.frame_interval - elapsed

                if remaining > 0:
                    self.stop_event.wait(remaining)

        except Exception:
            logger.exception(
                "Gate 發生未預期錯誤: %s - %s",
                self.gate.gate_id,
                self.gate.gate_name,
            )

            raise

        finally:
            self.camera.release()

    def release(self):
        """
        停止 Gate Runner
        """

        self.stop_event.clear()

        self.camera.release()

        logger.info(
            "Gate Runner 已停止: %s - %s",
            self.gate.gate_id,
            self.gate.gate_name,
        )

    # =========================================================
    # Frame
    # =========================================================

    def process_frame(self, frame):
        """
        處理單一 Frame
        """

        detections = self.detector.detect(frame)

        for detection in detections:
            try:
                x1, y1, x2, y2 = detection["bbox"]
                plate_crop = frame[y1:y2, x1:x2]
                result = self.ocr.recognize(plate_crop)

                if not result:
                    continue

                plate_number = re.sub(
                    r"[^A-Za-z0-9]",
                    "",
                    result["plate"],
                )

                confidence = result["confidence"]

                image_path = self.image_storage.save(
                    frame,
                    self.gate.gate_id,
                    plate_number,
                )

                logger.info(
                    "車牌辨識成功: %s - %s "
                    "plate_number=%s, score=%s, image_path=%s",
                    self.gate.gate_id,
                    self.gate.gate_name,
                    plate_number,
                    confidence,
                    image_path,
                )

            except Exception:
                logger.exception(
                    "車牌處理發生錯誤: %s - %s",
                    self.gate.gate_id,
                    self.gate.gate_name,
                )
