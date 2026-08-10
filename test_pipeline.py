from app.modules.preprocessing import PDFProcessor
from app.modules.ocr.factory import OCRFactory
from app.modules.llm.gemini_client import StructureAgent

# Step 1: Convert PDF to images
pdf_path = "data/input/sample.pdf"
images = PDFProcessor.pdf_to_images(pdf_path, "data/temp")

# Step 2: OCR
ocr = OCRFactory.get_ocr("rapidocr")

raw_text = ""

for image in images:
    result = ocr.extract_text(image)

    # Handle both dict and string outputs
    if isinstance(result, dict):
        raw_text += result.get("text", "") + "\n"
    else:
        raw_text += str(result) + "\n"

print("=" * 60)
print("OCR TEXT")
print("=" * 60)
print(raw_text)

# Step 3: Prepare input for StructureAgent
ocr_result = {
    "raw_text": raw_text,
    "pages": []
}

# Step 4: Extract structured invoice
structured = StructureAgent.structure_document(
    ocr_result,
    "invoice"
)

print("\n" + "=" * 60)
print("STRUCTURED JSON")
print("=" * 60)
print(structured)