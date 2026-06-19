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

## Phase 4: Production Readiness & Observability ✅

- **Agent V2 Migration**: Move from linear `AgentExecutor` to LangGraph `StateGraph`.
- **Validation Node**: Catch LLM hallucinations.
- **LangSmith Tracing**: Full request observability.
- **Evaluation Pipeline**: Semantic grader.
- **Automated Reporting**: Auto-generate markdown reports from LangSmith.

---

## Phase 5: System-Wide Analytics & Hardened Evaluation ✅

- **Aggregate Analytical Tool (Text-to-SQL)**: Dynamically queries PostgreSQL for system-wide insights instead of failing on missing `subsystem_id`s.
- **Planner CoT Routing**: Taught the Planner node to handle aggregate queries safely.
- **Async & Connection Handling**: Fixed connection exhaustion during external API calls.
- **Evaluation Hardening (V4/V5)**: Deployed Project-Grade 5-Layer Evaluator tracking Intent Classification, Targeted Extraction, Deterministic Math, and Business Logic safely independently from the Semantic LLM-as-a-judge.

---

## Phase 6: Cloud LLM Migration & Benchmarking ✅

- **Dynamic LLM Factory**: `app/core/llm_factory.py` implemented to instantly swap between `OllamaLLM` and `ChatGroq`.
- **Groq Integration**: Migrated to `llama-3.1-8b-instant` for blazing-fast 1.41s latency responses.
- **LLM Shootout Benchmarking**: Proved an 8.8x inference speedup and a 20% jump in deterministic accuracy (from 43% to 63%) just by upgrading the model endpoint.

---

## Future Enhancements (Phase 7+)

* Multi-agent finance orchestration (e.g. specialized Procurement vs Labor Agents)
* Advanced financial forecasting
* Real project data integrations
* Expanding Intent routing dynamically beyond standard finance questions
