from fastapi import FastAPI

app = FastAPI(
    title="Cost Finance AI Agent",
    version="1.0.0"
)

@app.get("/")
def health_check():
    return {
        "status": "running",
        "service": "Cost Finance AI Agent"
    }