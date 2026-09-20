from unittest.mock import MagicMock

import cv2

from license_plate_recognition.gate.gate_runner import GateRunner


# =========================================================
# Ignore Video Stream
# =========================================================

def test_process_frame_with_plate():
    """
    測試: 有偵測出車牌
    """

    frame = load_test_image()
    runner = create_runner()
    runner = create_mock_runner(runner)

    runner.detector.detect.return_value = [
        {
            "bbox": [100, 100, 300, 180]
        }
    ]

    runner.ocr.recognize.return_value = {
        "plate": "ABC-1234",
        "confidence": 0.95,
    }

    runner.image_storage.save.return_value = (
        "tests/output/ABC1234.jpg"
    )

    runner.process_frame(frame)

    runner.detector.detect.assert_called_once_with(frame)

    runner.ocr.recognize.assert_called_once()

    runner.image_storage.save.assert_called_once_with(
        frame,
        "TEST",
        "ABC1234",
    )


def test_process_frame_without_plate():
    """
    測試: 沒有偵測出車牌
    """

    frame = load_test_image()
    runner = create_runner()
    runner = create_mock_runner(runner)

    runner.detector.detect.return_value = []

    runner.process_frame(frame)

    runner.detector.detect.assert_called_once_with(frame)

    runner.ocr.recognize.assert_not_called()

    runner.image_storage.save.assert_not_called()


def test_process_frame_multiple_plates():
    """
    測試: 偵測出多個車牌
    """

    frame = load_test_image()
    runner = create_runner()
    runner = create_mock_runner(runner)

    runner.detector.detect.return_value = [
        {
            "bbox": [100, 100, 300, 180]
        },
        {
            "bbox": [400, 100, 600, 180]
        },
        {
            "bbox": [700, 100, 900, 180]
        },
    ]

    runner.ocr.recognize.side_effect = [
        {
            "plate": "ABC-1234",
            "confidence": 0.95,
        },
        {
            "plate": "XYZ-5678",
            "confidence": 0.91,
        },
        {
            "plate": "DEF-9999",
            "confidence": 0.88,
        },
    ]

    runner.image_storage.save.side_effect = [
        "tests/output/ABC1234.jpg",
        "tests/output/XYZ5678.jpg",
        "tests/output/DEF9999.jpg",
    ]

    runner.process_frame(frame)

    assert runner.ocr.recognize.call_count == 3

    assert runner.image_storage.save.call_count == 3


def test_process_frame_ocr_empty_result():
    """
    測試: OCR 回傳空字串 ""
    """

    frame = load_test_image()
    runner = create_runner()
    runner = create_mock_runner(runner)

    runner.detector.detect.return_value = [
        {
            "bbox": [100, 100, 300, 180]
        }
    ]

    runner.ocr.recognize.return_value = ""

    runner.process_frame(frame)

    runner.detector.detect.assert_called_once_with(frame)

    runner.ocr.recognize.assert_called_once()

    runner.image_storage.save.assert_not_called()


def test_process_frame_special_characters():
    """
    測試: OCR 回傳特殊字元
    """

    frame = load_test_image()
    runner = create_runner()
    runner = create_mock_runner(runner)

    runner.detector.detect.return_value = [
        {
            "bbox": [100, 100, 300, 180]
        }
    ]

    runner.ocr.recognize.return_value = {
        "plate": "A-B C@1#2$3%4",
        "confidence": 0.95,
    }

    runner.image_storage.save.return_value = (
        "tests/output/ABC1234.jpg"
    )

    runner.process_frame(frame)

    runner.detector.detect.assert_called_once_with(frame)

    runner.ocr.recognize.assert_called_once()

    runner.image_storage.save.assert_called_once_with(
        frame,
        "TEST",
        "ABC1234",
    )


def test_process_frame_ocr_failed():
    """
    測試: OCR 回傳 None
    """

    frame = load_test_image()
    runner = create_runner()
    runner = create_mock_runner(runner)

    runner.detector.detect.return_value = [
        {
            "bbox": [100, 100, 300, 180]
        }
    ]

    runner.ocr.recognize.return_value = None

    runner.process_frame(frame)

    runner.detector.detect.assert_called_once_with(frame)

    runner.ocr.recognize.assert_called_once()

    runner.image_storage.save.assert_not_called()


def test_process_frame_ocr_exception():
    """
    測試: OCR 發生 Exception
    """

    frame = load_test_image()
    runner = create_runner()
    runner = create_mock_runner(runner)

    runner.detector.detect.return_value = [
        {
            "bbox": [100, 100, 300, 180]
        }
    ]

    runner.ocr.recognize.side_effect = Exception("OCR error")

    runner.process_frame(frame)

    runner.detector.detect.assert_called_once_with(frame)

    runner.ocr.recognize.assert_called_once()

    runner.image_storage.save.assert_not_called()


def test_process_frame():
    """
    測試: 有偵測出車牌
    """

    frame = load_test_image()
    runner = create_runner()

    runner.process_frame(frame)


def load_test_image():
    """
    讀取測試用的圖片
    """

    frame = cv2.imread("tests/fixtures/car_01.png")

    assert frame is not None

    return frame


def create_runner():
    """
    建立測試用的 GateRunner
    """

    gate = MagicMock()
    gate.gate_id = "TEST"
    gate.gate_name = "Test Gate"
    gate.ip = "192.168.1.123:123"

    runner = GateRunner(gate)

    return runner


def create_mock_runner(runner):
    """
    將 GateRunner 的外部依賴替換成 Mock
    """

    # 不使用真正的 Detector / OCR / Storage
    runner.detector = MagicMock()
    runner.ocr = MagicMock()
    runner.image_storage = MagicMock()

    return runner
