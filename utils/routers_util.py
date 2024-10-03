from fastapi import FastAPI
from routers import (
    pdf_extraction_router,
)


def include_routers(app: FastAPI):
    app.include_router(pdf_extraction_router)
