"""
Lab Report Processor for extracting biomarker data from PDF and image files
"""

import PyPDF2
import pytesseract
from PIL import Image
import cv2
import numpy as np
import re
from typing import Dict, List, Optional, Tuple
import io
import base64

class LabReportProcessor:
    def __init__(self):
        self.biomarker_patterns = {
            'hemoglobin': r'(?i)(hemoglobin|hb|hgb)[\s:]*(\d+\.?\d*)\s*(g/dl|g/dL)',
            'glucose': r'(?i)(glucose|glu)[\s:]*(\d+\.?\d*)\s*(mg/dl|mg/dL)',
            'hba1c': r'(?i)(hba1c|hb a1c|glycated hemoglobin)[\s:]*(\d+\.?\d*)\s*(%|percent)',
            'total_cholesterol': r'(?i)(total cholesterol|chol)[\s:]*(\d+\.?\d*)\s*(mg/dl|mg/dL)',
            'ldl': r'(?i)(ldl|lld cholesterol)[\s:]*(\d+\.?\d*)\s*(mg/dl|mg/dL)',
            'hdl': r'(?i)(hdl|hld cholesterol)[\s:]*(\d+\.?\d*)\s*(mg/dl|mg/dL)',
            'triglycerides': r'(?i)(triglycerides|tg)[\s:]*(\d+\.?\d*)\s*(mg/dl|mg/dL)',
            'tsh': r'(?i)(tsh|thyroid stimulating hormone)[\s:]*(\d+\.?\d*)\s*(mIU/L|mIU/ml|uIU/mL)',
            't3': r'(?i)(t3|triiodothyronine)[\s:]*(\d+\.?\d*)\s*(ng/dl|ng/dL)',
            't4': r'(?i)(t4|thyroxine|free t4)[\s:]*(\d+\.?\d*)\s*(ng/dl|ng/dL)',
            'creatinine': r'(?i)(creatinine|creat)[\s:]*(\d+\.?\d*)\s*(mg/dl|mg/dL)',
            'vitamin_d': r'(?i)(vitamin d|25-oh vitamin d|25ohd)[\s:]*(\d+\.?\d*)\s*(ng/ml|ng/mL)',
            'crp': r'(?i)(crp|c-reactive protein)[\s:]*(\d+\.?\d*)\s*(mg/l|mg/L)',
            'esr': r'(?i)(esr|erythrocyte sedimentation rate)[\s:]*(\d+\.?\d*)\s*(mm/hr|mm/h)',
            'wbc': r'(?i)(wbc|white blood cells|leukocytes)[\s:]*(\d+\.?\d*)\s*(/ul|/μL|10e9/L)',
            'rbc': r'(?i)(rbc|red blood cells|erythrocytes)[\s:]*(\d+\.?\d*)\s*(million/ul|million/μL)',
            'platelets': r'(?i)(platelets|plt)[\s:]*(\d+\.?\d*)\s*(/ul|/μL|thousand/ul)',
            'mcv': r'(?i)(mcv|mean corpuscular volume)[\s:]*(\d+\.?\d*)\s*(fl|fL)',
            'iron': r'(?i)(serum iron|iron)[\s:]*(\d+\.?\d*)\s*(μg/dl|mcg/dl|ug/dl)',
            'ferritin': r'(?i)(ferritin)[\s:]*(\d+\.?\d*)\s*(ng/ml|ng/mL)'
        }
    
    def process_pdf(self, pdf_content: bytes) -> Dict[str, float]:
        """Extract biomarker data from PDF content"""
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
            text = ""
            
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return self._extract_biomarkers_from_text(text)
        except Exception as e:
            print(f"Error processing PDF: {e}")
            return {}
    
    def process_image(self, image_content: bytes) -> Dict[str, float]:
        """Extract biomarker data from image content using OCR"""
        try:
            # Load image
            image = Image.open(io.BytesIO(image_content))
            
            # Convert to OpenCV format
            cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Preprocess image for better OCR
            processed_image = self._preprocess_image_for_ocr(cv_image)
            
            # Perform OCR
            text = pytesseract.image_to_string(processed_image)
            
            return self._extract_biomarkers_from_text(text)
        except Exception as e:
            print(f"Error processing image: {e}")
            return {}
    
    def _preprocess_image_for_ocr(self, image: np.ndarray) -> np.ndarray:
        """Preprocess image to improve OCR accuracy"""
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Apply threshold to get binary image
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Morphological operations to clean up the image
        kernel = np.ones((1, 1), np.uint8)
        cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
        return cleaned
    
    def _extract_biomarkers_from_text(self, text: str) -> Dict[str, float]:
        """Extract biomarker values from text using regex patterns"""
        biomarkers = {}
        
        for biomarker_name, pattern in self.biomarker_patterns.items():
            matches = re.findall(pattern, text)
            
            if matches:
                # Take the first match
                match = matches[0]
                try:
                    value = float(match[1])
                    biomarkers[biomarker_name] = value
                except (ValueError, IndexError):
                    continue
        
        return biomarkers
    
    def process_base64_file(self, base64_content: str, file_type: str) -> Dict[str, float]:
        """Process base64 encoded file content"""
        try:
            # Decode base64 content
            file_content = base64.b64decode(base64_content)
            
            if file_type.lower() == 'pdf':
                return self.process_pdf(file_content)
            elif file_type.lower() in ['jpg', 'jpeg', 'png', 'bmp', 'tiff']:
                return self.process_image(file_content)
            else:
                print(f"Unsupported file type: {file_type}")
                return {}
        except Exception as e:
            print(f"Error processing base64 file: {e}")
            return {}
    
    def validate_biomarker_values(self, biomarkers: Dict[str, float]) -> Dict[str, Dict]:
        """Validate and categorize biomarker values"""
        validated = {}
        
        # Define reasonable ranges for validation
        validation_ranges = {
            'hemoglobin': (6.0, 20.0),
            'glucose': (50.0, 500.0),
            'hba1c': (3.0, 15.0),
            'total_cholesterol': (100.0, 500.0),
            'ldl': (50.0, 300.0),
            'hdl': (20.0, 100.0),
            'triglycerides': (50.0, 1000.0),
            'tsh': (0.1, 50.0),
            't3': (50.0, 300.0),
            't4': (0.5, 20.0),
            'creatinine': (0.3, 10.0),
            'vitamin_d': (5.0, 150.0),
            'crp': (0.1, 50.0),
            'esr': (1.0, 100.0),
            'wbc': (1.0, 50.0),
            'rbc': (2.0, 8.0),
            'platelets': (50.0, 1000.0),
            'mcv': (60.0, 120.0),
            'iron': (20.0, 300.0),
            'ferritin': (5.0, 1000.0)
        }
        
        for biomarker, value in biomarkers.items():
            if biomarker in validation_ranges:
                min_val, max_val = validation_ranges[biomarker]
                if min_val <= value <= max_val:
                    validated[biomarker] = {
                        'value': value,
                        'status': 'valid',
                        'range': (min_val, max_val)
                    }
                else:
                    validated[biomarker] = {
                        'value': value,
                        'status': 'out_of_range',
                        'range': (min_val, max_val),
                        'note': f"Value {value} is outside typical range {min_val}-{max_val}"
                    }
            else:
                validated[biomarker] = {
                    'value': value,
                    'status': 'unknown_range',
                    'note': 'No validation range defined'
                }
        
        return validated
    
    def get_extraction_summary(self, biomarkers: Dict[str, float]) -> Dict:
        """Get summary of extracted biomarkers"""
        return {
            'total_biomarkers_found': len(biomarkers),
            'biomarkers': list(biomarkers.keys()),
            'values': biomarkers,
            'extraction_timestamp': self._get_current_timestamp()
        }
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
