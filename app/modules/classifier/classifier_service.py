from app.modules.classifier.base_classifier import BaseClassifier
from app.modules.classifier.rules import DOCUMENT_RULES


class ClassifierService(BaseClassifier):
    """
    Rule-based document classifier.
    """

    def classify(self, text: str) -> dict:

        text = text.lower()

        scores = {}

        for document_type, keywords in DOCUMENT_RULES.items():

            score = 0

            for keyword in keywords:

                if keyword.lower() in text:
                    score += 1

            scores[document_type] = score

        best_document = max(
            scores,
            key=scores.get
        )

        total_keywords = len(
            DOCUMENT_RULES[best_document]
        )

        confidence = scores[best_document] / total_keywords

        return {
            "document_type": best_document,
            "confidence": round(confidence, 2)
        }