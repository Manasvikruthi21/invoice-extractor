from abc import ABC, abstractmethod


class BaseClassifier(ABC):
    """
    Base interface for document classifiers.
    """

    @abstractmethod
    def classify(self, text: str) -> dict:
        """
        Returns:
        {
            "document_type": "...",
            "confidence": 0.95
        }
        """
        pass