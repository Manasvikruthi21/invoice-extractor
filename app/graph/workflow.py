"""
LangGraph Workflow

Pipeline

START
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
Final Response
    ↓
END
"""

from langgraph.graph import StateGraph, START, END

from app.graph.state import GraphState

from app.graph.nodes import (
    ocr_node,
    classifier_node,
    extraction_node,
    validation_node,
    confidence_node,
    final_node,
)

# ==========================================================
# Create Workflow
# ==========================================================

workflow = StateGraph(GraphState)

# ==========================================================
# Register Nodes
# ==========================================================

workflow.add_node(
    "ocr",
    ocr_node,
)

workflow.add_node(
    "classifier",
    classifier_node,
)

workflow.add_node(
    "extraction",
    extraction_node,
)

workflow.add_node(
    "validation",
    validation_node,
)

workflow.add_node(
    "confidence",
    confidence_node,
)

workflow.add_node(
    "final",
    final_node,
)

# ==========================================================
# Connect Nodes
# ==========================================================

workflow.add_edge(
    START,
    "ocr",
)

workflow.add_edge(
    "ocr",
    "classifier",
)

workflow.add_edge(
    "classifier",
    "extraction",
)

workflow.add_edge(
    "extraction",
    "validation",
)

workflow.add_edge(
    "validation",
    "confidence",
)

workflow.add_edge(
    "confidence",
    "final",
)

workflow.add_edge(
    "final",
    END,
)

# ==========================================================
# Compile Graph
# ==========================================================

graph = workflow.compile()