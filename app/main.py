from fastapi import FastAPI
from app.api.v1 import health, instagram
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow origins (frontend URLs)
origins = [
    "http://localhost:5173",  # Vite dev server
    "http://127.0.0.1:5173",
    "https://your-production-domain.com",  # your prod site
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] to allow all origins (not recommended for prod)
    allow_credentials=True,
    allow_methods=["*"],    # ["GET", "POST", ...] if you want to restrict
    allow_headers=["*"],
)

# Include the health router
app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(instagram.router, prefix="/instagram", tags=["instagram"])
