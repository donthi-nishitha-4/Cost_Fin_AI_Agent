import os

report_path = r"e:\Practice_Agent_for_Cost_Fin_module_N\docs\evaluation_reports\eval_report_v5_124_ollama_llama3_local.md"
with open(report_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace literal \n with actual newlines
content = content.replace("\\n", "\n")

with open(report_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Formatting complete.")
