from app.modules.preprocessing import (
    DocumentLoader,
    PDFProcessor,
    ImageProcessor,
)

pdf = "data/input/sample.pdf"

DocumentLoader.validate(pdf)

images = PDFProcessor.pdf_to_images(
    pdf,
    "data/temp",
)

for image in images:
    ImageProcessor.preprocess(image)

print("Generated Images:")
for img in images:
    print(img)