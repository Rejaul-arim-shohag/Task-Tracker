
from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.database.db import connection

app = FastAPI()
app.include_router(auth_router)


@app.get("/")
def home():
    return {"message": "API is running"}
