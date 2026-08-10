from app.core.logger import logger

class OCRMerger:
    """
    Layout-aware spatial merger that combines the outputs of two OCR engines 
    (e.g., RapidOCR and EasyOCR) to maximize text coverage and resolve overlap.
    """

    @staticmethod
    def merge(result_a: dict, result_b: dict) -> dict:
        """
        Merge two standard OCR extraction structures.
        If a text block in result_b overlaps heavily with a block in result_a,
        we keep the one with higher confidence. Non-overlapping blocks are combined.
        The merged blocks are then sorted by logical reading order (top-to-bottom, left-to-right).
        """
        logger.info(f"Merging OCR results from: '{result_a.get('engine')}' and '{result_b.get('engine')}'")
        
        merged_result = {
            "engine": f"Merged ({result_a.get('engine')} + {result_b.get('engine')})",
            "pages": [],
            "raw_text": ""
        }
        
        pages_a = result_a.get("pages", [])
        pages_b = result_b.get("pages", [])
        
        # Determine number of pages to process
        num_pages = max(len(pages_a), len(pages_b))
        
        full_text_list = []
        
        for p_idx in range(num_pages):
            page_a = pages_a[p_idx] if p_idx < len(pages_a) else None
            page_b = pages_b[p_idx] if p_idx < len(pages_b) else None
            
            # Use dimensions from page_a if available, otherwise page_b
            dimensions = {"width": 1000.0, "height": 1400.0}
            if page_a:
                dimensions = page_a.get("dimensions", dimensions)
            elif page_b:
                dimensions = page_b.get("dimensions", dimensions)
                
            blocks_a = page_a.get("blocks", []) if page_a else []
            blocks_b = page_b.get("blocks", []) if page_b else []
            
            merged_blocks = []
            used_b_indices = set()
            
            for b_a in blocks_a:
                box_a = b_a.get("bbox", [0, 0, 0, 0])
                text_a = b_a.get("text", "")
                conf_a = b_a.get("confidence", 0.0)
                
                # Check for overlapping blocks in blocks_b
                overlapping_b_idx = None
                max_overlap_ratio = 0.0
                
                for idx_b, b_b in enumerate(blocks_b):
                    if idx_b in used_b_indices:
                        continue
                        
                    box_b = b_b.get("bbox", [0, 0, 0, 0])
                    
                    # Calculate overlap
                    overlap_ratio = OCRMerger._calculate_box_overlap(box_a, box_b)
                    if overlap_ratio > 0.5 and overlap_ratio > max_overlap_ratio:
                        overlapping_b_idx = idx_b
                        max_overlap_ratio = overlap_ratio
                
                if overlapping_b_idx is not None:
                    # Resolve conflict: keep higher confidence block
                    b_b = blocks_b[overlapping_b_idx]
                    conf_b = b_b.get("confidence", 0.0)
                    used_b_indices.add(overlapping_b_idx)
                    
                    if conf_b > conf_a:
                        merged_blocks.append(b_b)
                    else:
                        merged_blocks.append(b_a)
                else:
                    merged_blocks.append(b_a)
            
            # Add remaining non-overlapping blocks from B
            for idx_b, b_b in enumerate(blocks_b):
                if idx_b not in used_b_indices:
                    merged_blocks.append(b_b)
            
            # Sort merged blocks by logical reading order (top-to-bottom, then left-to-right)
            merged_blocks.sort(key=lambda b: (b.get("bbox", [0, 0, 0, 0])[1], b.get("bbox", [0, 0, 0, 0])[0]))
            
            merged_result["pages"].append({
                "page_idx": p_idx,
                "dimensions": dimensions,
                "blocks": merged_blocks
            })
            
            # Reconstruct raw text
            page_text = "\n".join([b.get("text", "") for b in merged_blocks])
            full_text_list.append(page_text)
            
        merged_result["raw_text"] = "\n\n".join(full_text_list)
        logger.info(f"OCR merge complete. Total merged blocks: {sum(len(p.get('blocks', [])) for p in merged_result['pages'])}")
        return merged_result

    @staticmethod
    def _calculate_box_overlap(box_a: list, box_b: list) -> float:
        """
        Calculates containment/intersection ratio between two boxes.
        Returns the overlap area divided by the area of the smaller box.
        """
        x0_a, y0_a, x1_a, y1_a = box_a
        x0_b, y0_b, x1_b, y1_b = box_b
        
        # Find intersection
        x0_i = max(x0_a, x0_b)
        y0_i = max(y0_a, y0_b)
        x1_i = min(x1_a, x1_b)
        y1_i = min(y1_a, y1_b)
        
        if x1_i <= x0_i or y1_i <= y0_i:
            return 0.0
            
        inter_area = (x1_i - x0_i) * (y1_i - y0_i)
        
        area_a = (x1_a - x0_a) * (y1_a - y0_a)
        area_b = (x1_b - x0_b) * (y1_b - y0_b)
        
        min_area = min(area_a, area_b)
        if min_area <= 0.0:
            return 0.0
            
        return inter_area / min_area
