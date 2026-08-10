from app.modules.classifier.classifier_service import ClassifierService

text = """
Invoice
Invoice Number INV-1001

Bill To

Subtotal
Tax

Total Amount
"""

classifier = ClassifierService()

result = classifier.classify(text)

print(result)