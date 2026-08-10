import easyocr

from app.modules.ocr.base_ocr import BaseOCR


class EasyOCRService(BaseOCR):

    def __init__(self):

        self.reader = easyocr.Reader(
            ['en'],
            gpu=False
        )

    def extract_text(self, image_path: str):

        result = self.reader.readtext(image_path)

        text = []
        confidence = []

        for _, txt, conf in result:
            text.append(txt)
            confidence.append(conf)

        avg_conf = (
            sum(confidence) / len(confidence)
            if confidence else 0.0
        )

        return {
            "engine": "easyocr",
            "text": "\n".join(text),
            "confidence": round(avg_conf, 3)
        }