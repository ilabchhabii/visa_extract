from utils.custom_exception import CustomException
from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception:
        raise CustomException(
            message="Failed to extract text from PDF",
            data="",
            status_code=500,
        )
