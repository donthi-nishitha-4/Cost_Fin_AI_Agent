import os
from dotenv import load_dotenv
from langsmith import Client # type: ignore
from langsmith.evaluation import evaluate # type: ignore

# Load environment variables
load_dotenv()

from app.agents.finance_agent_v2 import ask_finance_agent_v2

# Initialize LangSmith client
client = Client()

# Define the evaluation dataset
DATASET_NAME = "Cost_Finance_Evaluation"

EXAMPLES = [
    ("What is the cost breakdown for subsystem 17?", "Subsystem 17 (Water Supply - Block E) cost breakdown: Labor cost = $10,785.89, Material cost = $14,188.21, Equipment cost = $9,377.03. Sum of direct costs = $34,351.13, with the remaining $1,881.13 of the $36,232.26 actual cost attributed to indirect costs/overhead/contingency."),
    ("What is the cost breakdown for subsystem 42?", "Subsystem 42 (Mechanical Systems - Podium) cost breakdown: Labor cost = $33,899.42, Material cost = $32,670.70, Equipment cost = $11,327.86. Sum of direct costs = $77,897.98, with the remaining $9,777.01 of the $87,674.99 actual cost attributed to indirect costs/overhead/contingency."),
    ("What is the cost breakdown for subsystem 9?", "Subsystem 9 (Concrete Works - Tower A) cost breakdown: Labor cost = $5,998.07, Material cost = $4,615.69, Equipment cost = $3,843.77. Sum of direct costs = $14,457.53, with the remaining $2,528.92 of the $16,986.45 actual cost attributed to indirect costs/overhead/contingency."),
    ("What is the cost breakdown for subsystem 55?", "Subsystem 55 (Plumbing - South Wing) cost breakdown: Labor cost = $5,983.02, Material cost = $5,155.08, Equipment cost = $3,307.20. Sum of direct costs = $14,445.30, with the remaining $1,472.22 of the $15,917.52 actual cost attributed to indirect costs/overhead/contingency."),
    ("What is the cost breakdown for subsystem 63?", "Subsystem 63 (Telecommunications - West Annex) cost breakdown: Labor cost = $75,157.21, Material cost = $68,953.10, Equipment cost = $33,205.73. Sum of direct costs = $177,316.04, with the remaining $22,012.58 of the $199,328.62 actual cost attributed to indirect costs/overhead/contingency."),
    ("Show labor cost for subsystem 42.", "The labor cost for subsystem 42 (Mechanical Systems - Podium) is $33,899.42."),
    ("Show labor cost for subsystem 4.", "The labor cost for subsystem 4 (Landscaping - South Wing) is $44,955.24."),
    ("Show labor cost for subsystem 56.", "The labor cost for subsystem 56 (Parking - West Annex) is $333,390.41."),
    ("Show labor cost for subsystem 34.", "The labor cost for subsystem 34 (Plumbing - Sector 1) is $519,466.77."),
    ("Show labor cost for subsystem 23.", "The labor cost for subsystem 23 (Telecommunications - Podium) is $190,127.97."),
    ("Show material cost for subsystem 5.", "The material cost for subsystem 5 (Facade - East Annex) is $137,799.22."),
    ("Show material cost for subsystem 14.", "The material cost for subsystem 14 (Concrete Works - Zone 7) is $134,668.02."),
    ("Show material cost for subsystem 79.", "The material cost for subsystem 79 (Site Development - East Annex) is $177,527.56."),
    ("Show material cost for subsystem 53.", "The material cost for subsystem 53 (Site Development - Central Plant) is $231,815.25."),
    ("Show material cost for subsystem 88.", "The material cost for subsystem 88 (Landscaping - Extension) is $191,519.86."),
    ("Show equipment cost for subsystem 6.", "The equipment cost for subsystem 6 (Elevators - Tower A) is $154,845.43."),
    ("Show equipment cost for subsystem 2.", "The equipment cost for subsystem 2 (Structural Steel - Tower B) is $543,532.47."),
    ("Show equipment cost for subsystem 39.", "The equipment cost for subsystem 39 (Roofing - Block D) is $106,112.50."),
    ("Show equipment cost for subsystem 64.", "The equipment cost for subsystem 64 (Elevators - East Annex) is $87,815.30."),
    ("Show equipment cost for subsystem 18.", "The equipment cost for subsystem 18 (Interior Finishing - Phase 2) is $143,019.88."),
    ("Is subsystem 51 over budget?", "Subsystem 51 (Landscaping - Building C) has no planned budget (planned_cost = $0.00), so 'over budget' isn't applicable in the traditional sense. It is unplanned work with an actual cost of $45,695.84."),
    ("Is subsystem 11 over budget?", "Yes, subsystem 11 (Roofing - Basement Level) is over budget. Planned cost = $184,337.39, actual cost = $211,918.12, variance = +$27,580.73."),
    ("Is subsystem 7 over budget?", "No, subsystem 7 (Roads - Sector 1) is under budget. Planned cost = $500,000.00, actual cost = $210,000.00, variance = -$290,000.00 (i.e., $290,000.00 under)."),
    ("Is subsystem 33 over budget?", "Yes, subsystem 33 (Security - Podium) is over budget. Planned cost = $558,784.87, actual cost = $568,279.02, variance = +$9,494.15."),
    ("Is subsystem 13 over budget?", "Yes, subsystem 13 (Electrical - Podium) is over budget. Planned cost = $19,520.19, actual cost = $19,850.04, variance = +$329.85."),
    ("Compare planned and actual cost for subsystem 29.", "Subsystem 29 (Security - Main Building): planned cost = $135,537.38, actual cost = $178,261.69, variance = $42,724.31 (over)."),
    ("Compare planned and actual cost for subsystem 30.", "Subsystem 30 (Site Development - South Wing): planned cost = $686,882.17, actual cost = $417,457.16, variance = -$269,425.01 (under)."),
    ("Compare planned and actual cost for subsystem 1.", "Subsystem 1 (Fire Protection - Tower A): planned cost = $150,000.00, actual cost = $150,000.00, variance = $0.00 (exact match)."),
    ("Compare planned and actual cost for subsystem 8.", "Subsystem 8 (Water Supply - Phase 2): planned cost = $700,000.00, actual cost = $180,000.00, variance = -$520,000.00 (under)."),
    ("Compare planned and actual cost for subsystem 38.", "Subsystem 38 (Structural Steel - South Wing): planned cost = $50,338.26, actual cost = $52,480.53, variance = $2,142.27 (over)."),
    ("Is subsystem 21 under budget?", "Yes, subsystem 21 (Telecommunications - Wing 3) is under budget. Planned cost = $48,431.16, actual cost = $28,150.30, variance = -$20,280.86."),
    ("Is subsystem 45 under budget?", "Yes, subsystem 45 (Water Supply - Sector 2) is under budget. Planned cost = $681,753.17, actual cost = $565,960.74, variance = -$115,792.43."),
    ("Is subsystem 83 under budget?", "Yes, subsystem 83 (Concrete Works - Sector 2) is under budget. Planned cost = $148,345.16, actual cost = $86,868.63, variance = -$61,476.53."),
    ("Is subsystem 20 under budget?", "Yes, subsystem 20 (Fire Protection - Building C) is under budget. Planned cost = $684,385.22, actual cost = $521,129.32, variance = -$163,255.90."),
    ("Is subsystem 70 under budget?", "Yes, subsystem 70 (Structural Steel - Zone 7) is under budget. Planned cost = $643,477.65, actual cost = $424,933.01, variance = -$218,544.64."),
    ("What is the variance for subsystem 10?", "The variance for subsystem 10 (Wastewater - Block E) is $6,395.05 (actual $37,502.00 minus planned $31,106.95), indicating an overrun."),
    ("What is the variance for subsystem 19?", "The variance for subsystem 19 (Water Supply - Basement Level) is $72,173.80 (actual $313,637.33 minus planned $241,463.53), indicating an overrun."),
    ("What is the variance for subsystem 46?", "The variance for subsystem 46 (Plumbing - Sector 2) is $9,572.11 (actual $51,736.50 minus planned $42,164.39), indicating an overrun."),
    ("What is the variance for subsystem 58?", "The variance for subsystem 58 (Concrete Works - Building C) is $15,038.97 (actual $116,287.71 minus planned $101,248.74), indicating an overrun."),
    ("What is the variance for subsystem 80?", "The variance for subsystem 80 (Concrete Works - Basement Level) is $19,114.76 (actual $162,854.35 minus planned $143,739.59), indicating an overrun."),
    ("What is the remaining budget for subsystem 8?", "The remaining budget for subsystem 8 (Water Supply - Phase 2) is $520,000.00 (planned $700,000.00 minus actual $180,000.00)."),
    ("What is the remaining budget for subsystem 7?", "The remaining budget for subsystem 7 (Roads - Sector 1) is $290,000.00 (planned $500,000.00 minus actual $210,000.00)."),
    ("What is the remaining budget for subsystem 30?", "The remaining budget for subsystem 30 (Site Development - South Wing) is $269,425.01 (planned $686,882.17 minus actual $417,457.16)."),
    ("What is the remaining budget for subsystem 53?", "The remaining budget for subsystem 53 (Site Development - Central Plant) is $211,689.15 (planned $616,172.11 minus actual $404,482.96)."),
    ("What is the remaining budget for subsystem 70?", "The remaining budget for subsystem 70 (Structural Steel - Zone 7) is $218,544.64 (planned $643,477.65 minus actual $424,933.01)."),
    ("What is the overrun risk for subsystem 63?", "Subsystem 63 (Telecommunications - West Annex) has consumed 85.21% of its planned cost (planned = $233,923.53, actual = $199,328.62), which is classified as LOW overrun risk."),
    ("What is the overrun risk for subsystem 2?", "Subsystem 2 (Structural Steel - Tower B) has consumed 163.33% of its planned cost (planned = $600,000.00, actual = $980,000.00), which is classified as HIGH overrun risk."),
    ("What is the overrun risk for subsystem 29?", "Subsystem 29 (Security - Main Building) has consumed 131.52% of its planned cost (planned = $135,537.38, actual = $178,261.69), which is classified as HIGH overrun risk."),
    ("What is the overrun risk for subsystem 76?", "Subsystem 76 (Mechanical Systems - Tower B) has consumed 142.40% of its planned cost (planned = $405,840.93, actual = $577,898.66), which is classified as HIGH overrun risk."),
    ("What is the overrun risk for subsystem 39?", "Subsystem 39 (Roofing - Block D) has consumed 180.72% of its planned cost (planned = $239,774.90, actual = $433,325.10), which is classified as HIGH overrun risk."),
    ("What percentage of planned cost has subsystem 48 consumed?", "Subsystem 48 (Water Supply - Central Plant) has consumed 116.24% of its planned cost ($1,068,279.63 actual vs $919,015.22 planned)."),
    ("What percentage of planned cost has subsystem 34 consumed?", "Subsystem 34 (Plumbing - Sector 1) has consumed 111.34% of its planned cost ($995,304.08 actual vs $893,944.94 planned)."),
    ("What percentage of planned cost has subsystem 81 consumed?", "Subsystem 81 (Mechanical Systems - South Wing) has consumed 120.49% of its planned cost ($964,997.95 actual vs $800,900.44 planned)."),
    ("What percentage of planned cost has subsystem 19 consumed?", "Subsystem 19 (Water Supply - Basement Level) has consumed 129.89% of its planned cost ($313,637.33 actual vs $241,463.53 planned)."),
    ("What percentage of planned cost has subsystem 64 consumed?", "Subsystem 64 (Elevators - East Annex) has consumed 127.16% of its planned cost ($400,547.72 actual vs $314,997.17 planned)."),
    ("Is subsystem 7 low risk for overrun?", "Yes, subsystem 7 (Roads - Sector 1) is classified as LOW risk, having consumed only 42.00% of its planned cost."),
    ("Is subsystem 9 low risk for overrun?", "Yes, subsystem 9 (Concrete Works - Tower A) is classified as LOW risk, having consumed only 57.70% of its planned cost."),
    ("Is subsystem 30 low risk for overrun?", "Yes, subsystem 30 (Site Development - South Wing) is classified as LOW risk, having consumed only 60.78% of its planned cost."),
    ("Is subsystem 70 low risk for overrun?", "Yes, subsystem 70 (Structural Steel - Zone 7) is classified as LOW risk, having consumed only 66.04% of its planned cost."),
    ("Is subsystem 83 low risk for overrun?", "Yes, subsystem 83 (Concrete Works - Sector 2) is classified as LOW risk, having consumed only 58.56% of its planned cost."),
    ("Give me a financial summary of subsystem 11.", "Financial summary for subsystem 11 (Roofing - Basement Level): planned cost = $184,337.39, actual cost = $211,918.12, remaining budget = -$27,580.73, variance = $27,580.73, status = over budget."),
    ("Give me a financial summary of subsystem 25.", "Financial summary for subsystem 25 (Facade - Tower A): planned cost = $527,145.32, actual cost = $578,731.36, remaining budget = -$51,586.04, variance = $51,586.04, status = over budget."),
    ("Give me a financial summary of subsystem 33.", "Financial summary for subsystem 33 (Security - Podium): planned cost = $558,784.87, actual cost = $568,279.02, remaining budget = -$9,494.15, variance = $9,494.15, status = over budget."),
    ("Give me a financial summary of subsystem 60.", "Financial summary for subsystem 60 (Roofing - Tower A): planned cost = $216,114.33, actual cost = $241,677.17, remaining budget = -$25,562.84, variance = $25,562.84, status = over budget."),
    ("Give me a financial summary of subsystem 81.", "Financial summary for subsystem 81 (Mechanical Systems - South Wing): planned cost = $800,900.44, actual cost = $964,997.95, remaining budget = -$164,097.51, variance = $164,097.51, status = over budget."),
    ("Give me a financial summary of subsystem 100.", "Financial summary for subsystem 100 (Foundation - Main Building): planned cost = $758,208.16, actual cost = $832,447.47, remaining budget = -$74,239.31, variance = $74,239.31, status = over budget."),
    ("Give me a financial summary of subsystem 44.", "Financial summary for subsystem 44 (Fire Protection - East Annex): planned cost = $360,515.47, actual cost = $344,155.77, remaining budget = $16,359.70, variance = -$16,359.70, status = under budget."),
    ("Give me a financial summary of subsystem 57.", "Financial summary for subsystem 57 (Electrical - North Block): planned cost = $399,520.51, actual cost = $380,358.71, remaining budget = $19,161.80, variance = -$19,161.80, status = under budget."),
    ("Give me a financial summary of subsystem 93.", "Financial summary for subsystem 93 (Roads - Phase 1): planned cost = $57,403.92, actual cost = $42,817.21, remaining budget = $14,586.71, variance = -$14,586.71, status = under budget."),
    ("Give me a financial summary of subsystem 96.", "Financial summary for subsystem 96 (Electrical - Central Plant): planned cost = $35,246.44, actual cost = $32,044.74, remaining budget = $3,201.70, variance = -$3,201.70, status = under budget."),
    ("Give me a financial summary of subsystem 17.", "Financial summary for subsystem 17 (Water Supply - Block E): planned cost = $36,085.80, actual cost = $36,232.26, remaining budget = -$146.46, variance = $146.46, status = over budget."),
    ("Give me a financial summary of subsystem 26.", "Financial summary for subsystem 26 (Telecommunications - North Block): planned cost = $160,920.46, actual cost = $167,868.30, remaining budget = -$6,947.84, variance = $6,947.84, status = over budget."),
    ("Give me a financial summary of subsystem 36.", "Financial summary for subsystem 36 (Roads - Block E): planned cost = $11,104.02, actual cost = $11,522.68, remaining budget = -$418.66, variance = $418.66, status = over budget."),
    ("Give me a financial summary of subsystem 68.", "Financial summary for subsystem 68 (Site Development - Wing 3): planned cost = $249,326.29, actual cost = $250,582.61, remaining budget = -$1,256.32, variance = $1,256.32, status = over budget."),
    ("Give me a financial summary of subsystem 75.", "Financial summary for subsystem 75 (Telecommunications - Sector 1): planned cost = $138,544.20, actual cost = $143,534.10, remaining budget = -$4,989.90, variance = $4,989.90, status = over budget."),
    ("Which subsystem has zero planned budget?", "There are 5 subsystems with zero planned budget (unplanned work): Subsystem 24 (Site Development - Sector 2, actual cost $45,000.00), Subsystem 37 (Electrical - Tower B, actual cost $63,982.11), Subsystem 51 (Landscaping - Building C, actual cost $45,695.84), Subsystem 72 (Wastewater - Tower B, actual cost $40,204.77), Subsystem 85 (Roads - Wing 3, actual cost $70,202.56)."),
    ("Find severe overruns.", "There are 10 subsystems with severe overruns (actual cost exceeding 130% of planned cost): Subsystem 39 (Roofing - Block D, 180.72% of planned), Subsystem 97 (Plumbing - Tower B, 179.78% of planned), Subsystem 18 (Interior Finishing - Phase 2, 177.69% of planned), Subsystem 74 (Fire Protection - Main Building, 172.28% of planned), Subsystem 69 (Interior Finishing - Tower B, 171.12% of planned), Subsystem 2 (Structural Steel - Tower B, 163.33% of planned), Subsystem 91 (Landscaping - Main Building, 160.80% of planned), Subsystem 84 (Fire Protection - Sector 1, 155.56% of planned), Subsystem 76 (Mechanical Systems - Tower B, 142.40% of planned), Subsystem 29 (Security - Main Building, 131.52% of planned)."),
    ("Which subsystem exceeded budget by the highest amount?", "Subsystem 2 (Structural Steel - Tower B) exceeded its budget by the highest amount: $380,000.00 over (planned $600,000.00, actual $980,000.00)."),
    ("Which subsystem has the largest underspend compared to its planned budget?", "Subsystem 8 (Water Supply - Phase 2) has the largest underspend: $520,000.00 under budget (planned $700,000.00, actual $180,000.00)."),
    ("Which subsystem has the highest planned cost?", "Subsystem 48 (Water Supply - Central Plant) has the highest planned cost at $919,015.22."),
    ("Which subsystem has planned cost exactly equal to actual cost?", "Subsystem 1 (Fire Protection - Tower A) has planned cost exactly equal to actual cost: both are $150,000.00, resulting in zero variance."),
    ("Which subsystem has the lowest non-zero planned budget, and what is its actual cost?", "Subsystem 90 (Elevators - Wing 3) has the lowest non-zero planned budget at $10,102.61, with an actual cost of $12,469.17 (variance of $2,366.56)."),
    ("Which subsystem is labor-heavy, with labor cost as the dominant cost component?", "Subsystem 4 (Landscaping - South Wing) is labor-heavy: labor cost = $44,955.24, which is the largest of the three direct cost components (material = $17,194.34, equipment = $7,133.54)."),
    ("Which subsystem is material-heavy, with material cost as the dominant cost component?", "Subsystem 5 (Facade - East Annex) is material-heavy: material cost = $137,799.22, which is the largest of the three direct cost components (labor = $46,567.44, equipment = $18,088.49)."),
    ("Which subsystem is equipment-heavy, with equipment cost as the dominant cost component?", "Subsystem 6 (Elevators - Tower A) is equipment-heavy: equipment cost = $154,845.43, which is the largest of the three direct cost components (labor = $48,391.30, material = $68,567.42)."),
    ("What is the weather in London?", "This query is outside the scope of the Cost Finance AI Agent, which is designed to answer questions about construction subsystem cost breakdowns, budget comparisons, overrun risk, and financial summaries. Please ask a question related to subsystem cost or budget data."),
    ("Who won the football match yesterday?", "This query is outside the scope of the Cost Finance AI Agent, which is designed to answer questions about construction subsystem cost breakdowns, budget comparisons, overrun risk, and financial summaries. Please ask a question related to subsystem cost or budget data."),
    ("What's the capital of France?", "This query is outside the scope of the Cost Finance AI Agent, which is designed to answer questions about construction subsystem cost breakdowns, budget comparisons, overrun risk, and financial summaries. Please ask a question related to subsystem cost or budget data."),
    ("Can you book a flight to New York for me?", "This query is outside the scope of the Cost Finance AI Agent, which is designed to answer questions about construction subsystem cost breakdowns, budget comparisons, overrun risk, and financial summaries. Please ask a question related to subsystem cost or budget data."),
    ("What is the current stock price of Tesla?", "This query is outside the scope of the Cost Finance AI Agent, which is designed to answer questions about construction subsystem cost breakdowns, budget comparisons, overrun risk, and financial summaries. Please ask a question related to subsystem cost or budget data."),
    ("Tell me a joke.", "This query is outside the scope of the Cost Finance AI Agent, which is designed to answer questions about construction subsystem cost breakdowns, budget comparisons, overrun risk, and financial summaries. Please ask a question related to subsystem cost or budget data."),
    ("What's the recipe for chocolate chip cookies?", "This query is outside the scope of the Cost Finance AI Agent, which is designed to answer questions about construction subsystem cost breakdowns, budget comparisons, overrun risk, and financial summaries. Please ask a question related to subsystem cost or budget data."),
    ("Who is the president of the United States?", "This query is outside the scope of the Cost Finance AI Agent, which is designed to answer questions about construction subsystem cost breakdowns, budget comparisons, overrun risk, and financial summaries. Please ask a question related to subsystem cost or budget data."),
    ("Translate 'good morning' into Spanish.", "This query is outside the scope of the Cost Finance AI Agent, which is designed to answer questions about construction subsystem cost breakdowns, budget comparisons, overrun risk, and financial summaries. Please ask a question related to subsystem cost or budget data."),
    ("What movies are playing in theaters this week?", "This query is outside the scope of the Cost Finance AI Agent, which is designed to answer questions about construction subsystem cost breakdowns, budget comparisons, overrun risk, and financial summaries. Please ask a question related to subsystem cost or budget data."),
    ("How do I reset my email password?", "This query is outside the scope of the Cost Finance AI Agent, which is designed to answer questions about construction subsystem cost breakdowns, budget comparisons, overrun risk, and financial summaries. Please ask a question related to subsystem cost or budget data."),
    ("What's the latest news headline today?", "This query is outside the scope of the Cost Finance AI Agent, which is designed to answer questions about construction subsystem cost breakdowns, budget comparisons, overrun risk, and financial summaries. Please ask a question related to subsystem cost or budget data."),
    ("Can you write a poem about the ocean?", "This query is outside the scope of the Cost Finance AI Agent, which is designed to answer questions about construction subsystem cost breakdowns, budget comparisons, overrun risk, and financial summaries. Please ask a question related to subsystem cost or budget data."),
    ("What time zone is Tokyo in?", "This query is outside the scope of the Cost Finance AI Agent, which is designed to answer questions about construction subsystem cost breakdowns, budget comparisons, overrun risk, and financial summaries. Please ask a question related to subsystem cost or budget data."),
    ("How many calories are in a banana?", "This query is outside the scope of the Cost Finance AI Agent, which is designed to answer questions about construction subsystem cost breakdowns, budget comparisons, overrun risk, and financial summaries. Please ask a question related to subsystem cost or budget data."),
]

def setup_dataset():
    # Delete if exists to recreate fresh
    if client.has_dataset(dataset_name=DATASET_NAME):
        client.delete_dataset(dataset_name=DATASET_NAME)
        
    dataset = client.create_dataset(
        dataset_name=DATASET_NAME,
        description="Evaluation dataset for Cost Finance Agent V2"
    )
    
    for question, expected_answer in EXAMPLES:
        client.create_example(
            inputs={"query": question},
            outputs={"expected": expected_answer},
            dataset_id=dataset.id,
        )
    return dataset

# The target function to evaluate
def agent_target(inputs: dict) -> dict:
    query = inputs["query"]
    # We expect our agent to return a dictionary with an 'answer' field
    result = ask_finance_agent_v2(query)
    # the evaluator needs a string output usually, or a dict matching the outputs schema
    return {"result": result.get("answer", str(result))}

def main():
    print("Setting up LangSmith Evaluation Dataset...")
    dataset = setup_dataset()
    print(f"Dataset '{DATASET_NAME}' created.")
    
    print("\nStarting evaluation. This will run the agent against all examples...")
    
    # Initialize our Judge LLM (Ollama)
    from langchain_ollama import OllamaLLM # type: ignore
    judge_llm = OllamaLLM(model="llama3", temperature=0.0)

    # LLM-as-a-Judge semantic evaluator
    def semantic_match(run, example):
        prediction = str(run.outputs.get("result", ""))
        reference = str(example.outputs.get("expected", ""))
        query = str(example.inputs.get("query", ""))
        
        prompt = f"""You are an expert evaluator grading an AI agent. 
Compare the ACTUAL ANSWER to the EXPECTED ANSWER.
They must have the same semantic meaning, the SAME subsystem name, and the EXACT SAME financial numbers (costs, variances, risk levels).
If the ACTUAL ANSWER answers a completely different question or refers to a different subsystem, it is INCORRECT.
If the ACTUAL ANSWER has different numbers, it is INCORRECT.
(Ignore formatting, capitalization, or extra conversational words).

If they match perfectly in facts and numbers, reply with exactly 'CORRECT'.
If they do not match, reply with exactly 'INCORRECT'.

QUERY: {query}
EXPECTED ANSWER: {reference}
ACTUAL ANSWER: {prediction}

Verdict (CORRECT or INCORRECT):"""

        verdict = judge_llm.invoke(prompt).strip().upper()
        
        # Stricter parsing
        score = 1 if verdict == "CORRECT" or verdict.startswith("CORRECT") else 0
        
        return {
            "key": "semantic_match",
            "score": score,
            "comment": verdict
        }
    
    results = evaluate(
        agent_target,
        data=DATASET_NAME,
        evaluators=[semantic_match],
        experiment_prefix="V2_Semantic_Eval",
    )
    
    print("\nEvaluation complete! Check your LangSmith dashboard for the detailed report.")

if __name__ == "__main__":
    main()
