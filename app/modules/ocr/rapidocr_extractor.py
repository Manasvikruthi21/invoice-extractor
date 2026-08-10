import os
from app.core.logger import logger
from app.core.config import settings

_RAPIDOCR = None

def get_rapidocr():
    """
    Lazy load the RapidOCR engine.
    """
    global _RAPIDOCR
    if _RAPIDOCR is not None:
        return _RAPIDOCR
        
    try:
        from rapidocr_onnxruntime import RapidOCR
        logger.info("Initializing RapidOCR engine...")
        _RAPIDOCR = RapidOCR()
        logger.info("RapidOCR initialized successfully.")
        return _RAPIDOCR
    except Exception as e:
        logger.error(f"Failed to initialize RapidOCR: {str(e)}")
        if settings.ALLOW_MOCK_FALLBACK:
            logger.warning("Mock fallback enabled. Returning RapidOCR mock reader.")
            return "MOCK_READER"
        raise e


class RapidOCRExtractor:
    """
    RapidOCR engine for fast ONNX-based CPU extraction.
    Used in pipeline routing when main OCR certainty is low.
    """

    @staticmethod
    def extract(image_paths: list) -> dict:
        """
        Extract text using RapidOCR and structure it in standard format.
        """
        logger.info(f"Extracting text from {len(image_paths)} pages using RapidOCR...")
        engine = get_rapidocr()
        
        if engine == "MOCK_READER":
            return RapidOCRExtractor._generate_mock_rapidocr_response(image_paths)
            
        result = {
            "engine": "RapidOCR (ONNX Runtime)",
            "pages": [],
            "raw_text": ""
        }
        
        try:
            full_text_list = []
            
            for page_idx, img_path in enumerate(image_paths):
                # Run RapidOCR
                # returns: (results_list, elapse_time)
                # results_list item: [bbox, text, confidence]
                ocr_results, elapse = engine(img_path)
                
                # Get dimensions
                try:
                    from PIL import Image as PILImage
                    with PILImage.open(img_path) as im:
                        width, height = im.size
                except Exception:
                    width, height = 1000, 1400
                    
                page_blocks = []
                if ocr_results:
                    for item in ocr_results:
                        bbox, text, confidence = item
                        # bbox coordinates are: [[x0, y0], [x1, y1], [x2, y2], [x3, y3]]
                        xs = [pt[0] for pt in bbox]
                        ys = [pt[1] for pt in bbox]
                        
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
            logger.error(f"Error in RapidOCR processing: {str(e)}")
            if settings.ALLOW_MOCK_FALLBACK:
                logger.warning("Failing back to mock RapidOCR response.")
                return RapidOCRExtractor._generate_mock_rapidocr_response(image_paths)
            raise e

    @staticmethod
    def _generate_mock_rapidocr_response(image_paths: list) -> dict:
        """
        Generate mock text simulating RapidOCR output.
        """
        logger.info("Generating RapidOCR mock response.")
        result = {
            "engine": "RapidOCR (Mocked Fallback)",
            "pages": [],
            "raw_text": ""
        }
        
        mock_text = (
            "PURCHASE ORDER\n"
            "PO #: PO-9988\n"
            "Date: July 1, 2026\n"
            "Vendor: Hardware Supplies Inc\n"
            "Address: 789 Foundry Lane, Industrial Estate\n"
            "Ship To: C/O Manas, 456 Workspace Blvd, Dev Hub\n\n"
            "Item Code | Description | Qty | Unit Price | Total\n"
            "HW-M3-01 | Developer Test Monitors | 2.0 | $200.00 | $400.00\n\n"
            "Total Amount: $400.00"
        )
        
        full_text_list = []
        for idx in range(len(image_paths)):
            lines = mock_text.split("\n")
            blocks = []
            
            for line_idx, line in enumerate(lines):
                if line.strip():
                    blocks.append({
                        "text": line.strip(),
                        "bbox": [50.0, float(50 + line_idx * 30), 650.0, float(75 + line_idx * 30)],
                        "confidence": 0.94
                    })
                    full_text_list.append(line.strip())
                    
            result["pages"].append({
                "page_idx": idx,
                "dimensions": {"width": 800.0, "height": 1100.0},
                "blocks": blocks
            })
            
        result["raw_text"] = "\n\n".join(full_text_list)
        return result
