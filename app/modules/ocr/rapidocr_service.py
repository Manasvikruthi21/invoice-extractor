from rapidocr_onnxruntime import RapidOCR

from app.modules.ocr.base_ocr import BaseOCR


class RapidOCRService(BaseOCR):
    """
    RapidOCR implementation.
    """

    def __init__(self):
        self.engine = RapidOCR()

    def extract_text(self, image_path: str):

        result, _ = self.engine(image_path)

        if not result:
            return {
                "engine": "rapidocr",
                "text": "",
                "confidence": 0.0
            }

        texts = []
        confidences = []

        for box, text, confidence in result:
            texts.append(text)
            confidences.append(confidence)

        avg_confidence = (
            sum(confidences) / len(confidences)
            if confidences else 0.0
        )

        return {
            "engine": "rapidocr",
            "text": "\n".join(texts),
            "confidence": round(avg_confidence, 3)
        }