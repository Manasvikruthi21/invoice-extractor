import os
import fitz  # PyMuPDF
from app.core.logger import logger

class DocumentClassifier:
    """
    Classifies documents to determine:
    - Digital vs. Scanned detection (Digital Bypass).
    - Page count and type.
    """
    
    @staticmethod
    def is_digital_pdf(file_path: str) -> bool:
        """
        Check if a PDF file is digital (searchable) or scanned.
        Returns True if selectable text is found on the first few pages.
        """
        if not file_path.lower().endswith(".pdf"):
            logger.info(f"File {os.path.basename(file_path)} is not a PDF. Classified as Scanned/Image.")
            return False
            
        try:
            doc = fitz.open(file_path)
            # Inspect first 3 pages (or total pages if less than 3)
            pages_to_check = min(len(doc), 3)
            total_text_length = 0
            
            for i in range(pages_to_check):
                page = doc[i]
                text = page.get_text().strip()
                total_text_length += len(text)
                
            doc.close()
            # If we find a reasonable amount of text, classify as digital
            is_digital = total_text_length > 100
            logger.info(f"PDF classification for {os.path.basename(file_path)}: {'Digital' if is_digital else 'Scanned'} (text len: {total_text_length})")
            return is_digital
        except Exception as e:
            logger.error(f"Error checking if PDF is digital: {str(e)}")
            return False
