import os
import fitz  # PyMuPDF
from app.core.logger import logger

class PyMuPDFExtractor:
    """
    Handles PDF native text extraction (Digital Bypass) via PyMuPDF.
    Returns layout in a standardized format.
    """

    @staticmethod
    def extract(file_path: str) -> dict:
        """
        Extract text and layout from a digital PDF using PyMuPDF (fitz).
        Returns layout in a standardized format.
        """
        logger.info(f"Extracting native text from digital PDF: {os.path.basename(file_path)}")
        result = {
            "engine": "PyMuPDF (Native)",
            "pages": [],
            "raw_text": ""
        }
        
        try:
            doc = fitz.open(file_path)
            full_text_list = []
            
            for page_idx, page in enumerate(doc):
                w, h = page.rect.width, page.rect.height
                blocks = page.get_text("blocks")  # (x0, y0, x1, y1, "text", block_no, block_type)
                
                page_blocks = []
                for b in blocks:
                    # Filter out non-text blocks (block_type 0 is text)
                    if len(b) > 4 and b[4].strip():
                        page_blocks.append({
                            "text": b[4].strip(),
                            "bbox": [round(b[0], 2), round(b[1], 2), round(b[2], 2), round(b[3], 2)],
                            "confidence": 1.0
                        })
                        full_text_list.append(b[4].strip())
                
                result["pages"].append({
                    "page_idx": page_idx,
                    "dimensions": {"width": float(w), "height": float(h)},
                    "blocks": page_blocks
                })
                
            result["raw_text"] = "\n\n".join(full_text_list)
            doc.close()
            return result
        except Exception as e:
            logger.error(f"Error in PyMuPDF extraction: {str(e)}")
            raise e
