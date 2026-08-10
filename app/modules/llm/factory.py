from app.modules.llm.gemini_service import GeminiService


class LLMFactory:

    @staticmethod
    def get_llm(name="gemini"):

        if name.lower() == "gemini":
            return GeminiService()

        raise ValueError(f"Unsupported LLM: {name}")