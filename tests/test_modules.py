import os
import sys

# Ensure project root is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.modules.ocr.merger import OCRMerger
from app.modules.ocr.rapidocr_extractor import RapidOCRExtractor
from app.modules.validation.validator import DocumentValidator

def test_ocr_merger():
    """
    Test spatial merge logic between two OCR engines.
    """
    # Block A and Block B overlap
    res_a = {
        "engine": "Engine-A",
        "pages": [
            {
                "page_idx": 0,
                "dimensions": {"width": 1000, "height": 1000},
                "blocks": [
                    {"text": "Acme Corp", "bbox": [100, 100, 200, 150], "confidence": 0.9}
                ]
            }
        ]
    }
    
    res_b = {
        "engine": "Engine-B",
        "pages": [
            {
                "page_idx": 0,
                "dimensions": {"width": 1000, "height": 1000},
                "blocks": [
                    {"text": "ACME Corporation", "bbox": [105, 102, 198, 148], "confidence": 0.95}, # Overlaps A
                    {"text": "Invoice Details", "bbox": [500, 500, 600, 550], "confidence": 0.8} # Unique
                ]
            }
        ]
    }

    merged = OCRMerger.merge(res_a, res_b)
    
    # Should keep the higher confidence block (Engine B's 'ACME Corporation') 
    # and the unique block ('Invoice Details')
    assert len(merged["pages"][0]["blocks"]) == 2
    texts = [b["text"] for b in merged["pages"][0]["blocks"]]
    assert "ACME Corporation" in texts
    assert "Invoice Details" in texts
    assert "Acme Corp" not in texts


def test_document_validator_invoice():
    """
    Test validator checking subtotal + tax = total math.
    """
    # Valid invoice
    valid_data = {
        "subtotal": 100.0,
        "tax_amount": 10.0,
        "total_amount": 110.0,
        "line_items": [
            {"description": "Item 1", "quantity": 2, "unit_price": 50.0, "total_price": 100.0}
        ]
    }
    report = DocumentValidator.validate(valid_data, "invoice")
    assert report["is_valid"] is True
    assert len(report["errors"]) == 0
    
    # Invalid invoice
    invalid_data = {
        "subtotal": 100.0,
        "tax_amount": 10.0,
        "total_amount": 150.0, # Math error: 100 + 10 != 150
        "line_items": [
            {"description": "Item 1", "quantity": 2, "unit_price": 50.0, "total_price": 100.0}
        ]
    }
    report = DocumentValidator.validate(invalid_data, "invoice")
    assert report["is_valid"] is False
    assert len(report["errors"]) > 0


def test_rapid_ocr_mock():
    """
    Verify mock generator for RapidOCR works as expected.
    """
    res = RapidOCRExtractor.extract(["dummy_image.png"])
    assert res["engine"] == "RapidOCR (Mocked Fallback)"
    assert "PURCHASE ORDER" in res["raw_text"]
