# V5 Project-Grade Evaluation Report

**Date**: June 22, 2026
**Test Run**: `V5_Strict_Golden-523fcf01`

## 📊 High-Level Metrics
- **Total Queries**: 100
- **Math Accuracy**: 94.0%
- **Semantic Quality**: 92.0%

### Severity Breakdown
- **94 Pass** (INFO: Perfect Match)
- **0 Warning** (Missing IDs but math passed)
- **6 Fail** (Wrong subsystem, missing fields)
- **0 Critical** (Sign reversals, Business logic contradictions)

## 🎯 Intent Accuracy Stats
- **Aggregation**: 96.9% (31/32)
- **Budget Status**: 66.7% (10/15)
- **Cost Breakdown**: 100.0% (5/5)
- **Equipment Cost**: 100.0% (6/6)
- **Labor Cost**: 100.0% (6/6)
- **Material Cost**: 100.0% (6/6)
- **Unknown**: 100.0% (25/25)
- **Variance**: 100.0% (5/5)

## 🚨 Deep Dive: Critical Failures
*No critical business logic failures!*

## ❌ Deep Dive: Standard Failures
- CRITICAL: Wrong budget status. Expected under budget, got None. | FAIL: Missing required field 'variance'. Expected 290000.0.
- CRITICAL: Wrong budget status. Expected under budget, got None. | FAIL: Missing required field 'variance'. Expected 12453.169999999998.
- CRITICAL: Wrong budget status. Expected under budget, got None. | FAIL: Missing required field 'variance'. Expected 269425.01000000007.
- CRITICAL: Wrong budget status. Expected under budget, got None. | FAIL: Missing required field 'variance'. Expected 218544.64.
- CRITICAL: Wrong budget status. Expected under budget, got None. | FAIL: Missing required field 'variance'. Expected 61476.53.
- FAIL: Missing expected generic number: 60.0 | FAIL: Missing expected generic number: 2.0 | FAIL: Missing expected generic number: 2.0
