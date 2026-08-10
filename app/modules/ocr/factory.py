from app.modules.ocr.easyocr_service import EasyOCRService
from app.modules.ocr.rapidocr_service import RapidOCRService


class OCRFactory:
    """
    Factory class to create OCR engine instances.
    """

    @staticmethod
    def get_ocr(engine_name: str):

        engine_name = engine_name.lower()

        if engine_name == "easyocr":
            return EasyOCRService()

        elif engine_name == "rapidocr":
            return RapidOCRService()

        raise ValueError(f"Unsupported OCR Engine: {engine_name}")
    