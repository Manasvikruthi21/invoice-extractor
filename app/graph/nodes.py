"""
LangGraph Nodes

Each node performs one task and updates the shared GraphState.
"""

from app.graph.state import GraphState

from app.modules.ocr.factory import OCRFactory
from app.modules.classifier.classifier_service import ClassifierService
from app.modules.llm.factory import LLMFactory
from app.modules.validation.validator import ValidationAgent
from app.modules.confidence.confidence_agent import ConfidenceAgent


# ==========================================================
# OCR NODE
# ==========================================================

def ocr_node(state: GraphState):
    """
    Extract text from the document using OCR.
    """

    print("\n" + "=" * 70)
    print("STEP 1 : OCR")
    print("=" * 70)

    ocr = OCRFactory.get_ocr("easyocr")

    ocr_result = ocr.extract_text(state["file_path"])

    extracted_text = ocr_result.get("text", "").strip()

    if not extracted_text:
        raise ValueError("OCR could not extract any text.")

    state["ocr_result"] = ocr_result
    state["extracted_text"] = extracted_text

    print(f"OCR Engine      : {ocr_result['engine']}")
    print(f"OCR Confidence  : {ocr_result['confidence']}")
    print(f"OCR Text Length : {len(extracted_text)}")

    return state


# ==========================================================
# DOCUMENT CLASSIFICATION NODE
# ==========================================================

def classifier_node(state: GraphState):
    """
    Detect document type.
    """

    print("\n" + "=" * 70)
    print("STEP 2 : DOCUMENT CLASSIFICATION")
    print("=" * 70)

    classifier = ClassifierService()

    classification = classifier.classify(
        state["extracted_text"]
    )

    state["classification"] = classification

    print(f"Document Type : {classification['document_type']}")
    print(f"Confidence    : {classification['confidence']}")

    return state


# ==========================================================
# LLM EXTRACTION NODE
# ==========================================================

def extraction_node(state: GraphState):
    """
    Extract structured data using Gemini.
    """

    print("\n" + "=" * 70)
    print("STEP 3 : GEMINI EXTRACTION")
    print("=" * 70)

    llm = LLMFactory.get_llm("gemini")

    document_type = state["classification"]["document_type"]

    if document_type == "invoice":

        extracted_data = llm.extract_invoice(
            state["extracted_text"]
        )

    else:

        raise ValueError(
            f"Unsupported document type: {document_type}"
        )

    state["extracted_data"] = extracted_data

    print("Extraction Completed Successfully")

    return state


# ==========================================================
# VALIDATION NODE
# ==========================================================

def validation_node(state: GraphState):
    """
    Validate extracted JSON.
    """

    print("\n" + "=" * 70)
    print("STEP 4 : VALIDATION")
    print("=" * 70)

    validation = ValidationAgent.validate(
        state["extracted_data"]
    )

    state["validation"] = validation

    print(validation)

    return state


# ==========================================================
# CONFIDENCE NODE
# ==========================================================

def confidence_node(state: GraphState):
    """
    Calculate overall confidence.
    """

    print("\n" + "=" * 70)
    print("STEP 5 : CONFIDENCE")
    print("=" * 70)

    confidence = ConfidenceAgent.calculate(
        ocr_confidence=state["ocr_result"]["confidence"],
        validation=state["validation"],
    )

    state["confidence"] = confidence

    print(confidence)

    return state


# ==========================================================
# FINAL RESPONSE NODE
# ==========================================================

def final_node(state: GraphState):
    """
    Build the final API response.
    """

    print("\n" + "=" * 70)
    print("STEP 6 : FINAL RESPONSE")
    print("=" * 70)

    state["final_result"] = {

        "success": True,

        "classification": state["classification"],

        "ocr": {
            "engine": state["ocr_result"]["engine"],
            "confidence": state["ocr_result"]["confidence"],
        },

        "validation": state["validation"],

        "confidence": state["confidence"],

        "data": state["extracted_data"],
    }

    print("Workflow Completed Successfully")

    return state