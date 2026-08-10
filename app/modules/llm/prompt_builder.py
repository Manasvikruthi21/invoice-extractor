"""
Prompt Builder for AI Document Intelligence Agent
"""

BASE_SYSTEM_INSTRUCTION = """
You are an expert AI document extraction system.

Your task is to extract structured information from OCR text.

Rules:
1. Return ONLY valid JSON.
2. Do NOT include markdown.
3. Do NOT include explanations.
4. Do NOT invent values.
5. Preserve invoice numbers exactly.
6. Preserve dates exactly.
7. Preserve monetary values exactly.
8. If a field is missing, return null.
"""


INVOICE_PROMPT = """
Extract the following fields:

{
    "invoice_number": "",
    "invoice_date": "",
    "due_date": "",
    "merchant_name": "",
    "merchant_address": "",
    "customer_name": "",
    "customer_address": "",
    "line_items": [
        {
            "description": "",
            "quantity": "",
            "unit_price": "",
            "total_price": ""
        }
    ],
    "subtotal": "",
    "tax_amount": "",
    "total_amount": "",
    "payment_details": ""
}
"""


RECEIPT_PROMPT = """
Extract receipt information as structured JSON.
"""


BANK_STATEMENT_PROMPT = """
Extract bank statement information as structured JSON.
"""


PO_PROMPT = """
Extract purchase order information as structured JSON.
"""


FORM_PROMPT = """
Extract all available fields from the document as JSON.
"""


PROMPT_MAP = {
    "invoice": INVOICE_PROMPT,
    "receipt": RECEIPT_PROMPT,
    "bank_statement": BANK_STATEMENT_PROMPT,
    "purchase_order": PO_PROMPT,
    "form": FORM_PROMPT,
}


class PromptBuilder:
    """
    Builds prompts for Gemini.
    """

    @staticmethod
    def format_ocr_context(ocr_result: dict) -> str:
        """
        Supports both:

        {
            "text": "...",
            "confidence": ...
        }

        and

        {
            "raw_text": "...",
            "pages": [...]
        }
        """

        raw_text = (
            ocr_result.get("text")
            or ocr_result.get("raw_text")
            or ""
        ).strip()

        if raw_text:
            return raw_text

        lines = []

        for page in ocr_result.get("pages", []):

            for block in page.get("blocks", []):

                text = block.get("text", "").strip()

                if text:
                    lines.append(text)

        return "\n".join(lines)

    @classmethod
    def build_prompt(
        cls,
        ocr_result: dict,
        schema_type: str = "invoice",
    ) -> str:

        schema_type = schema_type.lower()

        if schema_type not in PROMPT_MAP:
            schema_type = "form"

        ocr_context = cls.format_ocr_context(ocr_result)

        return f"""
{BASE_SYSTEM_INSTRUCTION}

{PROMPT_MAP[schema_type]}

OCR TEXT
========================================

{ocr_context}

========================================

Return ONLY valid JSON.
"""