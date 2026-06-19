# Phase 6: Multi-LLM Shootout (Ollama vs Groq)

### ⏱️ Latency Comparison
- **Local Ollama (Llama 3 8B):** 12.44 seconds avg
- **Cloud Groq (Llama 3.1 8B):** 1.41 seconds avg
- **Speedup:** 8.8x Faster!

### 🥊 Query-by-Query Shootout

#### Query 1: `What is the cost breakdown for subsystem 17?`
**Ollama** (25.68s):
> Subsystem 17 (Water Supply - Block E) cost breakdown is labor 10785.89, material 14188.21, and equipment 9377.03.

**Groq** (1.33s):
> Subsystem 17 (Water Supply - Block E) cost breakdown is labor 10785.89, material 14188.21, and equipment 9377.03.

---

#### Query 2: `Is subsystem 11 over budget?`
**Ollama** (3.76s):
> Subsystem 11 (Roofing - Basement Level) is over_budget with a variance of -27580.72999999998 between planned cost 184337.39 and actual cost 211918.12.

**Groq** (0.20s):
> Subsystem 11 (Roofing - Basement Level) is over_budget with a variance of -27580.72999999998 between planned cost 184337.39 and actual cost 211918.12.

---

#### Query 3: `Show equipment cost for subsystem 6.`
**Ollama** (3.77s):
> Subsystem 6 (Elevators - Tower A) has a planned cost of 300000.0, actual cost of 312000.0, and remaining budget of -12000.0.

**Groq** (0.24s):
> Subsystem 6 (Elevators - Tower A) cost breakdown is labor 48391.3, material 68567.42, and equipment 154845.43.

---

#### Query 4: `Which subsystem has the largest planned cost?`
**Ollama** (24.82s):
> The Water Supply - Central Plant subsystem has the largest planned cost of $919,015.22.

**Groq** (5.07s):
> The Water Supply - Central Plant subsystem has the largest planned cost of $919,015.22.

---

#### Query 5: `Give me a financial summary of subsystem 36.`
**Ollama** (4.20s):
> Subsystem 36 (Roads - Block E) has planned cost 11104.02, actual cost 11522.68, and remaining budget -418.65999999999985. It is over_budget by -418.65999999999985 and has used 103.77% of planned cost, giving it high overrun risk.

**Groq** (0.21s):
> Subsystem 36 (Roads - Block E) has planned cost 11104.02, actual cost 11522.68, and remaining budget -418.65999999999985. It is over_budget by -418.65999999999985 and has used 103.77% of planned cost, giving it high overrun risk.

---

