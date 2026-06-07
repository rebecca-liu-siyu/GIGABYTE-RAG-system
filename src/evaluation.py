import json
from statistics import mean
from rag_pipeline import RAGPipeline

def safe(v):
    return v if v is not None else 0.0

with open("data/benchmark_dataset.json", encoding="utf-8") as f:
    dataset = json.load(f)

rag = RAGPipeline()

results = []

for item in dataset:
    q = item["question"]
    print(f"Running {item['id']} ...")

    result = rag.query(q)

    results.append({
        "id": item["id"],
        "question": item["question"],
        "parser_ttft": safe(result.get("parser_ttft")),
        "generator_ttft": safe(result.get("ttft")),
        "tps": safe(result.get("tps")),
        "answer": result.get("answer", "")
    })

parser_avg = mean(r["parser_ttft"] for r in results)
gen_avg = mean(r["generator_ttft"] for r in results)
tps_avg = mean(r["tps"] for r in results)

print("\n===== SUMMARY =====")
print("Avg Parser TTFT:", round(parser_avg, 3))
print("Avg Generator TTFT:", round(gen_avg, 3))
print("Avg TPS:", round(tps_avg, 3))

with open("data/benchmark_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Saved benchmark_results.json")
