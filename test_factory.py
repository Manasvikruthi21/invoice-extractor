from app.modules.ocr.factory import OCRFactory

# Test RapidOCR
rapid = OCRFactory.get_ocr("rapidocr")
print(type(rapid).__name__)

# Test EasyOCR
easy = OCRFactory.get_ocr("easyocr")
print(type(easy).__name__)