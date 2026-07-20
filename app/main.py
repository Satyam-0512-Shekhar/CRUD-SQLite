from fastapi import FastAPI

from app.database import create_db_and_tables
from app.routers import tasks

app = FastAPI(
    title="Task API",
    version="1.0.0"
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(tasks.router)


@app.get("/")
def home():
    return {
        "message": "Task API is running"
    }