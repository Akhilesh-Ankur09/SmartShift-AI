from fastapi import FastAPI
from api.routes import transcription

app = FastAPI(
    title="SmartShift-AI Backend",
    description="AI-powered meeting summarization and reporting system",
    version="0.1.0"
)

# include routes
app.include_router(transcription.router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "SmartShift-AI Backend running successfully!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
