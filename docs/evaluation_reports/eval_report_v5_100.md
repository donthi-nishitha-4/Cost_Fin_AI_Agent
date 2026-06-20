# V5 Project-Grade Evaluation Report

**Date**: June 20, 2026
**Test Run**: `V5_Strict_Golden-fda75b4b`

## 📊 High-Level Metrics
- **Total Queries**: 100
- **Math Accuracy**: 92.0%
- **Semantic Quality**: 97.0%

### Severity Breakdown
- **92 Pass** (INFO: Perfect Match)
- **0 Warning** (Missing IDs but math passed)
- **8 Fail** (Wrong subsystem, missing fields)
- **0 Critical** (Sign reversals, Business logic contradictions)

## 🎯 Intent Accuracy Stats
- **Aggregation**: 90.6% (29/32)
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
- FAIL: Missing expected generic number: 60.0 | FAIL: Missing expected generic number: 7.0
- FAIL: Missing expected generic number: 380000.0
- FAIL: Missing expected generic number: 3.0 | FAIL: Missing expected generic number: 12469.17
