# uvicorn main:app --reload - команда для запуска
# http://127.0.0.1:8000/docs - swagger

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.routers import api_router
import uvicorn


app = FastAPI(
    title="Kitchenware store",
    description="Сайт онлайн-магазина",
    version="1.0.0",
    debug=False 
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Укажите домен вашего фронтенда
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST, PUT, DELETE и т.д.)
    allow_headers=["*"],  # Разрешить все заголовки
)

app.include_router(api_router, prefix="/api")

@app.get("/")
async def index():
    return {"message": "открытый API, для доступа к swagger - /docs"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)