# Architecture Notes

## Overview

The Cost Finance Agent follows a layered architecture that separates API handling, agent orchestration, business logic, and persistence concerns.

This separation allows database implementations to change without requiring modifications to service logic, agent tooling, or API contracts.

---

## Current Validated Architecture

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

---

## Configuration Layer

```text
.env
  ↓
app/core/settings.py
  ↓
Application Configuration
```

Configuration currently manages:

* Application metadata
* Logging configuration
* LLM model settings
* Database configuration
* Environment-specific values

---

## Persistence Layer

### Current Components

```text
scripts/init_db.py
    └─ Database initialization

app/core/database.py
    └─ SQLite engine and session management

app/core/postgres_database.py
    └─ PostgreSQL engine preparation

app/core/seed_database.py
    └─ Seed database from finance dataset

app/repositories/finance_repository.py
    └─ Repository abstraction
```

### Design Goal

Business services should never communicate directly with database engines or SQLAlchemy sessions.

All persistence access should flow through the repository layer.

```text
Service Layer
      ↓
Repository Layer
      ↓
Database
```

This enables migration between SQLite and PostgreSQL with minimal service-layer changes.

---

## Phase 3 PostgreSQL Migration Strategy

### Already Completed

* PostgreSQL configuration scaffolding
* PostgreSQL database module
* Environment-driven database configuration
* Repository abstraction layer
* SQLite persistence validation

### Planned Migration Flow

1. Configure PostgreSQL runtime
2. Validate connection and session creation
3. Migrate one pilot endpoint
4. Verify API compatibility
5. Expand migration to remaining endpoints
6. Run full regression testing
7. Retire SQLite as primary runtime

---

## Stabilized Routes

* GET /
* GET /agent?query=...
* GET /api/v1/costs/{subsystem_id}
* GET /api/v1/breakdown/{subsystem_id}
* GET /api/v1/budget-comparison/{subsystem_id}
* GET /api/v1/overrun-risk/{subsystem_id}
* GET /api/v1/financial-summary/{subsystem_id}

---

## Current Safeguards

### Agent Safety

* Planner output is validated before execution.
* Tool execution occurs only through registered tool wrappers.
* Invalid plans are rejected before execution.

### Application Reliability

* Structured logging for finance operations.
* Centralized configuration management.
* Global exception handling.
* Request correlation IDs.

### Data Access Protection

* Service functions access persistence through repositories.
* Database initialization is explicit and repeatable.
* Seed data can be regenerated consistently.
* Database implementations remain isolated from business logic.

---

## Future Architecture Enhancements

* PostgreSQL production deployment
* Async database access
* LangGraph workflow orchestration
* Monitoring and observability layer
* Multi-agent collaboration patterns
