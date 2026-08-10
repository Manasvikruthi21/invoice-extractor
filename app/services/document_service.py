"""
Document Processing Service

Pipeline:

Document
    ↓
OCR
    ↓
Document Classification
    ↓
LLM Extraction
    ↓
Validation
    ↓
Confidence
    ↓
Final JSON
"""

from pathlib import Path

from app.modules.ocr.factory import OCRFactory
from app.modules.llm.factory import LLMFactory
from app.modules.classifier.classifier_service import ClassifierService
from app.modules.validation.validator import ValidationAgent
from app.modules.confidence.confidence_agent import ConfidenceAgent


class DocumentService:
    """
    AI Document Intelligence Service
    """

    def __init__(
        self,
        ocr_engine: str = "easyocr",
        llm_engine: str = "gemini",
    ):

        self.ocr = OCRFactory.get_ocr(ocr_engine)
        self.llm = LLMFactory.get_llm(llm_engine)
        self.classifier = ClassifierService()

    def process_document(
        self,
        file_path: str | Path,
    ) -> dict:
        """
        Process uploaded document.

        Args:
            file_path: Image/PDF path

        Returns:
            Structured JSON response
        """

        file_path = str(file_path)

        # ==================================================
        # STEP 1 : OCR
        # ==================================================

        print("\n" + "=" * 70)
        print("STEP 1 : OCR")
        print("=" * 70)

        ocr_result = self.ocr.extract_text(file_path)

        extracted_text = ocr_result.get("text", "").strip()

        if not extracted_text:
            raise ValueError("OCR could not extract any text.")

        print(f"OCR Engine      : {ocr_result.get('engine')}")
        print(f"OCR Confidence  : {ocr_result.get('confidence')}")
        print(f"OCR Text Length : {len(extracted_text)}")

        # ==================================================
        # STEP 2 : DOCUMENT CLASSIFICATION
        # ==================================================

        print("\n" + "=" * 70)
        print("STEP 2 : DOCUMENT CLASSIFICATION")
        print("=" * 70)

        classification = self.classifier.classify(
            extracted_text
        )

        document_type = classification["document_type"]

        print(f"Detected Document : {document_type}")
        print(f"Confidence        : {classification['confidence']}")

        # ==================================================
        # STEP 3 : LLM EXTRACTION
        # ==================================================

        print("\n" + "=" * 70)
        print("STEP 3 : LLM EXTRACTION")
        print("=" * 70)

        if document_type == "invoice":

            extracted_data = self.llm.extract_invoice(
                extracted_text
            )

        else:

            raise ValueError(
                f"Unsupported document type: {document_type}"
            )

        print("Extraction Completed Successfully")

        # ==================================================
        # STEP 4 : VALIDATION
        # ==================================================

        print("\n" + "=" * 70)
        print("STEP 4 : VALIDATION")
        print("=" * 70)

        validation_result = ValidationAgent.validate(
            extracted_data
        )

        print(validation_result)

        # ==================================================
        # STEP 5 : CONFIDENCE SCORING
        # ==================================================

        print("\n" + "=" * 70)
        print("STEP 5 : CONFIDENCE")
        print("=" * 70)

        confidence_result = ConfidenceAgent.calculate(
            ocr_confidence=ocr_result.get(
                "confidence",
                0.0,
            ),
            validation=validation_result,
        )

        print(confidence_result)

        # ==================================================
        # STEP 6 : FINAL RESPONSE
        # ==================================================

        print("\n" + "=" * 70)
        print("DOCUMENT PROCESSING COMPLETED")
        print("=" * 70)

        return {
            "success": True,

            "classification": {
                "document_type": document_type,
                "confidence": classification["confidence"],
            },

            "ocr": {
                "engine": ocr_result.get("engine"),
                "confidence": ocr_result.get("confidence"),
            },

            "validation": validation_result,

            "confidence": confidence_result,

            "data": extracted_data,
        }