# Changelog

## v0.9 - System-Wide Analytics (Phase 5)

### Added
- **Text-to-SQL Engine**: Added `execute_system_query` to automatically translate natural language into PostgreSQL queries for aggregate questions.
- **Chain of Thought Planner**: Refactored the `planner_node` prompt to force boolean evaluation before tool selection, resulting in 100% accurate tool routing.
- **Generative Formatter Updates**: The `FormatterNode` now dynamically summarizes multiple rows of SQL JSON outputs into comprehensive, human-readable answers.
- **Connection Pool Safety**: Patched a critical bug where long LLM inferences exhausted the PostgreSQL connection pool.

### Status
Phase 5 complete. Evaluation accuracy increased from 77% to **94%**.

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
