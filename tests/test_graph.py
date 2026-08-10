from app.graph.workflow import graph

state = {
    "file_path": "data/input/1000277478.jpg",

    "ocr_result": None,
    "extracted_text": None,

    "classification": None,

    "extracted_data": None,

    "validation": None,

    "confidence": None,

    "final_result": None,
}

result = graph.invoke(state)

print("\n")
print("=" * 80)
print("FINAL RESULT")
print("=" * 80)

print(result["final_result"])