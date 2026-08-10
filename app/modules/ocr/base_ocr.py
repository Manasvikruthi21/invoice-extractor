"""
Abstract Base Class for OCR Engines
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseOCR(ABC):
    """
    Base interface for every OCR engine.
    """

    @abstractmethod
    def extract_text(self, image_path: str) -> Dict[str, Any]:
        """
        Extract text from image.

        Returns:
            {
                "engine": "...",
                "text": "...",
                "confidence": 0.98
            }
        """
        pass