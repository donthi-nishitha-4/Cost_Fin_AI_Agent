# V2 Semantic Evaluation Report (Auto-Generated)

**Date**: June 19, 2026
**Dataset**: `Cost_Finance_Evaluation`
**Test Run**: `V2_Semantic_Eval-4238782b`
**Evaluator**: LLM-as-a-Judge (Semantic Match)

## Executive Summary
This report captures the evaluation results of the LangGraph Agent V2 against the expanded evaluation dataset.

## Performance Metrics
- **Total Test Cases**: 100
- **Passed (Semantic Match)**: 94
- **Failed**: 6
- **Overall Accuracy**: 94.0%

## 🔍 Semantic Passes (The Magic of LLM-as-a-Judge)
These are cases where the agent passed (Score = 1) even though the text was completely different. It successfully matched the *intent* and *data*, proving semantic evaluation works!

### Example 1:
- **Query**: What is the cost breakdown for subsystem 17?
- **Expected**: Subsystem 17 (Water Supply - Block E) cost breakdown: Labor cost = $10,785.89, Material cost = $14,188.21, Equipment cost = $9,377.03. Sum of direct costs = $34,351.13, with the remaining $1,881.13 of the $36,232.26 actual cost attributed to indirect costs/overhead/contingency.
- **Actual**: Water Supply - Block E cost breakdown is labor 10785.89, material 14188.21, and equipment 9377.03.

### Example 2:
- **Query**: What is the cost breakdown for subsystem 42?
- **Expected**: Subsystem 42 (Mechanical Systems - Podium) cost breakdown: Labor cost = $33,899.42, Material cost = $32,670.70, Equipment cost = $11,327.86. Sum of direct costs = $77,897.98, with the remaining $9,777.01 of the $87,674.99 actual cost attributed to indirect costs/overhead/contingency.
- **Actual**: Mechanical Systems - Podium cost breakdown is labor 33899.42, material 32670.7, and equipment 11327.86.

### Example 3:
- **Query**: What is the cost breakdown for subsystem 9?
- **Expected**: Subsystem 9 (Concrete Works - Tower A) cost breakdown: Labor cost = $5,998.07, Material cost = $4,615.69, Equipment cost = $3,843.77. Sum of direct costs = $14,457.53, with the remaining $2,528.92 of the $16,986.45 actual cost attributed to indirect costs/overhead/contingency.
- **Actual**: Concrete Works - Tower A cost breakdown is labor 5998.07, material 4615.69, and equipment 3843.77.

### Example 4:
- **Query**: What is the cost breakdown for subsystem 55?
- **Expected**: Subsystem 55 (Plumbing - South Wing) cost breakdown: Labor cost = $5,983.02, Material cost = $5,155.08, Equipment cost = $3,307.20. Sum of direct costs = $14,445.30, with the remaining $1,472.22 of the $15,917.52 actual cost attributed to indirect costs/overhead/contingency.
- **Actual**: Plumbing - South Wing cost breakdown is labor 5983.02, material 5155.08, and equipment 3307.2.

### Example 5:
- **Query**: What is the cost breakdown for subsystem 63?
- **Expected**: Subsystem 63 (Telecommunications - West Annex) cost breakdown: Labor cost = $75,157.21, Material cost = $68,953.10, Equipment cost = $33,205.73. Sum of direct costs = $177,316.04, with the remaining $22,012.58 of the $199,328.62 actual cost attributed to indirect costs/overhead/contingency.
- **Actual**: Telecommunications - West Annex cost breakdown is labor 75157.21, material 68953.1, and equipment 33205.73.

## ❌ Failed Cases
These are queries that the agent failed to answer correctly (or hallucinated).

### Failure 1:
- **Query**: Show equipment cost for subsystem 6.
- **Expected**: The equipment cost for subsystem 6 (Elevators - Tower A) is $154,845.43.
- **Actual**: Elevators - Tower A has a planned cost of 300000.0, actual cost of 312000.0, and remaining budget of -12000.0.

### Failure 2:
- **Query**: Show equipment cost for subsystem 64.
- **Expected**: The equipment cost for subsystem 64 (Elevators - East Annex) is $87,815.30.
- **Actual**: Elevators - East Annex has a planned cost of 314997.17, actual cost of 400547.72, and remaining budget of -85550.54999999999.

### Failure 3:
- **Query**: Find severe overruns.
- **Expected**: There are 10 subsystems with severe overruns (actual cost exceeding 130% of planned cost): Subsystem 39 (Roofing - Block D, 180.72% of planned), Subsystem 97 (Plumbing - Tower B, 179.78% of planned), Subsystem 18 (Interior Finishing - Phase 2, 177.69% of planned), Subsystem 74 (Fire Protection - Main Building, 172.28% of planned), Subsystem 69 (Interior Finishing - Tower B, 171.12% of planned), Subsystem 2 (Structural Steel - Tower B, 163.33% of planned), Subsystem 91 (Landscaping - Main Building, 160.80% of planned), Subsystem 84 (Fire Protection - Sector 1, 155.56% of planned), Subsystem 76 (Mechanical Systems - Tower B, 142.40% of planned), Subsystem 29 (Security - Main Building, 131.52% of planned).
- **Actual**: Severe overruns were identified for several subsystems, including Structural Steel - Tower B ($380,000), Fire Protection - Sector 1 ($369,429), and Mechanical Systems - Tower B ($172,058).

### Failure 4:
- **Query**: Which subsystem has the largest underspend compared to its planned budget?
- **Expected**: Subsystem 8 (Water Supply - Phase 2) has the largest underspend: $520,000.00 under budget (planned $700,000.00, actual $180,000.00).
- **Actual**: Fire Protection - Tower A is under_budget with a variance of 0.0 between planned cost 150000.0 and actual cost 150000.0.

### Failure 5:
- **Query**: Which subsystem has the lowest non-zero planned budget, and what is its actual cost?
- **Expected**: Subsystem 90 (Elevators - Wing 3) has the lowest non-zero planned budget at $10,102.61, with an actual cost of $12,469.17 (variance of $2,366.56).
- **Actual**: Fire Protection - Tower A has a planned cost of 150000.0, actual cost of 150000.0, and remaining budget of 0.0.

### Failure 6:
- **Query**: Which subsystem is labor-heavy, with labor cost as the dominant cost component?
- **Expected**: Subsystem 4 (Landscaping - South Wing) is labor-heavy: labor cost = $44,955.24, which is the largest of the three direct cost components (material = $17,194.34, equipment = $7,133.54).
- **Actual**: Fire Protection - Tower A cost breakdown is labor 45303.24, material 57287.05, and equipment 31635.68.


## Recommendations for V3
- **Aggregate Analytics Tool**: Aggregate queries (like "Find severe overruns") failed because the planner defaults to `subsystem_id: 1` when no ID is present. We need a system-wide analytical tool (Text-to-SQL or similar).
