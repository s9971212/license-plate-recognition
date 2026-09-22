import logging
import threading

import cv2

from ..config import settings

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

        self.cap = None

        self.frame = None

        # =========================
        # Threads
        # =========================

        self.thread = None

        self.stop_event = threading.Event()

        self.lock = threading.Lock()

    def run(self):
        """
        啟動 Video Stream
        """

        if self.stop_event.is_set():
            logger.warning(
                "Video Stream 已經啟動: %s - %s",
                self.gate.gate_id,
                self.gate.gate_name,
            )
            return

        self.stop_event.set()

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

        self.stop_event.clear()

        current_thread = threading.current_thread()

        if (
                self.thread is not None
                and self.thread is not current_thread
        ):
            self.thread.join(timeout=2)

        self.thread = None

        self._release_capture()

        with self.lock:
            self.frame = None

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
            while self.stop_event.is_set():
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

            with self.lock:
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

        self.stop_event.wait(
            timeout=settings.reconnect_interval
        )

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
