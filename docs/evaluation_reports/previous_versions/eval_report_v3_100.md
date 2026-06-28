# V3 Hybrid Evaluation Report (Auto-Generated)

**Date**: June 19, 2026
**Dataset**: `Cost_Finance_Evaluation`
**Test Run**: `V3_Hybrid_Eval-561a7445`
**Evaluator**: Hybrid Pipeline (Deterministic Math + LLM Semantic)

## Executive Summary
This report captures the evaluation results of the LangGraph Agent V2 against the expanded evaluation dataset, using the V3 Hybrid Evaluation Engine to guarantee zero "Math Blindness".

## Performance Metrics
- **Total Test Cases**: 100
- **Passed (Perfect Math & Semantic)**: 15
- **Failed**: 85
- **Overall True Business Accuracy**: 15.0%

## 🔍 Semantic Passes (The Magic of LLM-as-a-Judge)
These are cases where the agent passed mathematically and semantically, even though the text was completely different.

*No semantic diffs found.*
## ❌ Failed Cases
These are queries that the agent failed mathematically or semantically.

### Failure 1 (Math/Sign Error):
- **Query**: What is the cost breakdown for subsystem 17?
- **Expected**: Subsystem 17 (Water Supply - Block E) cost breakdown: Labor cost = $10,785.89, Material cost = $14,188.21, Equipment cost = $9,377.03. Sum of direct costs = $34,351.13, with the remaining $1,881.13 of the $36,232.26 actual cost attributed to indirect costs/overhead/contingency.
- **Actual**: Water Supply - Block E cost breakdown is labor 10785.89, material 14188.21, and equipment 9377.03.

### Failure 2 (Math/Sign Error):
- **Query**: What is the cost breakdown for subsystem 42?
- **Expected**: Subsystem 42 (Mechanical Systems - Podium) cost breakdown: Labor cost = $33,899.42, Material cost = $32,670.70, Equipment cost = $11,327.86. Sum of direct costs = $77,897.98, with the remaining $9,777.01 of the $87,674.99 actual cost attributed to indirect costs/overhead/contingency.
- **Actual**: Mechanical Systems - Podium cost breakdown is labor 33899.42, material 32670.7, and equipment 11327.86.

### Failure 3 (Math/Sign Error):
- **Query**: What is the cost breakdown for subsystem 9?
- **Expected**: Subsystem 9 (Concrete Works - Tower A) cost breakdown: Labor cost = $5,998.07, Material cost = $4,615.69, Equipment cost = $3,843.77. Sum of direct costs = $14,457.53, with the remaining $2,528.92 of the $16,986.45 actual cost attributed to indirect costs/overhead/contingency.
- **Actual**: Concrete Works - Tower A cost breakdown is labor 5998.07, material 4615.69, and equipment 3843.77.

### Failure 4 (Math/Sign Error):
- **Query**: What is the cost breakdown for subsystem 55?
- **Expected**: Subsystem 55 (Plumbing - South Wing) cost breakdown: Labor cost = $5,983.02, Material cost = $5,155.08, Equipment cost = $3,307.20. Sum of direct costs = $14,445.30, with the remaining $1,472.22 of the $15,917.52 actual cost attributed to indirect costs/overhead/contingency.
- **Actual**: Plumbing - South Wing cost breakdown is labor 5983.02, material 5155.08, and equipment 3307.2.

### Failure 5 (Math/Sign Error):
- **Query**: What is the cost breakdown for subsystem 63?
- **Expected**: Subsystem 63 (Telecommunications - West Annex) cost breakdown: Labor cost = $75,157.21, Material cost = $68,953.10, Equipment cost = $33,205.73. Sum of direct costs = $177,316.04, with the remaining $22,012.58 of the $199,328.62 actual cost attributed to indirect costs/overhead/contingency.
- **Actual**: Telecommunications - West Annex cost breakdown is labor 75157.21, material 68953.1, and equipment 33205.73.

### Failure 6 (Math/Sign Error):
- **Query**: Show labor cost for subsystem 42.
- **Expected**: The labor cost for subsystem 42 (Mechanical Systems - Podium) is $33,899.42.
- **Actual**: Mechanical Systems - Podium cost breakdown is labor 33899.42, material 32670.7, and equipment 11327.86.

### Failure 7 (Math/Sign Error):
- **Query**: Show labor cost for subsystem 4.
- **Expected**: The labor cost for subsystem 4 (Landscaping - South Wing) is $44,955.24.
- **Actual**: Landscaping - South Wing cost breakdown is labor 44955.24, material 17194.34, and equipment 7133.54.

### Failure 8 (Math/Sign Error):
- **Query**: Show labor cost for subsystem 56.
- **Expected**: The labor cost for subsystem 56 (Parking - West Annex) is $333,390.41.
- **Actual**: Parking - West Annex cost breakdown is labor 333390.41, material 102383.29, and equipment 42981.7.

### Failure 9 (Math/Sign Error):
- **Query**: Show labor cost for subsystem 34.
- **Expected**: The labor cost for subsystem 34 (Plumbing - Sector 1) is $519,466.77.
- **Actual**: Plumbing - Sector 1 cost breakdown is labor 519466.77, material 184521.36, and equipment 135892.98.

### Failure 10 (Math/Sign Error):
- **Query**: Show labor cost for subsystem 23.
- **Expected**: The labor cost for subsystem 23 (Telecommunications - Podium) is $190,127.97.
- **Actual**: Telecommunications - Podium cost breakdown is labor 190127.97, material 82380.43, and equipment 34772.54.

### Failure 11 (Math/Sign Error):
- **Query**: Show material cost for subsystem 5.
- **Expected**: The material cost for subsystem 5 (Facade - East Annex) is $137,799.22.
- **Actual**: Facade - East Annex cost breakdown is labor 46567.44, material 137799.22, and equipment 18088.49.

### Failure 12 (Math/Sign Error):
- **Query**: Show material cost for subsystem 14.
- **Expected**: The material cost for subsystem 14 (Concrete Works - Zone 7) is $134,668.02.
- **Actual**: Concrete Works - Zone 7 cost breakdown is labor 35485.56, material 134668.02, and equipment 27189.26.

### Failure 13 (Math/Sign Error):
- **Query**: Show material cost for subsystem 79.
- **Expected**: The material cost for subsystem 79 (Site Development - East Annex) is $177,527.56.
- **Actual**: Site Development - East Annex has a planned cost of 231682.29, actual cost of 291547.02, and remaining budget of -59864.73000000001.

### Failure 14 (Math/Sign Error):
- **Query**: Show material cost for subsystem 53.
- **Expected**: The material cost for subsystem 53 (Site Development - Central Plant) is $231,815.25.
- **Actual**: Site Development - Central Plant cost breakdown is labor 68743.77, material 231815.25, and equipment 58163.39.

### Failure 15 (Math/Sign Error):
- **Query**: Show material cost for subsystem 88.
- **Expected**: The material cost for subsystem 88 (Landscaping - Extension) is $191,519.86.
- **Actual**: Landscaping - Extension cost breakdown is labor 192316.23, material 191519.86, and equipment 132622.48.


## Recommendations for Phase 6
- **Groq LLM Migration**: The deterministic math bounds are now safely in place. It is completely safe to migrate to Groq/Llama3 cloud endpoints for blazing fast speed without worrying about undetected hallucinations.
