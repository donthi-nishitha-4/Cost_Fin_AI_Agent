# V5 Project-Grade Local Evaluation Report
    
**Date**: June 29, 2026
**Execution Engine**: Local Ollama (llama3)

## 📊 High-Level Metrics
- **Overall Pipeline Score**: 98.9% *(Weighted: 50% Math, 30% Semantic, 20% Business Logic Safety)*
- **Math Accuracy**: 99.2%
- **Semantic Quality**: 97.6%
- **Total Queries**: 124

### Severity Breakdown
- **123 Pass** (INFO: Perfect Match)
- **0 Warning** (Missing IDs but math passed)
- **1 Fail** (Wrong subsystem, missing fields)
- **0 Critical** (Sign reversals, Business logic contradictions)

### Performance Analytics
- **Total Execution Time**: 165.5 seconds
- **Average Latency**: 19.08 seconds per query
- **Slowest Response**: 148.74 seconds
- **Fastest Response**: 4.17 seconds

## 🎯 Intent Accuracy Stats
- **Aggregation**: 98.1% (51/52)
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
- Q: Find severe overruns. | FAIL: Missing expected generic number: 15.0 | FAIL: Missing expected generic number: 18.0 | FAIL: Missing expected generic number: 24.0 | FAIL: Missing expected generic number: 29.0 | FAIL: Missing expected generic number: 37.0 | FAIL: Missing expected generic number: 51.0 | FAIL: Missing expected generic number: 69.0 | FAIL: Missing expected generic number: 72.0 | FAIL: Missing expected generic number: 74.0 | FAIL: Missing expected generic number: 76.0 | FAIL: Missing expected generic number: 85.0 | FAIL: Missing expected generic number: 91.0 | FAIL: Missing expected generic number: 97.0

## ⚠️ Deep Dive: Warnings
*No warnings!*
