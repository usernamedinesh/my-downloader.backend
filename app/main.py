from fastapi import FastAPI
from app.api.v1 import health  # make sure the import path matches your folder structure

# Initialize the FastAPI app
app = FastAPI()

# Include the health router
app.include_router(health.router, prefix="/health", tags=["Health"])

