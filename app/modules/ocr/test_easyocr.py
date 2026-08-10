from app.modules.ocr.easyocr_service import EasyOCRService

ocr = EasyOCRService()

result = ocr.extract_text("data/input/sample.png")

print(result)