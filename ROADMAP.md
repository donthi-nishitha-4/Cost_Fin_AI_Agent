# Roadmap

## Phase 1 - Foundation ✅

* FastAPI backend
* Finance APIs
* Agent orchestration
* Tool registry
* LangChain integration
* Ollama integration

---

## Phase 2 - Feature Expansion ✅

* Budget comparison
* Overrun risk analysis
* Financial summary
* Response formatting
* Error handling
* Automated testing

---

## Phase 3 - Persistence Layer ✅

* SQLite foundation
* SQLAlchemy integration
* Repository abstraction
# Roadmap

## Phase 1 - Foundation ✅

* FastAPI backend
* Finance APIs
* Agent orchestration
* Tool registry
* LangChain integration
* Ollama integration

---

## Phase 2 - Feature Expansion ✅

* Budget comparison
* Overrun risk analysis
* Financial summary
* Response formatting
* Error handling
* Automated testing

---

## Phase 3 - Persistence Layer ✅

* SQLite foundation
* SQLAlchemy integration
* Repository abstraction
* Configuration management
* Database initialization tooling
* PostgreSQL migration and validation

---

## 🟢 Phase 4: Production Readiness & Observability (Completed)

- **Agent V2 Migration**: Move from linear `AgentExecutor` to LangGraph `StateGraph`.
- **Validation Node**: Create a validation node to catch LLM hallucinations.
- **LangSmith Tracing**: Integrate `LANGCHAIN_TRACING_V2` for full request observability.
- **Evaluation Pipeline**: Build `evaluate_v2.py` with an LLM-as-a-Judge semantic grader.
- **Automated Reporting**: Build `generate_report.py` to auto-generate markdown reports from LangSmith.
- **Scale Up**: Expand the mock dataset to 100 items and hit 100% test coverage with PostgreSQL.

## 🟡 Phase 5: System-Wide Analytics & Async Architecture (Next)

- **Aggregate Analytical Tool (Text-to-SQL)**: Based on the V2 semantic evaluation (77/100), the agent failed exactly 23 system-wide queries (e.g., "Find all severe overruns"). Phase 5 will introduce an aggregation tool to dynamically query PostgreSQL instead of relying on a single `subsystem_id`.
- **Planner Routing**: Teach the Planner node to route aggregate queries away from specific ID tools, fixing the bug where the planner hallucinates `subsystem_id: 1` as a default.
- **Async Migration**: Convert the core API to fully asynchronous operations.

---

## Future Enhancements

* Multi-agent finance orchestration
* Advanced financial forecasting
* Real project data integrations
