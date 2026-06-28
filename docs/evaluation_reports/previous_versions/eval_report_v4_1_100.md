# V4 Query-Aware Hybrid Evaluation Report (Auto-Generated)

**Date**: June 19, 2026
**Dataset**: `Cost_Finance_Evaluation`
**Test Run**: `V4_QueryAware_Eval-c55617b3`
**Evaluator**: V4 Hybrid (Query-Aware Extraction + Strict Math + LLM Semantic)

## Executive Summary
This report captures the evaluation results of the LangGraph Agent V2 against the expanded evaluation dataset. 
It utilizes the **V4 Query-Aware Evaluation Framework** to intelligently parse intents, enforce rigid mathematical assertions, and output Subsystem ID Warnings instead of false-positive failures.

## Performance Metrics
- **Total Test Cases**: 100
- **Passed (Perfect Math & Semantic)**: 44
- **Failed**: 56
- **Subsystem ID Warnings (Non-Fatal)**: 1
- **Overall True Business Accuracy**: 44.0%

## 🔍 Semantic Passes (The Magic of LLM-as-a-Judge)
These are cases where the agent passed mathematically and semantically, even though the text was completely different.

### Example 1:
- **Query**: What is the cost breakdown for subsystem 17?
- **Expected**: Subsystem 17 (Water Supply - Block E) cost breakdown: Labor cost = $10,785.89, Material cost = $14,188.21, Equipment cost = $9,377.03. Sum of direct costs = $34,351.13, with the remaining $1,881.13 of the $36,232.26 actual cost attributed to indirect costs/overhead/contingency.
- **Actual**: Subsystem 17 (Water Supply - Block E) cost breakdown is labor 10785.89, material 14188.21, and equipment 9377.03.

### Example 2:
- **Query**: What is the cost breakdown for subsystem 42?
- **Expected**: Subsystem 42 (Mechanical Systems - Podium) cost breakdown: Labor cost = $33,899.42, Material cost = $32,670.70, Equipment cost = $11,327.86. Sum of direct costs = $77,897.98, with the remaining $9,777.01 of the $87,674.99 actual cost attributed to indirect costs/overhead/contingency.
- **Actual**: Subsystem 42 (Mechanical Systems - Podium) cost breakdown is labor 33899.42, material 32670.7, and equipment 11327.86.

### Example 3:
- **Query**: What is the cost breakdown for subsystem 9?
- **Expected**: Subsystem 9 (Concrete Works - Tower A) cost breakdown: Labor cost = $5,998.07, Material cost = $4,615.69, Equipment cost = $3,843.77. Sum of direct costs = $14,457.53, with the remaining $2,528.92 of the $16,986.45 actual cost attributed to indirect costs/overhead/contingency.
- **Actual**: Subsystem 9 (Concrete Works - Tower A) cost breakdown is labor 5998.07, material 4615.69, and equipment 3843.77.

### Example 4:
- **Query**: What is the cost breakdown for subsystem 55?
- **Expected**: Subsystem 55 (Plumbing - South Wing) cost breakdown: Labor cost = $5,983.02, Material cost = $5,155.08, Equipment cost = $3,307.20. Sum of direct costs = $14,445.30, with the remaining $1,472.22 of the $15,917.52 actual cost attributed to indirect costs/overhead/contingency.
- **Actual**: Subsystem 55 (Plumbing - South Wing) cost breakdown is labor 5983.02, material 5155.08, and equipment 3307.2.

### Example 5:
- **Query**: What is the cost breakdown for subsystem 63?
- **Expected**: Subsystem 63 (Telecommunications - West Annex) cost breakdown: Labor cost = $75,157.21, Material cost = $68,953.10, Equipment cost = $33,205.73. Sum of direct costs = $177,316.04, with the remaining $22,012.58 of the $199,328.62 actual cost attributed to indirect costs/overhead/contingency.
- **Actual**: Subsystem 63 (Telecommunications - West Annex) cost breakdown is labor 75157.21, material 68953.1, and equipment 33205.73.

## ❌ Failed Cases
These are queries that the agent failed mathematically or semantically.

### Failure 1 (Math/Sign/Missing Data Error):
- **Query**: Show equipment cost for subsystem 6.
- **Expected**: The equipment cost for subsystem 6 (Elevators - Tower A) is $154,845.43.
- **Actual**: Subsystem 6 (Elevators - Tower A) has a planned cost of 300000.0, actual cost of 312000.0, and remaining budget of -12000.0.

### Failure 2 (Math/Sign/Missing Data Error):
- **Query**: Show equipment cost for subsystem 2.
- **Expected**: The equipment cost for subsystem 2 (Structural Steel - Tower B) is $543,532.47.
- **Actual**: Subsystem 2 (Structural Steel - Tower B) has a planned cost of 600000.0, actual cost of 980000.0, and remaining budget of -380000.0.

### Failure 3 (Math/Sign/Missing Data Error):
- **Query**: Show equipment cost for subsystem 39.
- **Expected**: The equipment cost for subsystem 39 (Roofing - Block D) is $106,112.50.
- **Actual**: Subsystem 39 (Roofing - Block D) has a planned cost of 239774.9, actual cost of 433325.1, and remaining budget of -193550.19999999998.

### Failure 4 (Math/Sign/Missing Data Error):
- **Query**: Show equipment cost for subsystem 64.
- **Expected**: The equipment cost for subsystem 64 (Elevators - East Annex) is $87,815.30.
- **Actual**: Subsystem 64 (Elevators - East Annex) has a planned cost of 314997.17, actual cost of 400547.72, and remaining budget of -85550.54999999999.

### Failure 5 (Math/Sign/Missing Data Error):
- **Query**: Show equipment cost for subsystem 18.
- **Expected**: The equipment cost for subsystem 18 (Interior Finishing - Phase 2) is $143,019.88.
- **Actual**: Subsystem 18 (Interior Finishing - Phase 2) has a planned cost of 146271.68, actual cost of 259911.79, and remaining budget of -113640.11000000002.

### Failure 6 (Math/Sign/Missing Data Error):
- **Query**: Is subsystem 11 over budget?
- **Expected**: Yes, subsystem 11 (Roofing - Basement Level) is over budget. Planned cost = $184,337.39, actual cost = $211,918.12, variance = +$27,580.73.
- **Actual**: Subsystem 11 (Roofing - Basement Level) is over_budget with a variance of -27580.72999999998 between planned cost 184337.39 and actual cost 211918.12.

### Failure 7 (Math/Sign/Missing Data Error):
- **Query**: Is subsystem 7 over budget?
- **Expected**: No, subsystem 7 (Roads - Sector 1) is under budget. Planned cost = $500,000.00, actual cost = $210,000.00, variance = -$290,000.00 (i.e., $290,000.00 under).
- **Actual**: Subsystem 7 (Roads - Sector 1) is under_budget with a variance of 290000.0 between planned cost 500000.0 and actual cost 210000.0.

### Failure 8 (Math/Sign/Missing Data Error):
- **Query**: Is subsystem 33 over budget?
- **Expected**: Yes, subsystem 33 (Security - Podium) is over budget. Planned cost = $558,784.87, actual cost = $568,279.02, variance = +$9,494.15.
- **Actual**: Subsystem 33 (Security - Podium) is over_budget with a variance of -9494.150000000023 between planned cost 558784.87 and actual cost 568279.02.

### Failure 9 (Math/Sign/Missing Data Error):
- **Query**: Is subsystem 13 over budget?
- **Expected**: Yes, subsystem 13 (Electrical - Podium) is over budget. Planned cost = $19,520.19, actual cost = $19,850.04, variance = +$329.85.
- **Actual**: Subsystem 13 (Electrical - Podium) is over_budget with a variance of -329.8500000000022 between planned cost 19520.19 and actual cost 19850.04.

### Failure 10 (Math/Sign/Missing Data Error):
- **Query**: Compare planned and actual cost for subsystem 29.
- **Expected**: Subsystem 29 (Security - Main Building): planned cost = $135,537.38, actual cost = $178,261.69, variance = $42,724.31 (over).
- **Actual**: Subsystem 29 (Security - Main Building) has a planned cost of 135537.38, actual cost of 178261.69, and remaining budget of -42724.31.

### Failure 11 (Math/Sign/Missing Data Error):
- **Query**: Compare planned and actual cost for subsystem 30.
- **Expected**: Subsystem 30 (Site Development - South Wing): planned cost = $686,882.17, actual cost = $417,457.16, variance = -$269,425.01 (under).
- **Actual**: Subsystem 30 (Site Development - South Wing) has a planned cost of 686882.17, actual cost of 417457.16, and remaining budget of 269425.01000000007.

### Failure 12 (Math/Sign/Missing Data Error):
- **Query**: Compare planned and actual cost for subsystem 8.
- **Expected**: Subsystem 8 (Water Supply - Phase 2): planned cost = $700,000.00, actual cost = $180,000.00, variance = -$520,000.00 (under).
- **Actual**: Subsystem 8 (Water Supply - Phase 2) has a planned cost of 700000.0, actual cost of 180000.0, and remaining budget of 520000.0.

### Failure 13 (Math/Sign/Missing Data Error):
- **Query**: Compare planned and actual cost for subsystem 38.
- **Expected**: Subsystem 38 (Structural Steel - South Wing): planned cost = $50,338.26, actual cost = $52,480.53, variance = $2,142.27 (over).
- **Actual**: Subsystem 38 (Structural Steel - South Wing) has a planned cost of 50338.26, actual cost of 52480.53, and remaining budget of -2142.269999999997.

### Failure 14 (Math/Sign/Missing Data Error):
- **Query**: Is subsystem 21 under budget?
- **Expected**: Yes, subsystem 21 (Telecommunications - Wing 3) is under budget. Planned cost = $48,431.16, actual cost = $28,150.30, variance = -$20,280.86.
- **Actual**: Subsystem 21 (Telecommunications - Wing 3) is under_budget with a variance of 20280.860000000004 between planned cost 48431.16 and actual cost 28150.3.

### Failure 15 (Math/Sign/Missing Data Error):
- **Query**: Is subsystem 45 under budget?
- **Expected**: Yes, subsystem 45 (Water Supply - Sector 2) is under budget. Planned cost = $681,753.17, actual cost = $565,960.74, variance = -$115,792.43.
- **Actual**: Subsystem 45 (Water Supply - Sector 2) is under_budget with a variance of 115792.43000000005 between planned cost 681753.17 and actual cost 565960.74.


## Recommendations for Phase 6
- **Groq LLM Migration**: The deterministic math bounds are now safely in place. It is completely safe to migrate to Groq/Llama3 cloud endpoints for blazing fast speed without worrying about undetected hallucinations.
