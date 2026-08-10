"""
OCR Module

This package provides OCR engine implementations and a factory
for selecting the appropriate OCR service.

Available OCR Engines:
- EasyOCR
- RapidOCR

Author: AI Document Intelligence Agent
"""

from .base_ocr import BaseOCR
from .easyocr_service import EasyOCRService
from .rapidocr_service import RapidOCRService
from .factory import OCRFactory

__all__ = [
    "BaseOCR",
    "EasyOCRService",
    "RapidOCRService",
    "OCRFactory",
]