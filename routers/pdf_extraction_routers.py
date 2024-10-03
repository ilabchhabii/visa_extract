from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Request
from typing import Annotated
from sqlalchemy.orm import Session
from app.db_utils import get_session
from auth.api_header import get_client_api
from llm.text_to_json import completion
from extractors.pdf_extractors import extract_text_from_pdf
from tempfile import NamedTemporaryFile
import os
from utils.rate_limit_validator import rate_limit_validator

pdf_extraction_router = APIRouter(tags=["PDF Extraction"])


@pdf_extraction_router.post("/pdf_to_json")
async def pdf_to_json(
    request: Request,
    api_key_obj: Annotated[str, Depends(get_client_api)],
    request_allowed: Annotated[bool, Depends(rate_limit_validator)],
    pdf_file: UploadFile = File(...),
    db: Session = Depends(get_session),
):
    with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        temp_pdf.write(pdf_file.file.read())
        temp_pdf_path = temp_pdf.name

    try:
        text = extract_text_from_pdf(temp_pdf_path)
        output, cost, input_tokens, output_tokens = completion(request, text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        os.remove(temp_pdf_path)
    return {
        "message": "PDF text extracted successfully",
        "total_cost": cost,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "extracted_text": output,
    }
