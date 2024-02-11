from fastapi import FastAPI

from routes import auth
from settings import settings
from utils.logger import logger

app = FastAPI()
app.include_router(auth.router)


@app.get(path="/")
async def home():
    response = {"status": "OK"}
    logger.success(f"GET / {response}")
    return response


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=settings.API_HOST, port=settings.API_PORT)
