from app.modules.validation.rules import REQUIRED_FIELDS


class ValidationAgent:
    """
    Validates extracted document data.
    """

    @staticmethod
    def validate(data: dict):

        missing_fields = []
        warnings = []

        # Required field validation
        for field in REQUIRED_FIELDS:

            value = data.get(field)

            if value is None:
                missing_fields.append(field)

            elif isinstance(value, str) and value.strip() == "":
                missing_fields.append(field)

            elif isinstance(value, list) and len(value) == 0:
                missing_fields.append(field)

        # Total amount validation
        total = data.get("total_amount")

        if total is None:
            warnings.append("Total amount missing.")

        # Line item validation
        items = data.get("line_items", [])

        if len(items) == 0:
            warnings.append("No line items found.")

        status = "passed"

        if missing_fields:
            status = "failed"

        return {
            "status": status,
            "missing_fields": missing_fields,
            "warnings": warnings,
        }