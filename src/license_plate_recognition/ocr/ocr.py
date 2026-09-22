import logging

from paddleocr import PaddleOCR

from ..config import settings

logger = logging.getLogger(__name__)


class OCR:

    def __init__(self):

        # =========================
        # OCR Model
        # =========================

        self.ocr = PaddleOCR(
            text_detection_model_name=settings.ocr_detection_model,
            text_recognition_model_name=settings.ocr_recognition_model,
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False,
            enable_mkldnn=False,
        )

    def recognize(self, image):
        """
        辨識車牌影像中的文字
        """

        results = self.ocr.predict(image)

        return self._parse_result(results)

    @staticmethod
    def _parse_result(results):
        """
        解析 PaddleOCR 結果
        """

        if not results:
            return None

        result = results[0]
        rec_texts = result.get("rec_texts", [])
        rec_scores = result.get("rec_scores", [])

        if not rec_texts:
            return None

        plate_text = rec_texts[0]
        confidence = float(rec_scores[0]) if rec_scores else 0.0

        if not plate_text:
            return None

        return {
            "plate": plate_text,
            "confidence": confidence,
        }
