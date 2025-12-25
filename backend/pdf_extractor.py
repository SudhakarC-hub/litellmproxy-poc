"""
PDF Text Extraction Utility

This module provides functionality to extract text from PDF files using PyMuPDF (fitz).
"""

import fitz  # PyMuPDF
from typing import Optional


class PDFExtractor:
    """Extract text content from PDF files."""
    
    @staticmethod
    def extract_text(pdf_path: str) -> str:
        """
        Extract all text from a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text as a string
            
        Raises:
            ValueError: If the PDF is invalid or cannot be read
            Exception: For other PDF processing errors
        """
        try:
            # Open the PDF file
            doc = fitz.open(pdf_path)
            
            # Extract text from all pages
            text_content = []
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text()
                if text.strip():  # Only add non-empty pages
                    text_content.append(f"--- Page {page_num + 1} ---\n{text}")
            
            doc.close()
            
            if not text_content:
                raise ValueError("No text content found in PDF")
            
            return "\n\n".join(text_content)
            
        except fitz.FileDataError as e:
            raise ValueError(f"Invalid or corrupted PDF file: {str(e)}")
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    @staticmethod
    def get_page_count(pdf_path: str) -> int:
        """
        Get the number of pages in a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Number of pages in the PDF
        """
        try:
            doc = fitz.open(pdf_path)
            page_count = len(doc)
            doc.close()
            return page_count
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
