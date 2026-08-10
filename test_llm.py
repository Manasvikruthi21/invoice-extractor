from app.modules.llm import LLMFactory, ResponseParser

ocr_text = """
ABC Office Supplies Pvt. Ltd.
123 Business Park, Chennai, Tamil Nadu 600001

Invoice No: INV-2026-001
Invoice Date: 25-Jul-2026
Due Date: 08-Aug-2026

Bill To:
XYZ Technologies Pvt. Ltd.
45 IT Expressway
Bengaluru, Karnataka 560100

Laptop Stand 2 1500 3000
Wireless Mouse 5 800 4000
Keyboard 3 1200 3600

Subtotal 10600
GST 1908
Total 12508

Payment Terms: Net 14 Days
"""

llm = LLMFactory.get_llm()

response = llm.extract_invoice(ocr_text)

print("Raw Response:\n")
print(response)

print("\nParsed JSON:\n")
print(ResponseParser.parse(response))