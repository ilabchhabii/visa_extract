from fastapi import APIRouter, Depends, UploadFile, File, Request
from typing import Annotated
from sqlalchemy.orm import Session
from app.db_utils import get_session
from auth.api_header import get_client_api
from extractors.pdf_to_json import pdf_to_json
from utils.rate_limit_validator import rate_limit_validator

pdf_extraction_router = APIRouter(tags=["PDF Extraction"])


@pdf_extraction_router.post("/pdf_to_json")
async def pdf_to_json_router(
    request: Request,
    api_key_obj: Annotated[str, Depends(get_client_api)],
    request_allowed: Annotated[bool, Depends(rate_limit_validator)],
    pdf_file: UploadFile = File(...),
    db: Session = Depends(get_session),
):
    
    
    response = pdf_to_json(request, pdf_file)
    return response
    