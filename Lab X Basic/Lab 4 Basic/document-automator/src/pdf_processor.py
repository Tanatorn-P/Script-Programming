# document-automator/src/pdf_processor.py
from PyPDF2 import PdfReader, PdfWriter
import os
from utils import setup_logging

logger = setup_logging(__name__)

class PDFProcessor:
    """จัดการการทำงานกับไฟล์ PDF โดยใช้ PyPDF2"""
    def __init__(self):
        logger.info("PDFProcessor initialized.")

    def extract_text_from_pdf(self, pdf_path):
        """ดึงข้อความทั้งหมดจากไฟล์ PDF ที่กำหนด"""
        if not os.path.exists(pdf_path):
            logger.error(f"PDF file not found: {pdf_path}")
            return None
        
        text_content = ""
        try:
            reader = PdfReader(pdf_path)
            num_pages = len(reader.pages)
            logger.info(f"Extracting text from '{pdf_path}' ({num_pages} pages)...")
            for page_num in range(num_pages):
                page = reader.pages[page_num]
                text_content += page.extract_text() + "\n--- Page End ---\n"
            logger.info(f"Successfully extracted text from '{pdf_path}'.")
            return text_content
        except Exception as e:
            logger.error(f"Error extracting text from '{pdf_path}': {e}")
            return None

    def merge_pdfs(self, pdf_paths, output_path):
        """รวมไฟล์ PDF หลายๆ ไฟล์เป็นไฟล์เดียว"""
        if not pdf_paths:
            logger.warning("No PDF paths provided for merging.")
            return False
            
        writer = PdfWriter()
        logger.info(f"Merging PDFs into '{output_path}'...")
        
        for pdf_path in pdf_paths:
            if not os.path.exists(pdf_path):
                logger.warning(f"Skipping non-existent PDF for merging: {pdf_path}")
                continue
            try:
                reader = PdfReader(pdf_path)
                for page in reader.pages:
                    writer.add_page(page)
                logger.info(f"Added '{pdf_path}' to merge queue.")
            except Exception as e:
                logger.error(f"Error reading PDF '{pdf_path}' for merging: {e}")
                continue
                
        if len(writer.pages) == 0:
            logger.warning("No pages were added to the merged PDF.")
            return False
            
        try:
            with open(output_path, 'wb') as f:
                writer.write(f)
            logger.info(f"PDFs successfully merged to '{output_path}'.")
            return True
        except Exception as e:
            logger.error(f"Error writing merged PDF to '{output_path}': {e}")
            return False