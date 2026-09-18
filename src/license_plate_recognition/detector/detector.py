from ultralytics import YOLO

from ..config import Config


class PlateDetector:
    # =========================
    # Vehicle Classes
    # =========================

    VEHICLE_CLASSES = {
        1,  # bicycle
        2,  # car
        3,  # motorcycle
        5,  # bus
        7,  # truck
    }

    def __init__(self):

        # =========================
        # Model
        # =========================

        self.vehicle_model = YOLO(Config.YOLO_MODEL_PATH)

        self.plate_model = YOLO(Config.LICENSE_PLATE_MODEL_PATH)

    def detect(self, image):
        """
        從原始影像中偵測車輛及車牌
        """

        plate_detections = []

        vehicle_detections = self._detect_vehicles(image)

        for vehicle in vehicle_detections:
            vehicle_bbox = vehicle["bbox"]

            vehicle_crop = self._crop(
                image,
                vehicle_bbox,
            )

            if vehicle_crop is None:
                continue

            detected_plates = self._detect_plates(vehicle_crop)

            for plate in detected_plates:
                plate_bbox = self._restore_bbox(
                    plate["bbox"],
                    vehicle_bbox,
                )

                plate_detections.append({
                    "bbox": plate_bbox,
                    "conf": plate["conf"],
                })

        return plate_detections

    # =========================================================
    # Detection
    # =========================================================

    def _detect_vehicles(self, image):
        """
        偵測原始影像中的車輛
        """

        results = self.vehicle_model(
            image,
            classes=list(self.VEHICLE_CLASSES),
            conf=Config.VEHICLE_CONFIDENCE,
            verbose=False,
        )

        vehicle_detections = []

        for result in results:
            for box in result.boxes:

                bbox = self._parse_bbox(box)

                if bbox is None:
                    continue

                conf = float(box.conf[0])
                cls = int(box.cls[0])

                vehicle_detections.append({
                    "bbox": bbox,
                    "conf": conf,
                    "cls": cls,
                    "name": self.vehicle_model.names[cls],
                })

        return vehicle_detections

    def _detect_plates(self, image):
        """
        偵測車輛 Crop 中的車牌
        """

        results = self.plate_model(
            image,
            verbose=False,
        )

        plate_detections = []

        for result in results:
            for box in result.boxes:

                bbox = self._parse_bbox(box)

                if bbox is None:
                    continue

                conf = float(box.conf[0])

                plate_detections.append({
                    "bbox": bbox,
                    "conf": conf,
                })

        return plate_detections

    # =========================================================
    # Bounding Box
    # =========================================================

    @staticmethod
    def _parse_bbox(box):
        """
        將 YOLO bbox 轉換成 int tuple
        """

        x1, y1, x2, y2 = map(
            int,
            box.xyxy[0],
        )

        return x1, y1, x2, y2

    @staticmethod
    def _crop(
            image,
            bbox,
    ):
        """
        根據 bbox 從影像中取出 Crop
        """

        x1, y1, x2, y2 = bbox

        height, width = image.shape[:2]

        x1 = max(0, min(x1, width))
        x2 = max(0, min(x2, width))

        y1 = max(0, min(y1, height))
        y2 = max(0, min(y2, height))

        if x1 >= x2 or y1 >= y2:
            return None

        return image[y1:y2, x1:x2]

    @staticmethod
    def _restore_bbox(
            bbox,
            parent_bbox,
    ):
        """
        將 Crop 座標轉回原始影像座標
        """

        x1, y1, x2, y2 = bbox

        px1, py1, _, _ = parent_bbox

        return (
            px1 + x1,
            py1 + y1,
            px1 + x2,
            py1 + y2,
        )
