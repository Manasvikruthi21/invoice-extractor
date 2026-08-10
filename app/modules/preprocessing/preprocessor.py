import os
import fitz  # PyMuPDF
import cv2
import numpy as np
from PIL import Image
from app.core.logger import logger
from app.modules.analyzer.classifier import DocumentClassifier

class DocumentPreprocessor:
    """
    Handles image preprocessing steps including:
    - PDF page rendering to images.
    - Skew angle detection using Hough Lines.
    - Image deskewing/rotation.
    - Aspect ratio and quality analysis.
    """
    
    @staticmethod
    def detect_skew_angle(image: np.ndarray) -> float:
        """
        Detect skew angle of a document image using OpenCV Hough Lines.
        Returns skew angle in degrees.
        """
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # Apply thresholding or Canny edge detection
            blur = cv2.GaussianBlur(gray, (9, 9), 0)
            thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
            
            # Dilate to merge text lines
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
            dilate = cv2.dilate(thresh, kernel, iterations=2)
            
            # Find all contours
            contours, _ = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            
            angles = []
            for contour in contours:
                area = cv2.contourArea(contour)
                if area < 1000:
                    continue
                # Get the min area rect
                rect = cv2.minAreaRect(contour)
                angle = rect[-1]
                
                # Format the angle based on minAreaRect returns
                if angle < -45:
                    angle = -(90 + angle)
                elif angle > 45:
                    angle = 90 - angle
                    
                angles.append(angle)
                
            if not angles:
                return 0.0
                
            median_angle = float(np.median(angles))
            # Filter out extreme angles
            if abs(median_angle) > 20.0:
                return 0.0
                
            return median_angle
        except Exception as e:
            logger.warning(f"Failed to detect skew angle: {str(e)}. Defaulting to 0.0")
            return 0.0

    @staticmethod
    def rotate_image(image: np.ndarray, angle: float) -> np.ndarray:
        """
        Rotate the image by a given angle (in degrees).
        """
        if abs(angle) < 0.1:
            return image
            
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        return rotated

    @classmethod
    def analyze_and_preprocess(cls, file_path: str, output_dir: str) -> dict:
        """
        Main preprocessing entry point.
        Analyzes document metadata, detects skew, deskews if necessary, and saves the preprocessed page images.
        Returns a dict of preprocessing results.
        """
        os.makedirs(output_dir, exist_ok=True)
        filename = os.path.basename(file_path)
        is_pdf = file_path.lower().endswith(".pdf")
        is_digital = DocumentClassifier.is_digital_pdf(file_path)
        
        result = {
            "original_filename": filename,
            "is_pdf": is_pdf,
            "is_digital": is_digital,
            "page_count": 0,
            "preprocessed_images": [],
            "skew_angles": [],
            "aspect_ratio": "portrait",
            "contrast_status": "good"
        }
        
        if is_pdf:
            if is_digital:
                # Get page count for digital PDF
                try:
                    doc = fitz.open(file_path)
                    result["page_count"] = len(doc)
                    doc.close()
                except Exception as e:
                    logger.error(f"Error reading PDF page count: {str(e)}")
                return result
                
            # Scanned PDF: Render pages as images
            try:
                doc = fitz.open(file_path)
                result["page_count"] = len(doc)
                
                for page_idx in range(len(doc)):
                    page = doc[page_idx]
                    # Render page to image (300 DPI for high quality OCR)
                    pix = page.get_pixmap(dpi=300)
                    image_path = os.path.join(output_dir, f"page_{page_idx}.png")
                    pix.save(image_path)
                    
                    # Preprocess the rendered page
                    img = cv2.imread(image_path)
                    if img is not None:
                        skew_angle = cls.detect_skew_angle(img)
                        result["skew_angles"].append(skew_angle)
                        
                        if abs(skew_angle) > 0.5:
                            logger.info(f"Deskewing page {page_idx} of {filename} by {skew_angle:.2f} degrees")
                            img = cls.rotate_image(img, skew_angle)
                            cv2.imwrite(image_path, img)
                            
                        result["preprocessed_images"].append(image_path)
                        
                        # Detect aspect ratio
                        h, w = img.shape[:2]
                        result["aspect_ratio"] = "landscape" if w > h else "portrait"
                    else:
                        logger.error(f"Failed to read rendered PDF page {page_idx} with OpenCV")
                doc.close()
            except Exception as e:
                logger.error(f"Error processing scanned PDF pages: {str(e)}")
        else:
            # Single Image file
            result["page_count"] = 1
            image_path = os.path.join(output_dir, "page_0.png")
            try:
                # Load with PIL and save to normalize formats
                img_pil = Image.open(file_path)
                img_pil.save(image_path)
                
                img = cv2.imread(image_path)
                if img is not None:
                    skew_angle = cls.detect_skew_angle(img)
                    result["skew_angles"].append(skew_angle)
                    
                    if abs(skew_angle) > 0.5:
                        logger.info(f"Deskewing image {filename} by {skew_angle:.2f} degrees")
                        img = cls.rotate_image(img, skew_angle)
                        cv2.imwrite(image_path, img)
                        
                    result["preprocessed_images"].append(image_path)
                    
                    h, w = img.shape[:2]
                    result["aspect_ratio"] = "landscape" if w > h else "portrait"
                else:
                    logger.error(f"Failed to read image with OpenCV: {file_path}")
            except Exception as e:
                logger.error(f"Error processing image {filename}: {str(e)}")
                
        return result
