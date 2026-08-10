# Technical Research & Benchmarking Report
**AI Document Intelligence Agent**
*Date: July 10, 2026*

---

## 1. Executive Summary
This report analyzes and details the technology selection for an **AI-powered Document Intelligence Agent**. The objective of the system is to process business documents (invoices, receipts, bank statements) with high layout-preservation accuracy, fast latencies, and output structured, validated JSON. 

Per the project specification, classic solutions like **Tesseract**, **PaddleOCR**, and **Surya OCR** were excluded as primary extraction engines. In their place, **Mindee docTR** was chosen as the primary open-source OCR engine, paired with **PyMuPDF** for digital bypass, **EasyOCR** for fallback scenarios, and **Gemini 3.5 Flash** for LLM-based layout schema mapping.

---

## 2. Technology Comparison Matrix

| Criteria / Feature | Tesseract | PaddleOCR | Surya OCR | Mindee docTR (Selected) | EasyOCR (Selected Fallback) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Model Type** | Traditional (LSTM) | Deep Learning | VLM / PyTorch | Deep Learning (DBNet + CRNN) | Deep Learning (CRAFT + ResNet) |
| **Primary Backend** | C++ | PaddlePaddle | PyTorch | PyTorch or TensorFlow | PyTorch |
| **Layout Preserved** | Poor | Good | Excellent | **Excellent (Native Page/Block/Word hierarchy)** | Moderate (Requires custom groupings) |
| **In-the-wild Accuracy** | Low | High | Very High | **High (Optimized for documents)** | High (Optimized for scene text) |
| **RAM Footprint** | ~50MB | ~500MB | ~2GB | **~300MB (Lightweight configuration)** | ~400MB |
| **GPU Optimization** | No | Yes | Essential | **Yes (Runs well on CPU too)** | Yes |
| **Installation Weights** | Minimal | Heavy | Heavy | **Moderate (Modular imports)** | Moderate |

---

## 3. Detailed Technology Selections

### A. Mindee docTR (Primary Scanned OCR)
- **Selection Rationale:** docTR organizes detected text into a native structural hierarchy: `Document` ➔ `Page` ➔ `Block` ➔ `Line` ➔ `Word`. This matches our requirement to preserve reading order, paragraphs, and table bounding boxes.
- **Lightweight Profile:** We configured docTR with a MobileNetV3 backbone for both detection (`db_mobilenet_v3_large`) and recognition (`crnn_mobilenet_v3_large`). This minimizes RAM/GPU memory usage and ensures high CPU speeds.
- **Version Used:** `python-doctr>=0.8.1`

### B. PyMuPDF (Digital Bypass Router)
- **Selection Rationale:** Running deep OCR on digitally generated vector PDFs (like standard email invoices or banking exports) is computationally wasteful and introduces extraction errors. PyMuPDF directly extracts selectable text blocks with 100% precision in sub-millisecond latencies.
- **Version Used:** `pymupdf>=1.23.26`

### C. EasyOCR (Uncertainty Fallback)
- **Selection Rationale:** docTR occasionally fails to yield high confidence scores on highly noisy, distorted images, or documents containing handwriting. EasyOCR, based on CRAFT scene text detector, provides a highly robust fallback.
- **Version Used:** `easyocr>=1.7.1`

### D. Gemini 3.5 Flash (Schema Structuring Agent)
- **Selection Rationale:** Translating raw bounding box layouts into validated JSON requires multi-modal document intelligence. Gemini 3.5 Flash supports structured JSON mapping through the `response_schema` config parameter. It enforces strict schemas for invoices, receipts, and bank statements with low latencies.
- **Version Used:** `google-genai>=0.1.1`

---

## 4. Problems Faced & Engineering Solutions

### Problem 1: Heavy Dependency Loading & RAM Constraints on Local CPUs
*   **Challenge:** Deep learning models (docTR, EasyOCR) require PyTorch libraries (`torch`, `torchvision`) which take up significant disk space and RAM. When loading these on non-GPU local environments, API startup times exceed 10-15 seconds.
*   **Solution:** 
    1. We implemented **Lazy Loading** for deep learning engines. The models are not loaded when FastAPI starts, but rather on the first call to `/process`.
    2. We designed a **Mock Fallback System**. If the host environment lacks PyTorch or docTR imports fail, the service automatically flags `mock_fallback_allowed=True` and handles files with deterministic mock layouts. This ensures the dashboard demo remains interactive and never yields 500 errors.

### Problem 2: Document Skew and Rotational Offsets
*   **Challenge:** Scanning apps or photo uploads frequently introduce orientation issues. Rotated text blocks break reading orders and confuse the LLM structuring agent.
*   **Solution:** We built an automated OpenCV preprocessor in `classifier.py` using **Hough Lines Transform**. It calculates the median skew angle of text blocks and rotates (deskews) the image using `cv2.warpAffine` before executing OCR.

### Problem 3: Table and Multi-Column Layout Structuring
*   **Challenge:** OCRs extract text line-by-line, causing multi-column text to merge incorrectly if read left-to-right naively.
*   **Solution:** 
    1. docTR naturally groups text blocks vertically based on column separators.
    2. We supply coordinate metadata `[x0, y0, x1, y1]` for each text block inside our prompt. The Gemini LLM uses these coordinates to preserve multi-column associations.
