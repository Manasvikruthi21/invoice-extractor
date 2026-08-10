import fitz
from pathlib import Path


class PDFProcessor:
    """
    Converts PDF pages into images.
    """

    @staticmethod
    def pdf_to_images(pdf_path: str, output_dir: str):

        pdf = fitz.open(pdf_path)

        output = Path(output_dir)
        output.mkdir(parents=True, exist_ok=True)

        image_paths = []

        for page_number, page in enumerate(pdf):

            pix = page.get_pixmap(dpi=300)

            image_path = output / f"page_{page_number+1}.png"

            pix.save(image_path)

            image_paths.append(str(image_path))

        pdf.close()

        return image_paths