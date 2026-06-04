# Cost Finance AI Agent

Enterprise-style AI Agent for cost estimation, budget tracking, and financial analytics within construction and project-management systems.

---

## Project Status

**Current Phase:** Phase 3 - Persistence & PostgreSQL Migration Preparation

### Completed

* AI Agent orchestration
* Finance service layer
* Tool abstraction layer
* SQLite persistence foundation
* Repository abstraction
* Configuration management
* API coverage and testing

### In Progress

* PostgreSQL migration planning
* Persistence layer refinement

### Upcoming

* PostgreSQL rollout
* Async architecture
* Monitoring and metrics
* LangGraph workflows

---

## Architecture Overview

```text
User Query
    |
API Layer
    |
Orchestrator
    |
Planner
    |
Validator
    |
Tool Registry
    |
Tool Executor
    |
Finance Tools
    |
Response Formatter
    |
Service Layer
    |
Repository Layer
    |
Database
```

The architecture isolates business logic from persistence concerns, enabling future migration between database implementations with minimal service-layer changes.

---

## Features

### Platform Features

* FastAPI backend
* Versioned API routes
* Health monitoring endpoint
* Structured logging
* Request correlation IDs
* Global error handling
* Environment-based configuration
* Automated testing

### AI Agent Features

* LangChain integration
* Ollama support
* Llama3 integration
* Tool routing and execution
* Planner validation
* Multi-intent handling
* Human-readable response generation

### Persistence Features

* SQLite database support
* SQLAlchemy engine and session management
* Database initialization scripts
* Repository abstraction layer
* Environment-driven database configuration

---

## Finance Capabilities

* Subsystem cost summary
* Cost breakdown analysis
* Budget comparison
* Overrun risk analysis
* Financial summary generation

---

## API Endpoints

| Endpoint                                     | Description                |
| -------------------------------------------- | -------------------------- |
| GET /                                        | Health and root endpoint   |
| GET /agent?query=...                         | Finance AI Agent           |
| GET /api/v1/costs/{subsystem_id}             | Cost summary               |
| GET /api/v1/breakdown/{subsystem_id}         | Cost breakdown             |
| GET /api/v1/budget-comparison/{subsystem_id} | Budget comparison          |
| GET /api/v1/overrun-risk/{subsystem_id}      | Overrun risk analysis      |
| GET /api/v1/financial-summary/{subsystem_id} | Combined financial summary |

---

## Local Development

### Start the Application

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

### Run Tests

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Current status:

```text
44 passed
```

---

## Example Agent Query

```powershell
curl "http://127.0.0.1:8000/agent?query=give%20me%20full%20financial%20summary%20of%20subsystem%201"
```

The response includes:

* Human-readable summary
* Structured finance data
* Tool execution metadata

---

## Configuration

Environment values are loaded from `.env`.

### Core Settings

```text
PROJECT_NAME
ENVIRONMENT
LOG_LEVEL
LLM_MODEL
```

### Database Settings

```text
DATABASE_URL
DB_ECHO
POSTGRES_URL
```

---

## Persistence Layer

SQLite currently serves as the validated persistence implementation.

Initialize the database:

```powershell
.\.venv\Scripts\python.exe -m scripts.init_db
```

This creates the schema and seeds the database using the finance mock dataset.

Repository abstractions have been introduced to support the upcoming PostgreSQL migration.

---

## Roadmap

### Phase 3

* PostgreSQL migration
* Persistent finance storage

### Phase 4

* Async architecture
* LangGraph workflows
* Monitoring and metrics

### Future

* Production deployment readiness
* Multi-agent finance workflows
