# V5 Project-Grade Evaluation Report

**Date**: June 26, 2026
**Test Run**: `V5_Strict_Golden-d2d97bb7`

## 📊 High-Level Metrics
- **Total Queries**: 100
- **Math Accuracy**: 90.0%
- **Semantic Quality**: 78.0%

### Severity Breakdown
- **90 Pass** (INFO: Perfect Match)
- **0 Warning** (Missing IDs but math passed)
- **10 Fail** (Wrong subsystem, missing fields)
- **0 Critical** (Sign reversals, Business logic contradictions)

## 🎯 Intent Accuracy Stats
- **Aggregation**: 93.8% (30/32)
- **Budget Status**: 66.7% (10/15)
- **Cost Breakdown**: 100.0% (5/5)
- **Equipment Cost**: 83.3% (5/6)
- **Labor Cost**: 83.3% (5/6)
- **Material Cost**: 83.3% (5/6)
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
- FAIL: Missing expected generic number: 60.0 | FAIL: Missing expected generic number: 7.0 | FAIL: Missing expected generic number: 2.0 | FAIL: Missing expected generic number: 2.0
- WARNING: Missing subsystem ID. | FAIL: Missing expected generic number: 0.0 | FAIL: Missing expected generic number: 150000.0 | FAIL: Missing expected generic number: 150000.0
- WARNING: Missing subsystem ID. | FAIL: Missing required field 'labor'. Expected 45303.24.
- WARNING: Missing subsystem ID. | FAIL: Missing required field 'material'. Expected 57287.05.
- WARNING: Missing subsystem ID. | FAIL: Missing required field 'equipment'. Expected 31635.68.
