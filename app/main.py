from fastapi import FastAPI
from app.agents.finance_agent import ask_finance_agent

app = FastAPI(title="Cost Finance AI Agent")


@app.get("/agent")
def finance_agent(query: str):

    result = ask_finance_agent(query)

    return {
        "query": query,
        "result": result
    }