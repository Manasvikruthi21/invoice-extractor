"""
Graph State

Shared state passed between LangGraph nodes.
"""

from typing import Optional, TypedDict


class GraphState(TypedDict):
    """
    Shared state across the workflow.
    """

    # Input
    file_path: str

    # OCR
    ocr_result: Optional[dict]
    extracted_text: Optional[str]

    # Classification
    classification: Optional[dict]

    # LLM
    extracted_data: Optional[dict]

    # Validation
    validation: Optional[dict]

    # Confidence
    confidence: Optional[dict]

    # Final Response
    final_result: Optional[dict]