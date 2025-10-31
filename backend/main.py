# backend/main.py
from fastapi import FastAPI

# Routers
from api.routes import transcription
from api.routes import intervals  # <-- interval endpoints

# Database: create tables at startup
from database.db import Base, engine
from database import models  # noqa: F401 (ensure models are imported so tables are created)


def create_tables() -> None:
    """Create all tables if they don't exist."""
    Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="SmartShift-AI Backend",
    description="AI-powered meeting summarization and reporting system",
    version="0.1.0",
)

# Optional: enable CORS now to make future Flutter/web work easier.
# You can restrict origins later.
try:
    from fastapi.middleware.cors import CORSMiddleware

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
except Exception:
    # If middleware import fails for any reason, just skip CORS.
    pass

# Ensure DB tables exist
create_tables()

# Include routes
app.include_router(transcription.router, prefix="/api", tags=["Transcription"])
app.include_router(intervals.router, prefix="/api", tags=["Intervals"])


@app.get("/", tags=["Health"])
async def root():
    return {"message": "SmartShift-AI Backend running successfully!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
