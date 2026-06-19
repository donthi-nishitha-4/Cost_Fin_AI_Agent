import os
from dotenv import load_dotenv

# Load environment variables (including LangSmith tracing setup)
load_dotenv()

from app.agents.finance_agent_v2 import ask_finance_agent_v2

def main():
    print("Testing Agent V2...")
    
    # Example query
    query = "What is the cost breakdown for subsystem 1?"
    print(f"\nQuery: {query}")
    
    response = ask_finance_agent_v2(query)
    
    print("\nFinal Response:")
    import json
    print(json.dumps(response, indent=2))
    print("\nIf tracing is active, check your LangSmith dashboard to see the trace!")

if __name__ == "__main__":
    main()
