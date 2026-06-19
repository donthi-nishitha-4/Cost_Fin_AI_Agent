import csv
import json

csv_path = r"e:\Practice_Agent_for_Cost_Fin_module_N\app\data\Experiment_csvs\V3_Hybrid_Eval-561a7445.csv"

def analyze():
    failed_examples = []
    
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            math_score = int(row.get('math_score', 0))
            if math_score == 0:
                # We need to run the logic from evaluate_v3.py to see what was missing
                import re
                expected = str(json.loads(row['reference_outputs']).get('expected', ''))
                actual = str(json.loads(row['outputs']).get('result', ''))
                
                exp_nums = [float(m) for m in re.findall(r'[-+]?\d*\.\d+|[-+]?\d+', expected.replace('$', '').replace(',', ''))]
                act_nums = [float(m) for m in re.findall(r'[-+]?\d*\.\d+|[-+]?\d+', actual.replace('$', '').replace(',', ''))]
                
                missing = []
                for en in exp_nums:
                    if not any(abs(en - an) < 0.1 for an in act_nums):
                        missing.append(en)
                
                failed_examples.append({
                    "expected": expected,
                    "missing": missing
                })

    for ex in failed_examples[:3]:
        print(f"Missing Numbers: {ex['missing']} in Expected: {ex['expected']}")

if __name__ == "__main__":
    analyze()
