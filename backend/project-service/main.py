import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from fastapi import FastAPI
from shared.utils import setup_logging
from project_service.routes import router as project_router

setup_logging(level=os.getenv("LOG_LEVEL", "INFO"))

app = FastAPI(title="Project Service", version="1.0.0")

app.include_router(project_router, prefix="/project", tags=["projects"])


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "project-service"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)