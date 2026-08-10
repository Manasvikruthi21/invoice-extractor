class ConfidenceAgent:
    """
    Calculates overall confidence score.
    """

    @staticmethod
    def calculate(ocr_confidence: float, validation: dict):

        score = float(ocr_confidence)

        score -= len(validation.get("missing_fields", [])) * 0.10
        score -= len(validation.get("warnings", [])) * 0.05

        score = max(0.0, min(score, 1.0))

        if score >= 0.90:
            status = "HIGH"
        elif score >= 0.75:
            status = "MEDIUM"
        else:
            status = "LOW"

        return {
            "overall_confidence": round(score, 3),
            "status": status,
        }