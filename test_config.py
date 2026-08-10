from app.config.settings import settings

print("=" * 50)
print("Project Name :", settings.PROJECT_NAME)
print("Version      :", settings.VERSION)
print("Host         :", settings.HOST)
print("Port         :", settings.PORT)
print("Default OCR  :", settings.DEFAULT_OCR)
print("Default LLM  :", settings.DEFAULT_LLM)
print("=" * 50)