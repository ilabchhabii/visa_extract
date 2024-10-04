from llm.text_to_json import completion
from extractors.pdf_extractors import extract_text_from_pdf
from tempfile import NamedTemporaryFile
import os
from utils.custom_exception import CustomException
def pdf_to_json(request, pdf_file):
    

    try:
        with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(pdf_file.file.read())
            temp_pdf_path = temp_pdf.name
        text = extract_text_from_pdf(temp_pdf_path)
        output, cost, input_tokens, output_tokens = completion(request, text)
        return {
            "code": "SUCCESS",
            "message": "PDF text extracted successfully",
            "data": {
                "extracted_text": output,
            },
        }
    except Exception:
        raise CustomException(
            message="Unsupported file format",
            data="",
            status_code=500,
        )

    finally:
        os.remove(temp_pdf_path)
