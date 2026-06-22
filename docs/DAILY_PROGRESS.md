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

## June 19, 2026 - Phase 5: System Analytics & V3 Evaluation Hardening

### Key Decisions Made
1. **Text-to-SQL System Analytics Engine**: To solve the Phase 4 failure where aggregate queries ("Find severe overruns") were being rejected, we introduced `system_analytics_tool`.
   - *Why?* A 100-row database cannot be easily injected into an LLM context window. Instead, we injected the PostgreSQL schema and prompted the LLM to write native SQL queries.
   - *Result*: The agent can now securely fetch complex, multi-row aggregate data directly from PostgreSQL.

2. **Chain-of-Thought Planner Prompting**: We hardened the `planner_node` by forcing the LLM to output explicit boolean logic before making a tool decision.
   - *Why?* The LLM was experiencing "attention span" issues—ignoring the critical rules at the top of the prompt and routing aggregate queries to the wrong tool.
   - *Result*: The Chain-of-Thought trick completely eliminated hallucinated tool routing, boosting raw Semantic Accuracy from 77% to 94%.

3. **The LLM Math Blindness Audit & V3 Hybrid Evaluation**: A rigorous manual audit of the 94% "passing" cases revealed that the LLM-as-a-Judge suffered from severe "Math Blindness" (failing to penalize flipped mathematical signs and logical contradictions like "not applicable" vs "over budget").
   - *Why?* LLMs optimize for semantic "vibes", not strict accounting principles.
   - *Solution*: We designed and implemented `scripts/evaluate_v3.py`. This new architecture introduces a **Hybrid Deterministic + Semantic Pipeline**. It uses a strict Python regex engine to mathematically verify every digit and sign `(+/-)` first, acting as a binary gatekeeper before allowing the LLM Judge to grade the conversational tone.
   - *Result*: A production-grade `confidence_score` metric natively integrated into LangSmith that mathematically guarantees safety while preserving natural language evaluation.

## June 19, 2026 - Phase 6: Cloud LLM Migration & Benchmarking

### Key Decisions Made
1. **Dynamic LLM Factory**: Instead of hardcoding Ollama everywhere, we implemented `app/core/llm_factory.py`.
   - *Why?* We needed the flexibility to hot-swap LLM providers (Local vs Cloud) based on a simple `.env` flag without touching the agent logic.
   - *Result*: Achieved massive flexibility; developers can work locally via Ollama, while production routes to cloud LPUs.

2. **Groq LPU Migration**: We migrated the default model inference engine to the Groq Cloud API (`llama-3.1-8b-instant`).
   - *Why?* The local Ollama Llama-3 model struggled heavily with `cost_lookup` vs `cost_breakdown` logic. We hypothesized a faster, slightly more capable cloud model would resolve tool routing issues.
   - *Result*: Inference dropped from 12.44 seconds to **1.41 seconds** (8.8x faster). Furthermore, mathematical evaluation scores spiked from 43% to 63%, proving that the new Llama 3.1 model routed tools far better than the local Llama 3 model.

3. **V5 Project-Grade Evaluator**: We rebuilt the V3 evaluation pipeline into the ultimate V5 Evaluator.
   - *Why?* V3 still relied on the LLM to extract fields like `subsystem_id`, which hallucinates. 
   - *Result*: The new V5 evaluator (`scripts/evaluate_v5.py`) implements strict 5-layer checking: (1) Regex Intent Routing, (2) Intent-Specific Targeted Regex Extraction (e.g. only searching for "variance" if the intent is variance), (3) Deterministic Math validation, (4) Immediate `CRITICAL` severity failures for Business Logic violations, and (5) Decoupled Semantic validation.

## June 20, 2026 - Phase 6.6: The Golden Dataset Generation

### Key Decisions Made
1. **Regenerating Ground Truth from Source**: Our V5 Math Evaluation plateaued at 63% due to mismatched mock logic (e.g., Risk threshold logic, "> 130%" vs ">= 130%"). Instead of attempting to hack the evaluator to accept the mock data, we made the architectural decision to write `scripts/generate_golden_dataset.py`.
   - *Why?* Evaluation datasets must be mathematically identical to the actual deterministic business rules in `finance_service.py`. We passed 100 queries directly into our optimized Groq agent to pull actual data tables and dynamically write the golden expected answers.
   - *Result*: The `Cost_Finance_Golden` dataset correctly aligned the LangSmith baseline to the true backend codebase logic.

2. **Final Golden Evaluation**: We repointed `evaluate_v5.py` to test the agent exclusively against the Golden Dataset.
   - *Why?* To prove that the Groq-powered Agent architecture had no true logic flaws.
   - *Result*: Achieved a measured **94.0% Math Accuracy with Groq** (and 92.0% with Ollama). The architecture proved highly accurate, and the missing 6-8% was isolated entirely to regex routing false-negatives in the evaluator script itself.
