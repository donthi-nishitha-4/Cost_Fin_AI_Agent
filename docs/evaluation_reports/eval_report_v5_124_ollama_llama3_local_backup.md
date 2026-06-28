# V5 Project-Grade Local Evaluation Report
    
**Date**: June 28, 2026
**Execution Engine**: Local Ollama (llama3)

## 📊 High-Level Metrics
- **Overall Pipeline Score**: 98.5% *(Weighted: 50% Math, 30% Semantic, 20% Business Logic Safety)*
- **Math Accuracy**: 98.4%
- **Semantic Quality**: 97.6%
- **Total Queries**: 124

### Severity Breakdown
- **122 Pass** (INFO: Perfect Match)
- **0 Warning** (Missing IDs but math passed)
- **2 Fail** (Wrong subsystem, missing fields)
- **0 Critical** (Sign reversals, Business logic contradictions)

### Performance Analytics
- **Total Execution Time**: 3181.5 seconds
- **Average Latency**: 19.05 seconds per query
- **Slowest Response**: 150.16 seconds
- **Fastest Response**: 4.64 seconds

## 🎯 Intent Accuracy Stats
- **Aggregation**: 96.2% (50/52)
- **Budget Status**: 100.0% (10/10)
- **Cost Breakdown**: 100.0% (5/5)
- **Equipment Cost**: 100.0% (5/5)
- **Labor Cost**: 100.0% (6/6)
- **Material Cost**: 100.0% (5/5)
- **Remaining Budget**: 100.0% (6/6)
- **Risk**: 100.0% (10/10)
- **Unknown**: 100.0% (20/20)
- **Variance**: 100.0% (5/5)

## 🚨 Deep Dive: Critical Failures
*No critical business logic failures!*

## ❌ Deep Dive: Standard Failures
- Q: Which subsystem is equipment-heavy, with equipment cost as the dominant cost component? | FAIL: Wrong subsystem ID. Expected 18.0, got 2.0.
- Q: Find severe overruns. | FAIL: Missing expected generic number: 15.0 | FAIL: Missing expected generic number: 2.0 | FAIL: Missing expected generic number: 18.0 | FAIL: Missing expected generic number: 24.0 | FAIL: Missing expected generic number: 29.0 | FAIL: Missing expected generic number: 37.0 | FAIL: Missing expected generic number: 51.0 | FAIL: Missing expected generic number: 69.0 | FAIL: Missing expected generic number: 72.0 | FAIL: Missing expected generic number: 74.0 | FAIL: Missing expected generic number: 76.0 | FAIL: Missing expected generic number: 85.0 | FAIL: Missing expected generic number: 91.0 | FAIL: Missing expected generic number: 97.0

## ⚠️ Deep Dive: Warnings
*No warnings!*
