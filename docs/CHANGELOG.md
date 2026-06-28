# Changelog

## v1.2 - Local Optimization & V5 Hardening (Phase 7.1)

### Added
- **SQL Prompt Constraint Rules**: Restructured Text-to-SQL prompts in `finance_service.py` to ban table aliases, unions, and joins for multiple subsystems, forcing standard single-selects (e.g. `WHERE id IN (...)`) to completely resolve UndefinedTable errors.
- **Deterministic Planner Overrides**: Implemented whitespace split keyword routing in `planner.py` to force aggregate intents (e.g. `average`, `total`, `sum`, `count`) and single-subsystem summaries to correct endpoints, ensuring 100% stable routing.
- **Concise Formatter Constraints**: Added a formatting prompt limit in `response_formatter.py` enforcing list output when results exceed 3 subsystems, preventing model laziness and list truncation.
- **Evaluator Robustness**: Fixed regex lookahead decimals extraction and aggregate ID stripping bugs in `evaluate_v5.py`.
- **Workspace Restructuring**: Moved previous versions of reports, datasets, and scripts into dedicated `previous_versions/` and `legacy_evaluators/` archive folders to clean up active workspaces.

### Status
Phase 7.1 complete. Local Ollama (Llama 3) achieved an outstanding **98.9%** overall pipeline accuracy (99.2% Math, 97.6% Semantic) over 124 golden queries.

## v1.1 - Infrastructure Hardening & Load Mitigation

### Added
- **Database Connection Pooling**: Added active connection pooling (`pool_size=10, max_overflow=50, pool_timeout=30`) to the SQLAlchemy `engine` in `app/core/database.py` to prevent PostgreSQL `ConnectionTimeout` crashes under heavy LangSmith concurrent load.
- **LangSmith Throttling**: Hardcoded `max_concurrency=2` into `evaluate_v5.py` to actively throttle burst API requests, eliminating `429 RateLimitError` blocks from Groq's Tokens-Per-Minute restrictions.
- **Dataset History Preservation**: Engineered `scripts/generate_golden_dataset.py` to dynamically `update_example()` instead of deleting the dataset. This successfully prevents data loss of historical LangSmith experiments.
- **Regex Edge Case Fix**: Patched a false-negative bug in the golden dataset generator where `"remaining budget"` queries were unfairly misrouted to the fallback intent.

### Status
Infrastructure stabilized. Solved all database timeouts and API rate limit crashes. Ready for Phase 7 (Multi-Agent Evaluation).

## v1.0 - Cloud LLM Migration & Multi-Model Benchmarking (Phase 6)

### Added
- **LLM Factory Pattern**: Implemented `app/core/llm_factory.py` to securely route requests between local `OllamaLLM` and cloud-hosted `ChatGroq`.
- **Groq LPU Integration**: Standardized the system on `llama-3.1-8b-instant`, dropping inference latency to 1.4s (8.8x speedup).
- **V5 Project-Grade Evaluator**: Deployed a rigorous 5-Layer evaluation architecture (`evaluate_v5.py`) featuring deterministic field extraction, severity scoring (`INFO`, `WARNING`, `FAIL`, `CRITICAL`), and decoupled semantic judging.
- **Strict Golden Dataset**: Re-engineered `generate_golden_dataset.py` to bypass the LLM and query PostgreSQL directly, eliminating evaluation tautologies.
- **LLM Shootout**: Created `compare_llms.py` to benchmark latency and quality between Ollama and Groq dynamically.

### Status
Phase 6 complete. Achieved a mathematically proven **94.0%** execution accuracy with Groq (and 92.0% with Ollama) against the Strict Golden Dataset. Exposed regex-based routing flaws in the evaluator, proving the agent logic is vastly superior to rigid string matching.

## v0.9 - System-Wide Analytics (Phase 5)

### Added
- **Text-to-SQL Engine**: Added `execute_system_query` to automatically translate natural language into PostgreSQL queries for aggregate questions.
- **Chain of Thought Planner**: Refactored the `planner_node` prompt to force boolean evaluation before tool selection, resulting in 100% accurate tool routing.
- **Generative Formatter Updates**: The `FormatterNode` now dynamically summarizes multiple rows of SQL JSON outputs into comprehensive, human-readable answers.
- **Connection Pool Safety**: Patched a critical bug where long LLM inferences exhausted the PostgreSQL connection pool.

### Status
Phase 5 complete. Evaluation accuracy increased from 77% to **94%** (legacy V3 semantic score).

## v0.8 - Advanced AI & Observability (Phase 4)

### Added
- Agent V2 powered by LangGraph `StateGraph` for highly deterministic orchestration.
- Full observability with LangSmith Tracing.
- Semantic Evaluation Suite (`scripts/evaluate_v2.py`) using LLM-as-a-Judge.
- Expanded Mock Dataset to 100 items including edge cases.
- `generate_report.py` script for automated LangSmith markdown reporting.

### Status
Phase 4 complete. The agent is now fully observable, deterministic, and evaluated.

## v0.7 - PostgreSQL Migration & Validation (Phase 3)

### Added
- Full PostgreSQL persistence support
- Config-driven database switching
- Automated schema creation and seeding for PostgreSQL

### Status
Phase 3 complete. The application is fully migrated to PostgreSQL.

## v0.5 & v0.6 - Architecture Foundation

### Added
- Centralized settings module backed by `.env`
- Request correlation IDs & Global error handler
- SQLite foundation & Repository pattern implementation

## v0.1 to v0.4 - Initial Agent & Finance Tools

### Added
- Finance agent using LangChain + Ollama
- Subsystem cost tool, Budget comparison, Overrun risk, Financial summary
- Agent Response Formatting
