from paddleocr import PaddleOCR
import numpy as np
import cv2

_ocr = None


def get_ocr():
    global _ocr
    if _ocr is None:
        _ocr = PaddleOCR(use_textline_orientation=True, lang='en')
    return _ocr


def extract_text_ocr(image_path: str) -> str:
    ocr = get_ocr()
    result = ocr.ocr(image_path)
    if not result:
        return ""
    texts = []
    for item in result:
        if isinstance(item, dict):
            texts.extend(item.get('rec_texts', []))
    return ' '.join(texts).strip()
