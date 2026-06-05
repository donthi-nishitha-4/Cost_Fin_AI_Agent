# Changelog

## v0.7 - PostgreSQL Migration & Validation

### Added
- Full PostgreSQL persistence support
- Config-driven database switching
- Automated schema creation and seeding for PostgreSQL
- PostgreSQL connection diagnostic tools
- Regression testing against PostgreSQL (49 passed)

### Updated
- README and Architecture notes to reflect PostgreSQL as primary persistence
- Project progress and Roadmap status

### Status
Phase 3 complete. The application is now fully migrated to PostgreSQL.

## v0.6 - SQLite Persistence Foundation

### Added
- SQLite database config
- SQLAlchemy engine and session setup
- Explicit database initialization script
- Mock finance data seeding into SQLite
- Repository layer for finance reads
- DB-backed finance service helpers
- SQLite/PostgreSQL dependency helpers
- Settings and dependency tests
- PostgreSQL engine/session staging

### Status
Phase 3 persistence foundation is now in place.

## v0.5 - Config Foundation and Middleware Cleanup

### Added
- Centralized settings module backed by `.env`
- Environment-driven project name, log level, and LLM model
- Request correlation IDs
- Global error handler

### Updated
- README, architecture notes, API contracts, and debugging guide

### Status
Phase 2 cleanup complete, ready to begin Phase 3 configuration and persistence work.

## v0.4 - Agent Response Formatting

### Added
- Human-readable answer field in agent responses
- Response formatter module
- Formatter tests

### Status
Agent responses now include both readable summaries and raw structured data.

## v0.3 - Financial Summary Tool

### Added
- Financial summary service
- Financial summary tool
- Financial summary API
- Agent routing for financial summary
- Tests for service, tool, validator, and API layers

### Status
Full financial summary works end-to-end.

## v0.2 - Phase 2 Finance Tools

### Added
- Budget comparison service, tool, and API
- Overrun risk service, tool, and API
- Planner routing support
- Validator support
- Tests for new tools

### Status
Multi-tool finance capabilities are operational.

## v0.1 - Initial Working Agent

### Added
- Finance agent using LangChain + Ollama
- Subsystem cost tool
- API endpoints
- Basic test suite

### Status
Stable working baseline for production refactoring
