"""
Gemini LLM Service
"""

from app.modules.llm.base_llm import BaseLLM
from app.modules.llm.gemini_client import GeminiClient
from app.modules.llm.prompt_builder import PromptBuilder
from app.modules.llm.parser import ResponseParser


class GeminiService(BaseLLM):
    """
    Gemini implementation for document extraction.
    """

    def __init__(self):
        self.client = GeminiClient()

    def extract_invoice(self, text: str) -> dict:
        """
        Extract structured invoice data using Gemini.

        Args:
            text: OCR extracted text

        Returns:
            Parsed JSON dictionary
        """

        ocr_result = {
            "text": text
        }

        # Build prompt
        prompt = PromptBuilder.build_prompt(
            ocr_result=ocr_result,
            schema_type="invoice",
        )

        # Debug information
        print("\n" + "=" * 70)
        print("GEMINI SERVICE")
        print("=" * 70)
        print(f"OCR Text Length : {len(text)}")
        print(f"Prompt Length   : {len(prompt)}")
        print("-" * 70)
        print("Prompt Preview:")
        print(prompt[:800])
        print("-" * 70)

        # Call Gemini
        response = self.client.generate(prompt)

        print("Gemini Response Received")
        print("-" * 70)
        print(response[:1000])
        print("-" * 70)

        # Convert JSON string to Python dict
        parsed_response = ResponseParser.parse(response)

        return parsed_response

    def extract_document(
        self,
        text: str,
        schema_type: str = "invoice",
    ) -> dict:
        """
        Generic extraction entry point.
        """

        schema_type = schema_type.lower()

        if schema_type == "invoice":
            return self.extract_invoice(text)

        raise ValueError(
            f"Unsupported schema type: {schema_type}"
        )