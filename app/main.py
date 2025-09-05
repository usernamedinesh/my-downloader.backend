from fastapi import FastAPI
from app.api.v1 import health, instagram

app = FastAPI()

# Include the health router
app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(instagram.router, prefix="/instagram", tags=["instagram"])
