from app.modules.llm.factory import LLMFactory


sample_invoice = """
ABC Office Supplies Pvt Ltd

Invoice No: INV-1001
Invoice Date: 29-07-2026
Due Date: 05-08-2026

Customer:
XYZ Technologies

Item            Qty     Price
Laptop Bag       2      1500
Mouse            1       800

Subtotal: 3800
GST: 684
Total: 4484
"""


llm = LLMFactory.get_llm("gemini")

result = llm.extract_invoice(sample_invoice)

print(result)
