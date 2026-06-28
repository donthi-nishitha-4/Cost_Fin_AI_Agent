# pyrefly: ignore [missing-import]
from sqlalchemy import text # type : ignore
from app.core.llm_factory import get_llm
from app.core.settings import settings

from app.core.database import get_db
from app.repositories.finance_repository import get_finance_subsystem_by_id


def get_subsystem_cost(subsystem_id: int, db=None):
    return get_subsystem_cost_from_db(subsystem_id, db=db)


def get_subsystem_cost_from_db(subsystem_id: int, db=None):
    close_db = False

    if db is None:
        db = next(get_db())
        close_db = True

    try:
        row = get_finance_subsystem_by_id(db, subsystem_id)

        if not row:
            return None

        remaining_budget = row.planned_cost - row.actual_cost

        return {
            "subsystem": row.subsystem_name,
            "planned_cost": row.planned_cost,
            "actual_cost": row.actual_cost,
            "remaining_budget": remaining_budget
        }
    finally:
        if close_db:
            db.close()


def get_cost_breakdown_from_db(subsystem_id: int, db=None):
    close_db = False

    if db is None:
        db = next(get_db())
        close_db = True

    try:
        row = get_finance_subsystem_by_id(db, subsystem_id)

        if not row:
            return None

        return {
            "subsystem": row.subsystem_name,
            "labor_cost": row.labor_cost,
            "material_cost": row.material_cost,
            "equipment_cost": row.equipment_cost
        }
    finally:
        if close_db:
            db.close()


def get_budget_comparison_from_db(subsystem_id: int, db=None):
    close_db = False

    if db is None:
        db = next(get_db())
        close_db = True

    try:
        row = get_finance_subsystem_by_id(db, subsystem_id)

        if not row:
            return None

        variance = row.planned_cost - row.actual_cost

        if variance >= 0:
            budget_status = "under_budget"
        else:
            budget_status = "over_budget"

        return {
            "subsystem": row.subsystem_name,
            "planned_cost": row.planned_cost,
            "actual_cost": row.actual_cost,
            "variance": variance,
            "budget_status": budget_status
        }
    finally:
        if close_db:
            db.close()


def get_overrun_risk_from_db(subsystem_id: int, db=None):
    close_db = False

    if db is None:
        db = next(get_db())
        close_db = True

    try:
        row = get_finance_subsystem_by_id(db, subsystem_id)

        if not row:
            return None

        if row.planned_cost == 0:
            utilization_percent = float('inf') if row.actual_cost > 0 else 0.0
        else:
            utilization_percent = round((row.actual_cost / row.planned_cost) * 100, 2)

        if utilization_percent >= 90:
            risk_level = "high"
        elif utilization_percent >= 75:
            risk_level = "medium"
        else:
            risk_level = "low"

        return {
            "subsystem": row.subsystem_name,
            "planned_cost": row.planned_cost,
            "actual_cost": row.actual_cost,
            "utilization_percent": utilization_percent,
            "risk_level": risk_level
        }
    finally:
        if close_db:
            db.close()


def get_cost_breakdown(subsystem_id: int, db=None):
    return get_cost_breakdown_from_db(subsystem_id, db=db)


def get_budget_comparison(subsystem_id: int, db=None):
    return get_budget_comparison_from_db(subsystem_id, db=db)


def get_overrun_risk(subsystem_id: int, db=None):
    return get_overrun_risk_from_db(subsystem_id, db=db)


def get_financial_summary(subsystem_id: int, db=None):
    close_db = False

    if db is None:
        db = next(get_db())
        close_db = True

    try:
        cost = get_subsystem_cost(subsystem_id, db=db)
        breakdown = get_cost_breakdown(subsystem_id, db=db)
        budget_comparison = get_budget_comparison(subsystem_id, db=db)
        overrun_risk = get_overrun_risk(subsystem_id, db=db)

        if not cost:
            return None

        return {
            "subsystem": cost["subsystem"],
            "cost": cost,
            "breakdown": breakdown,
            "budget_comparison": budget_comparison,
            "overrun_risk": overrun_risk
        }
    finally:
        if close_db:
            db.close()


def execute_system_query(query: str, db=None):
    # 1. Ask the LLM to generate the SQL FIRST, before touching the database!
    prompt = f"""
You are a PostgreSQL expert. Given the following natural language query, write the exact PostgreSQL SQL query to answer it.
The database has a table named 'finance_subsystems' with the following schema:
- id (Integer, primary_key)
- subsystem_name (String, e.g. 'Fire Protection - Tower A')
- planned_cost (Float)
- actual_cost (Float)
- labor_cost (Float)
- material_cost (Float)
- equipment_cost (Float)

CRITICAL SQL INSTRUCTION: Generate a standard SQL query that SELECTs the relevant raw columns or rows from 'finance_subsystems' (or uses aggregates like SUM, AVG, COUNT). You may perform basic mathematical calculations (like additions/subtractions, e.g., planned_cost - actual_cost) and sorting (ORDER BY ... LIMIT) directly in the SQL.
1. Do NOT perform complex string formatting, CASE statements, or text concatenations inside the SQL.
2. If the query compares or queries MULTIPLE subsystem IDs, you MUST use a simple 'WHERE id IN (id_A, id_B, ...)' clause. Do NOT use JOINs, UNIONs, table aliases, or multiple SELECT blocks.
3. Always place all filter conditions in the WHERE clause BEFORE any ORDER BY or LIMIT clauses. Never place filter conditions after LIMIT.
4. For queries listing or describing specific subsystems, you MUST always include the 'id' column in your SELECT statement so the subsystem ID is available in the results. (This does NOT apply to aggregate queries that calculate counts, sums, or averages, such as 'COUNT(*)' or 'AVG(...)').
5. If the query asks for planned cost, actual cost, variance, overrun, or budget details of specific subsystems, you MUST include both 'planned_cost' and 'actual_cost' in your SELECT statement.

Return ONLY the raw SQL query string. Do not include markdown tags (like ```sql) or any explanations.

Hints:
- "severe overruns" means actual_cost > 1.3 * planned_cost
- "underspend" means planned_cost - actual_cost
- "over budget" means actual_cost > planned_cost
- "under budget" means actual_cost <= planned_cost
- "variance" means planned_cost - actual_cost (deficit/overrun is negative, surplus/underspend is positive)
- "bottom 5 variances" means the 5 lowest values of variance (which will be the most negative/worst overruns). You MUST use 'ORDER BY (planned_cost - actual_cost) ASC LIMIT 5' in your SQL query.
- "top 5 overruns" means the 5 highest values of overrun. You MUST use 'ORDER BY (actual_cost - planned_cost) DESC LIMIT 5' in your SQL query.
- "overrun" means actual_cost - planned_cost
- "X-heavy" (e.g., labor-heavy, material-heavy, equipment-heavy) means you MUST select and sort by the ratio of that component over direct costs (e.g., 'SELECT id, subsystem_name, X_cost / (labor_cost + material_cost + equipment_cost) AS ratio FROM finance_subsystems ORDER BY ratio DESC LIMIT 1').

Query: {query}
"""

    response = get_llm().invoke(prompt)
    if hasattr(response, "content"):
        sql_query = response.content.strip()
    else:
        sql_query = str(response).strip()
    
    # Strip markdown codeblocks just in case Ollama/Groq includes them
    if sql_query.startswith("```sql"):
        sql_query = sql_query[6:]
    if sql_query.startswith("```"):
        sql_query = sql_query[3:]
    if sql_query.endswith("```"):
        sql_query = sql_query[:-3]
    sql_query = sql_query.strip()

    # 2. NOW open the database connection just to run the query!
    close_db = False
    if db is None:
        from app.core.database import get_db
        db = next(get_db())
        close_db = True

    try:
        # Execute the raw query safely
        result = db.execute(text(sql_query)).fetchall()
        
        # Convert SQLAlchemy rows into standard dictionaries
        if result:
            keys = result[0]._mapping.keys()
            rows = [dict(zip(keys, row)) for row in result]
        else:
            rows = []

        return {
            "query": query,
            "sql": sql_query,
            "result": rows
        }
    except Exception as e:
        return {
            "query": query,
            "sql": sql_query,
            "error": str(e)
        }
    finally:
        if close_db:
            db.close()
