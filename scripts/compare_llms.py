import os
import time
import sys

# Add the project root to the python path so it can find the 'app' module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from app.agents.finance_agent_v2 import ask_finance_agent_v2
import app.core.llm_factory

load_dotenv()

QUERIES = [
    "What is the cost breakdown for subsystem 17?",
    "Is subsystem 11 over budget?",
    "Show equipment cost for subsystem 6.",
    "Which subsystem has the largest planned cost?",
    "Give me a financial summary of subsystem 36."
]

def run_shootout():
    print("=== Phase 6: LLM Shootout (Ollama vs Groq) ===\n")
    
    results_ollama = []
    results_groq = []
    
    # --- TEST OLLAMA ---
    print("Testing Local Ollama (llama3)...")
    os.environ["LLM_PROVIDER"] = "ollama"
    
    # We must reset the instances so the factory builds the new one
    app.core.llm_factory._ollama_instance = None
    app.core.llm_factory._groq_instance = None
    
    for i, q in enumerate(QUERIES):
        print(f"  [Ollama] Query {i+1}...")
        start_time = time.time()
        try:
            ans = ask_finance_agent_v2(q)
            ans_text = ans.get("answer", str(ans))
        except Exception as e:
            ans_text = f"ERROR: {e}"
        latency = time.time() - start_time
        results_ollama.append({"latency": latency, "answer": ans_text})

    # --- TEST GROQ ---
    print("\nTesting Cloud Groq (llama3-8b-8192)...")
    os.environ["LLM_PROVIDER"] = "groq"
    
    app.core.llm_factory._ollama_instance = None
    app.core.llm_factory._groq_instance = None
    
    for i, q in enumerate(QUERIES):
        print(f"  [Groq] Query {i+1}...")
        start_time = time.time()
        try:
            ans = ask_finance_agent_v2(q)
            ans_text = ans.get("answer", str(ans))
        except Exception as e:
            ans_text = f"ERROR: {e}"
        latency = time.time() - start_time
        results_groq.append({"latency": latency, "answer": ans_text})

    # --- GENERATE REPORT ---
    print("\nGenerating Shootout Report...")
    
    md_content = "# Phase 6: Multi-LLM Shootout (Ollama vs Groq)\n\n"
    
    avg_ollama = sum(r["latency"] for r in results_ollama) / len(results_ollama)
    avg_groq = sum(r["latency"] for r in results_groq) / len(results_groq)
    
    md_content += f"### ⏱️ Latency Comparison\n"
    md_content += f"- **Local Ollama (Llama 3 8B):** {avg_ollama:.2f} seconds avg\n"
    md_content += f"- **Cloud Groq (Llama 3.1 8B):** {avg_groq:.2f} seconds avg\n"
    speedup = avg_ollama / avg_groq if avg_groq > 0 else 0
    md_content += f"- **Speedup:** {speedup:.1f}x Faster!\n\n"
    
    md_content += "### 🥊 Query-by-Query Shootout\n\n"
    
    for i, q in enumerate(QUERIES):
        md_content += f"#### Query {i+1}: `{q}`\n"
        md_content += f"**Ollama** ({results_ollama[i]['latency']:.2f}s):\n> {results_ollama[i]['answer']}\n\n"
        md_content += f"**Groq** ({results_groq[i]['latency']:.2f}s):\n> {results_groq[i]['answer']}\n\n"
        md_content += "---\n\n"
        
    report_path = os.path.join("docs", "llm_shootout.md")
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(md_content)
        
    print(f"\nDone! Shootout report saved to {report_path}")

if __name__ == "__main__":
    run_shootout()
