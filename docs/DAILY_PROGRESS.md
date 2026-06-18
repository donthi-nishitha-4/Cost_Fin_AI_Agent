# Daily Progress Log

This document serves as a chronological record of the development journey for the Cost Finance AI Agent. It acts as an ongoing Architecture Decision Record (ADR), capturing the reasoning behind key technical choices, unexpected challenges, and the step-by-step evolution of the system architecture.

## Historical Briefing (Pre-June 18, 2026)
Before advancing to Phase 4, the Cost Finance AI Agent established a robust foundation through three major phases of development:
- **Phase 1 (Foundation):** Set up the FastAPI backend, integrated the local Ollama LLM (Llama3) using LangChain, and established a modular architecture with structured logging and a Tool Registry.
- **Phase 2 (Finance Services):** Expanded the agent's capabilities to include advanced financial calculations (Budget Comparison, Overrun Risk Analysis, and Financial Summaries). Engineered a human-readable response formatter alongside structured JSON outputs.
- **Phase 3 (Persistence Layer):** Migrated from hardcoded mock data to an active PostgreSQL database using SQLAlchemy. Engineered automated schema creation, robust database seeding mechanisms, and a centralized `.env` configuration layer. Validated the migration with a comprehensive suite of 49 automated Pytest cases.

## June 18, 2026 - Phase 4: Advanced AI & Production Readiness

### Key Decisions Made
1. **LangGraph Over LangChain**: We made the architectural decision to migrate from a linear LangChain orchestrator to a `langgraph` StateGraph. 
   - *Why?* Linear LLM pipelines crash easily if the model hallucinates an invalid tool. By using a state graph (`finance_agent_v2.py`), we were able to introduce a `validator_node` that catches hallucinations and routes them back to the planner, creating a deterministic and safe execution loop.
   - *Result*: Zero backend crashes due to LLM parsing errors.

2. **LangSmith Tracing**: Instead of building custom logging for token usage and prompts, we opted to integrate LangSmith (`LANGCHAIN_TRACING_V2`).
   - *Why?* It provided a massive out-of-the-box UI to visualize the exact inputs/outputs of our local `llama3` model.
   - *Result*: We used this UI immediately to debug an issue where the LLM hallucinated a `subsystem_id: 1` instead of extracting the correct ID for "Security".

3. **Semantic Evaluation (LLM-as-a-Judge)**: We discarded exact string matching for evaluation and wrote a custom semantic evaluator using a strictly-prompted Ollama instance.
   - *Why?* String matching failed when the database returned `over_budget` but the expected answer was `OVER BUDGET`. Semantic evaluation proves that the agent successfully extracted the correct financial intent, regardless of capitalization or phrasing.
   - *Result*: Achieved a production-grade evaluation pipeline capable of grading conversational responses.

4. **100-Item Realistic Dataset**: The user initiated a scale-up of the mock dataset from 3 items to 100 items.
   - *Why?* To stress-test the agent against extreme edge cases (massive budget overruns up to 180%, exact matches, and $0 planned budgets that cause division-by-zero errors in the backend).
   - *Result*: The expanded dataset successfully caught a hidden Python `ZeroDivisionError` in `finance_service.py` before it hit production.

### Code Changes & Betterments
- Created `finance_agent_v2.py` implementing the 4-node LangGraph logic.
- Expanded `mock_finance_data.py` edge cases, and subsequently migrated to the user-generated `evaluation_dataset_100.py`.
- Fixed `ZeroDivisionError` in `get_overrun_risk_from_db` by explicitly handling `planned_cost == 0`.
- Updated `planner.py` prompt to dynamically extract `subsystem_id` directly from user queries rather than relying on a hardcoded 1-6 mapping.
- Wrote `evaluate_v2.py` to automate testing against the LangSmith API.
- Re-wired `seed_database.py` to elegantly clear existing rows before seeding the new 100-item dataset.
- Completed comprehensive documentation updates across `README`, `ROADMAP`, `CHANGELOG`, `ARCHITECTURE_NOTES`, `PROJECT_PROGRESS`, `DEBUGGING_GUIDE`, and `API_CONTRACTS`.

### Next Steps
- **Evaluation Review**: The `generate_report.py` script outputted `docs/evaluation_reports/eval_report_v2_100.md`. The local Llama3 model scored exactly **77/100**. The 23 failures were exclusively aggregate analytical questions (e.g. "Find severe overruns").
- **Transition to Phase 5**: The agent needs a new System-Wide Analytics tool (Text-to-SQL) to process aggregate queries, breaking free from the single `subsystem_id` planner limitation. Phase 4 is now officially complete and all documentation is synced.
