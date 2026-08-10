import os
from app.core.logger import logger
from app.core.config import settings

_EASYOCR_READER = None

def get_easyocr_reader():
    """
    Lazy load the EasyOCR Reader instance.
    """
    global _EASYOCR_READER
    if _EASYOCR_READER is not None:
        return _EASYOCR_READER
        
    try:
        import easyocr
        logger.info("Initializing EasyOCR Reader (English)...")
        # EasyOCR will download models on first call if not cached
        _EASYOCR_READER = easyocr.Reader(['en'], gpu=True)
        logger.info("EasyOCR initialized successfully.")
        return _EASYOCR_READER
    except Exception as e:
        logger.error(f"Failed to initialize EasyOCR: {str(e)}")
        if settings.ALLOW_MOCK_FALLBACK:
            logger.warning("Mock fallback enabled. Returning EasyOCR mock reader.")
            return "MOCK_READER"
        raise e


class EasyOCRExtractor:
    """
    Fallback OCR engine using EasyOCR for scene text, handwritten elements,
    or instances where docTR fails or experiences high uncertainty.
    """
    
    @staticmethod
    def extract(image_paths: list) -> dict:
        """
        Extract text using EasyOCR and structure it in standard format.
        """
        logger.info(f"Extracting text from {len(image_paths)} pages using EasyOCR...")
        reader = get_easyocr_reader()
        
        if reader == "MOCK_READER":
            return EasyOCRExtractor._generate_mock_easyocr_response(image_paths)
            
        result = {
            "engine": "EasyOCR (PyTorch)",
            "pages": [],
            "raw_text": ""
        }
        
        try:
            full_text_list = []
            
            for page_idx, img_path in enumerate(image_paths):
                # Run EasyOCR - returns list of [[box], text, confidence]
                ocr_results = reader.readtext(img_path)
                
                # Get dimensions
                try:
                    from PIL import Image as PILImage
                    with PILImage.open(img_path) as im:
                        width, height = im.size
                except Exception:
                    width, height = 1000, 1400
                    
                page_blocks = []
                for box, text, confidence in ocr_results:
                    # box coordinates are: [[x0, y0], [x1, y1], [x2, y2], [x3, y3]]
                    xs = [pt[0] for pt in box]
                    ys = [pt[1] for pt in box]
                    
                    x0 = min(xs)
                    y0 = min(ys)
                    x1 = max(xs)
                    y1 = max(ys)
                    
                    if text.strip():
                        page_blocks.append({
                            "text": text.strip(),
                            "bbox": [round(x0, 2), round(y0, 2), round(x1, 2), round(y1, 2)],
                            "confidence": round(float(confidence), 3)
                        })
                        full_text_list.append(text.strip())
                        
                result["pages"].append({
                    "page_idx": page_idx,
                    "dimensions": {"width": float(width), "height": float(height)},
                    "blocks": page_blocks
                })
                
            result["raw_text"] = "\n\n".join(full_text_list)
            return result
        except Exception as e:
            logger.error(f"Error in EasyOCR processing: {str(e)}")
            if settings.ALLOW_MOCK_FALLBACK:
                logger.warning("Failing back to mock EasyOCR response.")
                return EasyOCRExtractor._generate_mock_easyocr_response(image_paths)
            raise e

    @staticmethod
    def _generate_mock_easyocr_response(image_paths: list) -> dict:
        """
        Generate mock text simulating EasyOCR output.
        """
        logger.info("Generating EasyOCR mock response.")
        result = {
            "engine": "EasyOCR (Mocked Fallback)",
            "pages": [],
            "raw_text": ""
        }
        
        mock_text = (
            "RECEIPT\n"
            "STORE #5031 - DEVELOPER CAFE\n"
            "100 PYTHON AVENUE, WIN 10\n"
            "July 10, 2026 10:55 PM\n\n"
            "1x Large Latte - $4.50 (A)\n"
            "1x Blueberry Muffin - $3.25 (A)\n"
            "1x Chocolate Cookie - $2.50 (A)\n\n"
            "SUBTOTAL: $10.25\n"
            "TAX (8.25%): $0.85\n"
            "TOTAL: $11.10\n"
            "CARD PAYMENT: $11.10\n"
            "AUTH CODE: 123456\n\n"
            "THANK YOU FOR VISITING!"
        )
        
        full_text_list = []
        for idx in range(len(image_paths)):
            lines = mock_text.split("\n")
            blocks = []
            
            for line_idx, line in enumerate(lines):
                if line.strip():
                    blocks.append({
                        "text": line.strip(),
                        "bbox": [60.0, float(40 + line_idx * 28), 440.0, float(65 + line_idx * 28)],
                        "confidence": 0.95
                    })
                    full_text_list.append(line.strip())
                    
            result["pages"].append({
                "page_idx": idx,
                "dimensions": {"width": 500.0, "height": 800.0},
                "blocks": blocks
            })
            
        result["raw_text"] = "\n\n".join(full_text_list)
        return result
