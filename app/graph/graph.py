from langgraph.graph import StateGraph, START, END

from app.graph.state import GraphState

from app.graph.nodes import (
    preprocess_node,
    ocr_node,
    extraction_node,
    validation_node,
    confidence_node,
)

# -----------------------------------
# Create Workflow
# -----------------------------------

workflow = StateGraph(GraphState)

# -----------------------------------
# Register Nodes
# -----------------------------------

workflow.add_node("preprocess", preprocess_node)

workflow.add_node("ocr", ocr_node)

workflow.add_node("extract", extraction_node)

workflow.add_node("validate", validation_node)

workflow.add_node("confidence", confidence_node)

# -----------------------------------
# Build Graph
# -----------------------------------

workflow.add_edge(START, "preprocess")

workflow.add_edge("preprocess", "ocr")

workflow.add_edge("ocr", "extract")

workflow.add_edge("extract", "validate")

workflow.add_edge("validate", "confidence")

workflow.add_edge("confidence", END)

# -----------------------------------
# Compile
# -----------------------------------

graph = workflow.compile()
