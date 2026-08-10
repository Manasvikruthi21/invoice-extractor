import os
import time

from dotenv import load_dotenv
from google import genai


class GeminiClient:
    """
    Gemini API Client with automatic retry support.
    """

    def __init__(self):
        load_dotenv()

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env")

        self.model = os.getenv(
            "GEMINI_MODEL",
            "models/gemini-3.5-flash",
        )

        self.client = genai.Client(api_key=api_key)

    def generate(self, prompt: str) -> str:
        """
        Send prompt to Gemini with automatic retry.
        """

        max_retries = 3
        retry_delay = 5  # seconds

        for attempt in range(max_retries):
            try:

                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                )

                if response.text:
                    return response.text

                raise RuntimeError("Gemini returned an empty response.")

            except Exception as e:

                # Last attempt → raise the error
                if attempt == max_retries - 1:
                    raise RuntimeError(
                        f"Gemini API failed after {max_retries} attempts.\n{str(e)}"
                    )

                print(
                    f"[Gemini Retry {attempt + 1}/{max_retries}] "
                    f"API unavailable. Retrying in {retry_delay} seconds..."
                )

                time.sleep(retry_delay)