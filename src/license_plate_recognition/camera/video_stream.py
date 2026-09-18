import logging
import threading
import time

import cv2

from ..config import Config

logger = logging.getLogger(__name__)


class VideoStream:

    def __init__(
            self,
            gate,
    ):

        # =========================
        # Gate
        # =========================

        self.gate = gate

        # =========================
        # Stream
        # =========================

        self.stream_url = f"rtsp://{gate.ip}/stream1"

        self.running = False

        self.cap = None

        self.frame = None

        # =========================
        # Threads
        # =========================

        self.thread = None

        self.lock = threading.Lock()

    def run(self):
        """
        啟動 Video Stream
        """

        if self.running:
            logger.warning(
                "Video Stream 已經啟動: %s - %s",
                self.gate.gate_id,
                self.gate.gate_name,
            )
            return

        self.running = True

        self.thread = threading.Thread(
            target=self._update,
            name=f"VideoStream-{self.gate.gate_id}",
            daemon=True,
        )

        self.thread.start()

        logger.info(
            "啟動 Video Stream: %s - %s",
            self.gate.gate_id,
            self.gate.gate_name,
        )

    def release(self):
        """
        停止 Video Stream
        """

        self.running = False

        current_thread = threading.current_thread()

        if (
                self.thread is not None
                and self.thread is not current_thread
        ):
            self.thread.join(timeout=2)

        self.thread = None

        logger.info(
            "Video Stream 已停止: %s - %s",
            self.gate.gate_id,
            self.gate.gate_name,
        )

    # =========================================================
    # Background Thread
    # =========================================================

    def _update(self):
        """
        持續讀取最新 Frame
        如果串流中斷，自動重新連線
        """

        try:
            while self.running:
                if self.cap is None:
                    connected = self.connect()

                    if not connected:
                        self._wait_before_reconnect()
                        continue

                ret, frame = self.cap.read()

                if not ret or frame is None:
                    logger.warning(
                        "Camera 讀取 Frame 失敗，準備重新連線: %s - %s",
                        self.gate.gate_id,
                        self.gate.gate_name,
                    )

                    self._release_capture()
                    self._wait_before_reconnect()

                    continue

                with self.lock:
                    self.frame = frame

        finally:
            self._release_capture()
            self.frame = None

    # =========================================================
    # Connection
    # =========================================================

    def connect(self):
        """
        建立 RTSP 連線
        """

        self._release_capture()

        cap = cv2.VideoCapture(
            self.stream_url,
            cv2.CAP_FFMPEG,
        )

        cap.set(
            cv2.CAP_PROP_HW_ACCELERATION,
            cv2.VIDEO_ACCELERATION_NONE,
        )

        if not cap.isOpened():
            cap.release()

            logger.error(
                "Camera 串流開啟失敗: %s - %s",
                self.gate.gate_id,
                self.gate.gate_name,
            )

            return False

        self.cap = cap

        logger.info(
            "Camera 串流連線成功: %s - %s",
            self.gate.gate_id,
            self.gate.gate_name,
        )

        return True

    def _wait_before_reconnect(self):
        """
        等待下一次重新連線
        """

        for _ in range(Config.RECONNECT_INTERVAL):
            if not self.running:
                return

            time.sleep(1)

    # =========================================================
    # Capture
    # =========================================================

    def _release_capture(self):
        """
        釋放 OpenCV VideoCapture
        """

        if self.cap is not None:
            self.cap.release()
            self.cap = None

    # =========================================================
    # Frame
    # =========================================================

    def read(self):
        """
        取得最新 Frame
        """

        with self.lock:
            if self.frame is None:
                return None

            return self.frame.copy()
