from app.modules.llm.gemini_client import GeminiClient

client = GeminiClient()

response = client.generate("Say only: Hello from Gemini")

print(response)