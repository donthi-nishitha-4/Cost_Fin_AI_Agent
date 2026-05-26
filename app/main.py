from fastapi import FastAPI

from app.api.v1.endpoints.subsystem_routes import (
    router as subsystem_router
)

from app.agents.finance_agent import (
    ask_finance_agent
)

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


@app.get("/agent")
def finance_agent(query: str):

    result = ask_finance_agent(query)

    return {
        "query": query,
        "response": result
    }


app.include_router(
    subsystem_router,
    prefix="/api/v1"
)