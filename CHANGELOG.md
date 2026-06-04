# Changelog

## v0.7 - Phase 3 Preparation and Documentation Cleanup

### Added

* PostgreSQL migration planning documentation
* Project roadmap and next-stage guidance
* Phase 3 architecture notes

### Updated

* README documentation
* PROJECT_PROGRESS.md
* ARCHITECTURE_NOTES.md
* DEBUGGING_GUIDE.md
* CHANGELOG.md

### Status

Project documentation aligned with Phase 3 PostgreSQL migration objectives.

---

## v0.6 - SQLite Persistence Foundation

### Added

* SQLite database configuration
* SQLAlchemy engine and session setup
* Explicit database initialization script
* Mock finance data seeding into SQLite
* Repository layer for finance reads
* Database-backed finance service helpers
* PostgreSQL preparation scaffolding

### Status

Persistence foundation completed. Repository abstraction enables future PostgreSQL migration.

---

## v0.5 - Config Foundation and Middleware Cleanup

### Added

* Centralized settings module backed by `.env`
* Environment-driven project name, log level, and LLM model
* Request correlation IDs
* Global error handling

### Updated

* README documentation
* Architecture notes
* API contracts
* Debugging guide

### Status

Configuration and middleware foundations stabilized.

---

## v0.4 - Agent Response Formatting

### Added

* Human-readable answer field in agent responses
* Response formatter module
* Response formatter test coverage

### Status

Agent responses now provide both readable summaries and structured data.

---

## v0.3 - Financial Summary Tool

### Added

* Financial summary service
* Financial summary tool
* Financial summary API
* Agent routing for financial summary
* Service, tool, validator, and API tests

### Status

Financial summary workflow operational end-to-end.

---

## v0.2 - Phase 2 Finance Tools

### Added

* Budget comparison service, tool, and API
* Overrun risk service, tool, and API
* Planner routing support
* Validator support
* Test coverage for new finance tools

### Status

Multi-tool finance capabilities operational.

---

## v0.1 - Initial Working Agent

### Added

* Finance agent using LangChain and Ollama
* Subsystem cost tool
* Finance API endpoints
* Initial test suite

### Status

Stable baseline established for future expansion.
