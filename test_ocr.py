from app.modules.preprocessing import PDFProcessor
from app.modules.ocr.factory import OCRFactory

pdf_path = "data/input/sample.pdf"

# Convert PDF to images
images = PDFProcessor.pdf_to_images(pdf_path, "data/temp")

# Load OCR engine
ocr = OCRFactory.get_ocr("rapidocr")

print("=" * 50)
print("OCR RESULT")
print("=" * 50)

for image in images:
    text = ocr.extract_text(image)
    print(text)