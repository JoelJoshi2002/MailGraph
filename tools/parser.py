import pymupdf
import os

class FormParser:
    def __init__(self, forms_dir: str):
        self.forms_dir = forms_dir

    def extract_text_from_pdf(self, filename: str) -> str:
        """Extracts raw text from a standard PDF form."""
        filepath = os.path.join(self.forms_dir, filename)
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Form not found at {filepath}")

        # Open the document
        doc = pymupdf.open(filepath)
        extracted_text = ""
        
        try:
            for page in doc:
                # Extracts plain text with line breaks
                extracted_text += page.get_text("text") + "\n"
        finally:
            doc.close()
            
        # Clean up excessive whitespace
        return " ".join(extracted_text.split())