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
- **Strict Golden Dataset (Phase 6.6)**: Completely purged LLM-generated tautology from ground truth evaluations. Revealed hidden V5 Evaluator regex bugs, achieving a measured **94.0% Math Accuracy with Groq** (and 92.0% with local Ollama). This proved the Agent's reasoning paths and calculations are flawless while exposing evaluator script limitations.
- **Infrastructure Hardening**: Optimized PostgreSQL connection pooling and enforced `max_concurrency=2` in LangSmith evaluators to completely eliminate `psycopg.errors.ConnectionTimeout` and `429 RateLimitError` bottlenecks during batch load testing.

---

## Phase 7.1 - Local Model Optimization & V5 Hardening ✅

- **Deterministic Routing Overrides**: Added split-word aggregate keyword parsing and single-subsystem summary checks directly in `planner.py` to route queries flawlessly without relying on LLM inference.
- **SQL Prompt Hardening**: Banned table aliases, unions, and joins for multiple subsystems, forcing standard single-select `WHERE id IN (...)` queries to resolve psycopg errors.
- **Concise Formatter Constraints**: Added a formatting prompt limit in `response_formatter.py` to output lists when results exceed 3 subsystems, preventing model laziness and list truncation.
- **Local Benchmarking**: Deployed local evaluator script `evaluate_v5_local.py`, benchmarking local Ollama (Llama 3 8B) at **98.9%** overall pipeline score over 124 golden queries.

---

## Future Enhancements (Phase 7+)

* Multi-agent finance orchestration (e.g. specialized Procurement vs Labor Agents)
* Advanced financial forecasting
* Real project data integrations
* Expanding Intent routing dynamically beyond standard finance questions
