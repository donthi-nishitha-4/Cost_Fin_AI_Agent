import csv

csv_path = r"e:\Practice_Agent_for_Cost_Fin_module_N\app\data\Experiment_csvs\V3_Hybrid_Eval-561a7445.csv"

def calculate_latency():
    latencies = []
    
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                lat = float(row.get('latency', 0))
                if lat > 0:
                    latencies.append(lat)
            except ValueError:
                pass

    if latencies:
        avg_lat = sum(latencies) / len(latencies)
        max_lat = max(latencies)
        min_lat = min(latencies)
        
        print(f"Total Rows Checked: {len(latencies)}")
        print(f"Average Latency: {avg_lat:.2f} seconds")
        print(f"Min Latency: {min_lat:.2f} seconds")
        print(f"Max Latency: {max_lat:.2f} seconds")
    else:
        print("No latency data found.")

if __name__ == "__main__":
    calculate_latency()
