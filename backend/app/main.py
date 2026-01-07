from fastapi import FastAPI
from app.api.endpoints import router as api_router

app = FastAPI(title="Code Analytics API")

app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to Code Analytics API"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
