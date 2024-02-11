from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import auth
from settings import settings
from utils.logger import logger

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(auth.router)


@app.get(path="/")
async def home():
    response = {"status": "OK"}
    logger.success(f"GET / {response}")
    return response


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=settings.API_HOST, port=settings.API_PORT)
