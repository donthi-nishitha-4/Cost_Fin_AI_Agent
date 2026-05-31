from fastapi import FastAPI

from app.agents.finance_agent import ask_finance_agent
from app.api.v1.endpoints.subsystem_routes import router as subsystem_router
from app.core.error_handler import global_exception_handler
from app.core.request_context import request_context_middleware
from app.core.settings import settings

app = FastAPI(title=settings.project_name)
app.add_exception_handler(Exception, global_exception_handler)
app.middleware("http")(request_context_middleware)
app.include_router(subsystem_router, prefix="/api/v1", tags=["finance"])


@app.get("/")
def health_check():
    return {
        "status": "running",
        "service": settings.project_name,
        "environment": settings.environment
    }


@app.get("/agent")
def finance_agent(query: str):
    result = ask_finance_agent(query)
    answer = result.pop("answer", None)

    return {
        "query": query,
        "answer": answer,
        "result": result
    }