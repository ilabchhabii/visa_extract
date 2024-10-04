import uvicorn

from database import engine
from models.base import Base
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils import routers_util
from utils.custom_exception import register_app
app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

routers_util.include_routers(app)
register_app(app)

@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=9000,
        reload=True,
    )
