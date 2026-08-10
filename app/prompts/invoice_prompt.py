INVOICE_PROMPT = """
Extract the following fields from the invoice.

Return JSON containing:

- invoice_number
- invoice_date
- due_date
- merchant_name
- merchant_address
- customer_name
- customer_address
- line_items
    - description
    - quantity
    - unit_price
    - total_price
- subtotal
- tax_amount
- total_amount
- payment_details

Return only JSON.
"""
