from app.agents.finance_agent_v2 import ask_finance_agent_v2

test_queries = [
    # 1. Tests Text-to-SQL Generation
    "Find severe overruns.",
    
    # 2. Tests the "equipment" routing fix we just made
    "Which subsystem is equipment-heavy, with equipment cost as the dominant cost component?",
    
    # 3. Tests the standard DB retrieval
    "What is the cost breakdown for subsystem 17?",
    
    # 4. Tests the Out-of-Scope Fallback
    "What is the weather in London?"
]

for q in test_queries:
    print(f"\n==============================================")
    print(f"QUERY: {q}")
    result = ask_finance_agent_v2(q)
    print(f"RESULT: {result.get('answer', str(result))}")
    print(f"==============================================\n")
