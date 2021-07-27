from fastapi import FastAPI
import uvicorn
from motor.motor_asyncio import AsyncIOMotorClient
from config import settings

from apps.todo.routers import router as todo_router

app = FastAPI()


@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(settings.DB_URL)
    app.mongodb = app.mongodb_client[settings.DB_NAME]


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(todo_router, tags=["api"], prefix="/api")


if __name__ == "__main__":
    print("=======================================")
    print("HOST: " + settings.HOST)
    print("PORT: " + str(settings.PORT))
    print("=======================================")
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        reload=settings.DEBUG_MODE,
        port=settings.PORT,
    )
