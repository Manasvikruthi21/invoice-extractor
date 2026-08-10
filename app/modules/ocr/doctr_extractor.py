import os
from app.core.logger import logger
from app.core.config import settings

# Global variables for lazy-loading models
_DOCTR_MODEL = None

def get_doctr_model():
    """
    Lazy load the docTR OCR predictor to speed up startup.
    Uses a lightweight MobileNet backend for detection/recognition.
    """
    global _DOCTR_MODEL
    if _DOCTR_MODEL is not None:
        return _DOCTR_MODEL
        
    try:
        from doctr.models import ocr_predictor
        import torch
        
        logger.info("Initializing Mindee docTR Predictor (MobileNetV3 lightweight)...")
        # Check if CUDA is available
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Using device: {device} for docTR")
        
        # Load lightweight models for faster CPU/GPU processing
        _DOCTR_MODEL = ocr_predictor(
            det_arch="db_mobilenet_v3_large", 
            reco_arch="crnn_mobilenet_v3_large",
            pretrained=True
        )
        
        # Move to GPU if torch has CUDA
        if device.type == "cuda":
            _DOCTR_MODEL = _DOCTR_MODEL.cuda()
            
        logger.info("docTR initialized successfully.")
        return _DOCTR_MODEL
    except Exception as e:
        logger.error(f"Failed to import or initialize docTR: {str(e)}")
        if settings.ALLOW_MOCK_FALLBACK:
            logger.warning("Mock fallback is enabled. Returning mock extractor.")
            return "MOCK_MODEL"
        raise e


class DocTRExtractor:
    """
    Handles scanned document OCR via Mindee docTR.
    Returns layout in a standardized format.
    """

    @staticmethod
    def extract(image_paths: list) -> dict:
        """
        Extract text and layout from scanned images using Mindee docTR.
        Returns layout in a standardized format.
        """
        logger.info(f"Extracting text from {len(image_paths)} pages using Mindee docTR...")
        model = get_doctr_model()
        
        if model == "MOCK_MODEL":
            return DocTRExtractor._generate_mock_ocr_response(image_paths, "Mindee docTR (Mocked)")
            
        result = {
            "engine": "Mindee docTR (MobileNetV3)",
            "pages": [],
            "raw_text": ""
        }
        
        try:
            from doctr.io import DocumentFile
            
            # Read images using docTR loader
            docs = [DocumentFile.from_images([img])[0] for img in image_paths]
            
            full_text_list = []
            
            for page_idx, doc_img in enumerate(docs):
                # Run prediction on single page
                pred = model([doc_img])
                export_data = pred.export()
                
                # Retrieve original image size
                img_path = image_paths[page_idx]
                try:
                    from PIL import Image as PILImage
                    with PILImage.open(img_path) as im:
                        width, height = im.size
                except Exception:
                    width, height = 1000, 1400  # Default fallback
                
                page_data = export_data["pages"][0]
                page_blocks = []
                
                # docTR coordinates are normalized (0 to 1). Convert to pixel bboxes.
                for block in page_data.get("blocks", []):
                    block_text_parts = []
                    # Keep track of words coordinates to construct block level box
                    xs, ys = [], []
                    
                    for line in block.get("lines", []):
                        for word in line.get("words", []):
                            w_text = word["value"]
                            block_text_parts.append(w_text)
                            
                            # docTR word bbox is geometry: ((xmin, ymin), (xmax, ymax))
                            geom = word["geometry"]
                            (xmin, ymin), (xmax, ymax) = geom
                            xs.extend([xmin, xmax])
                            ys.extend([ymin, ymax])
                            
                    if block_text_parts:
                        block_text = " ".join(block_text_parts)
                        x0 = min(xs) * width if xs else 0.0
                        y0 = min(ys) * height if ys else 0.0
                        x1 = max(xs) * width if xs else width
                        y1 = max(ys) * height if ys else height
                        
                        # Calculate mean confidence
                        word_count = sum(len(l.get("words", [])) for l in block.get("lines", []))
                        sum_confidence = sum(w["confidence"] for l in block.get("lines", []) for w in l.get("words", []))
                        avg_confidence = round(sum_confidence / max(1, word_count), 3)
                        
                        page_blocks.append({
                            "text": block_text,
                            "bbox": [round(x0, 2), round(y0, 2), round(x1, 2), round(y1, 2)],
                            "confidence": avg_confidence
                        })
                        full_text_list.append(block_text)
                        
                result["pages"].append({
                    "page_idx": page_idx,
                    "dimensions": {"width": float(width), "height": float(height)},
                    "blocks": page_blocks
                })
                
            result["raw_text"] = "\n\n".join(full_text_list)
            return result
        except Exception as e:
            logger.error(f"Error in docTR OCR processing: {str(e)}")
            if settings.ALLOW_MOCK_FALLBACK:
                logger.warning("Failing back to mock OCR response due to exception.")
                return DocTRExtractor._generate_mock_ocr_response(image_paths, "Mindee docTR (Mock-Fallback)")
            raise e

    @staticmethod
    def _generate_mock_ocr_response(image_paths: list, engine_name: str) -> dict:
        """
        Generates structured mock OCR response when OCR library loading fails.
        Enables demonstration and verification of formatting logic without CUDA/Heavy installs.
        """
        logger.info(f"Generating mock OCR text for {len(image_paths)} pages.")
        result = {
            "engine": engine_name,
            "pages": [],
            "raw_text": ""
        }
        
        mock_texts = [
            # Page 0
            "INVOICE\n"
            "ACME Corporation Ltd\n"
            "123 Innovation Way, Tech City\n"
            "Date: July 10, 2026\n"
            "Invoice #: INV-2026-0042\n"
            "Due Date: August 10, 2026\n\n"
            "Bill To:\n"
            "Manas Corporation\n"
            "456 Workspace Blvd, Dev Hub\n\n"
            "Description | Qty | Unit Price | Total\n"
            "Cloud Database Hosting | 1 | $250.00 | $250.00\n"
            "Agent Processing API | 5 | $50.00 | $250.00\n"
            "Custom VLM Integration | 2 | $150.00 | $300.00\n\n"
            "Subtotal: $800.00\n"
            "Tax (VAT 10%): $80.00\n"
            "Total Amount Due: $880.00\n\n"
            "Payment Details:\n"
            "Bank Account: Acme Corp Ltd, Bank: Developer Savings Bank\n"
            "Thank you for your business!"
        ]
        
        full_text_list = []
        for idx in range(len(image_paths)):
            # Cycle through mock texts if multiple pages
            m_text = mock_texts[idx % len(mock_texts)]
            lines = m_text.split("\n")
            blocks = []
            
            for line_idx, line in enumerate(lines):
                if line.strip():
                    blocks.append({
                        "text": line.strip(),
                        "bbox": [50.0, float(50 + line_idx * 30), 650.0, float(75 + line_idx * 30)],
                        "confidence": 0.98
                    })
                    full_text_list.append(line.strip())
                    
            result["pages"].append({
                "page_idx": idx,
                "dimensions": {"width": 800.0, "height": 1100.0},
                "blocks": blocks
            })
            
        result["raw_text"] = "\n\n".join(full_text_list)
        return result
