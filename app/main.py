from fastapi import FastAPI
from .routers import documents

app = FastAPI(
    title="CSA Data Store API",
    description="API to access ERP data stored in MongoDB.",
    version="0.1.0",
)

app.include_router(documents.router)


@app.get("/")
async def root():
    return {"message": "Welcome to the CSA Data API"}
