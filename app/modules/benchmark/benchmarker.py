import time
from app.core.logger import logger
from app.modules.ocr.doctr_extractor import DocTRExtractor
from app.modules.ocr.easyocr_extractor import EasyOCRExtractor
from app.modules.ocr.rapidocr_extractor import RapidOCRExtractor

class OCRBenchmarker:
    """
    Evaluates, profiles, and compares multiple OCR engines (docTR, RapidOCR, EasyOCR)
    side-by-side on the same set of preprocessed images.
    """

    @staticmethod
    def run_benchmark(image_paths: list) -> dict:
        """
        Runs docTR, EasyOCR, and RapidOCR on the list of image paths.
        Measures latencies, character yields, and calculates comparison benchmarks.
        """
        logger.info(f"Starting OCR benchmark on {len(image_paths)} pages...")
        
        metrics = {}
        
        # 1. docTR
        t0 = time.time()
        doctr_res = DocTRExtractor.extract(image_paths)
        t_doctr = time.time() - t0
        char_doctr = len(doctr_res.get("raw_text", ""))
        word_doctr = len(doctr_res.get("raw_text", "").split())
        metrics["doctr"] = {
            "name": "Mindee docTR (MobileNetV3)",
            "latency_seconds": round(t_doctr, 3),
            "char_count": char_doctr,
            "word_count": word_doctr
        }

        # 2. RapidOCR
        t0 = time.time()
        rapid_res = RapidOCRExtractor.extract(image_paths)
        t_rapid = time.time() - t0
        char_rapid = len(rapid_res.get("raw_text", ""))
        word_rapid = len(rapid_res.get("raw_text", "").split())
        metrics["rapidocr"] = {
            "name": "RapidOCR (ONNX Runtime)",
            "latency_seconds": round(t_rapid, 3),
            "char_count": char_rapid,
            "word_count": word_rapid
        }

        # 3. EasyOCR
        t0 = time.time()
        easy_res = EasyOCRExtractor.extract(image_paths)
        t_easy = time.time() - t0
        char_easy = len(easy_res.get("raw_text", ""))
        word_easy = len(easy_res.get("raw_text", "").split())
        metrics["easyocr"] = {
            "name": "EasyOCR (PyTorch CRAFT)",
            "latency_seconds": round(t_easy, 3),
            "char_count": char_easy,
            "word_count": word_easy
        }

        # Calculate relative speeds (speed multipliers)
        # Using docTR as reference baseline
        ref_latency = max(0.001, t_doctr)
        for engine_key in metrics:
            lat = metrics[engine_key]["latency_seconds"]
            metrics[engine_key]["speed_multiplier_vs_doctr"] = round(ref_latency / max(0.001, lat), 2)
            
        logger.info("OCR benchmark completed successfully.")
        return {
            "benchmark_pages_count": len(image_paths),
            "engines": metrics,
            "summary": {
                "fastest_engine": min(metrics, key=lambda k: metrics[k]["latency_seconds"]),
                "highest_yield_engine": max(metrics, key=lambda k: metrics[k]["char_count"])
            }
        }
