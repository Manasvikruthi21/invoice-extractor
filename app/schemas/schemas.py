from pydantic import BaseModel, Field
from typing import List, Optional

# ==========================================
# Pydantic Schemas for Structured Output
# ==========================================

class InvoiceItem(BaseModel):
    description: str = Field(description="Description of the item or service.")
    quantity: Optional[float] = Field(None, description="Quantity of the item. Default to None if not specified.")
    unit_price: Optional[float] = Field(None, description="Price per single unit. Default to None if not specified.")
    total_price: float = Field(description="Total price for this line item.")

class InvoiceSchema(BaseModel):
    invoice_number: Optional[str] = Field(None, description="The unique identifier/number of the invoice.")
    invoice_date: Optional[str] = Field(None, description="The date the invoice was issued.")
    due_date: Optional[str] = Field(None, description="The date the invoice payment is due.")
    merchant_name: str = Field(description="The name of the vendor/sender company.")
    merchant_address: Optional[str] = Field(None, description="The physical or billing address of the merchant.")
    customer_name: Optional[str] = Field(None, description="The name of the client/recipient company or individual.")
    customer_address: Optional[str] = Field(None, description="The shipping/billing address of the customer.")
    line_items: List[InvoiceItem] = Field(default_factory=list, description="Array of purchased products or services.")
    subtotal: Optional[float] = Field(None, description="Sum of all items before taxes and discounts.")
    tax_amount: Optional[float] = Field(None, description="Tax charged, e.g. VAT, GST, Sales tax.")
    total_amount: float = Field(description="The total final amount due/paid.")
    payment_details: Optional[str] = Field(None, description="Bank account numbers, wire instructions, or terms mentioned.")


class ReceiptItem(BaseModel):
    name: str = Field(description="Name or short description of the item.")
    price: float = Field(description="Price paid for the item.")

class ReceiptSchema(BaseModel):
    merchant_name: str = Field(description="The name of the store, restaurant, or vendor.")
    merchant_address: Optional[str] = Field(None, description="Address of the store/vendor.")
    date_time: Optional[str] = Field(None, description="Date and time of the purchase.")
    items: List[ReceiptItem] = Field(default_factory=list, description="List of items on the receipt.")
    subtotal: Optional[float] = Field(None, description="Subtotal before tax.")
    tax: Optional[float] = Field(None, description="Tax amount.")
    total: float = Field(description="Total amount paid.")
    payment_method: Optional[str] = Field(None, description="Cash, Credit Card, Mobile Pay, etc.")


class TransactionItem(BaseModel):
    date: str = Field(description="The date the transaction took place.")
    description: str = Field(description="The description/memo of the transaction.")
    amount: float = Field(description="The transaction amount. Positive for credit/deposit, negative for debit/withdrawal.")
    type: str = Field(description="Transaction type, either 'CREDIT' or 'DEBIT'.")
    balance: Optional[float] = Field(None, description="Running balance after transaction.")

class BankStatementSchema(BaseModel):
    bank_name: str = Field(description="The name of the banking institution.")
    account_holder: str = Field(description="The name of the account holder.")
    account_number: Optional[str] = Field(None, description="The bank account number.")
    statement_period: Optional[str] = Field(None, description="The date range covered by the statement.")
    opening_balance: Optional[float] = Field(None, description="The starting balance of the period.")
    closing_balance: Optional[float] = Field(None, description="The ending balance of the period.")
    transactions: List[TransactionItem] = Field(default_factory=list, description="List of individual transactions.")


class POItem(BaseModel):
    item_code: Optional[str] = Field(None, description="Part number, SKU, or item code.")
    description: str = Field(description="Description of the item ordered.")
    quantity: float = Field(description="Quantity ordered.")
    unit_price: float = Field(description="Price per unit.")
    total_price: float = Field(description="Total cost for this item line.")

class PurchaseOrderSchema(BaseModel):
    po_number: str = Field(description="The unique Purchase Order number.")
    po_date: str = Field(description="Date of the purchase order.")
    vendor_name: str = Field(description="The name of the supplier/vendor.")
    vendor_address: Optional[str] = Field(None, description="Vendor billing/correspondence address.")
    shipping_address: Optional[str] = Field(None, description="Destination address where items should be delivered.")
    items: List[POItem] = Field(default_factory=list, description="List of items ordered.")
    total_amount: float = Field(description="The total amount of the purchase order.")


class GenericField(BaseModel):
    key: str = Field(description="Label or name of the field.")
    value: str = Field(description="The content or check status of the field.")
    confidence: float = Field(0.9, description="Confidence estimation of extraction.")

class GenericFormSchema(BaseModel):
    form_title: Optional[str] = Field(None, description="Title or heading of the form.")
    fields: List[GenericField] = Field(default_factory=list, description="Extracted key-value pairs from the form.")


# Mapping for schemas
SCHEMA_MAP = {
    "invoice": InvoiceSchema,
    "receipt": ReceiptSchema,
    "bank_statement": BankStatementSchema,
    "purchase_order": PurchaseOrderSchema,
    "form": GenericFormSchema
}
