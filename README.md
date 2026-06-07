# GIGABYTE AORUS MASTER 16 AM6H Hardware Assistant

---

# System Architecture

```text
User Question
      │
      ▼
LLM Query Parser
      │
      ▼
Structured Retrieval
      │
      ▼
FAISS Semantic Search
      │
      ▼
Retrieved Chunks
      │
      ▼
Prompt Builder
      │
      ▼
Stream Generation
      │
      ▼
Answer
```

---

# Quick Start

## 1. Clone Repository

```bash
git clone https://github.com/rebecca-liu-siyu/GIGABYTE-RAG-system.git

cd rag_project
```

---

## 2. Install Dependencies

```bash
uv sync
```

---

## 3. Download LLM Model

Download the following model and place it in the specified path.

[Qwen2.5-3B-Instruct-Q4_k_M](https://huggingface.co/JackeyLai/Qwen2.5-3B-Instruct-Q4_K_M-GGUF/blob/main/qwen2.5-3b-instruct-q4_k_m.gguf)

```text
rag_project/
└── models/
    └── qwen2.5-3b-instruct-q4_k_m.gguf
```

---

## 4. Start llama.cpp Server

Download llama.cpp

[llama.cpp Releases](https://github.com/ggml-org/llama.cpp/releases?utm_source=chatgpt.com)

Make sure the following files existed.

```text
C:\llama\
├── llama-server.exe
└── llama-cli.exe
```

Enter the folder.

```powershell
cd C:\llama
```

Use the following cmd to run the model.

```powershell
.\llama-server.exe -m "C:\path\to\rag_project\models\qwen2.5-3b-instruct-q4_k_m.gguf" -c 4096 --host 127.0.0.1 --port 8080
```

---

## 6. Run Interactive QA

Use the following cmd to run interactive QA assistant.

```bash
uv run src/test_rag_full.py
```

Example：

```text
Question:
BZH 的CPU是什麼？
```

Output：

```text
Intel Core Ultra 9 Processor 275HX
```

---

## Benchmark Evaluation

Use the following cmd to run the benchmark evaluation

```bash
uv run src/evaluation.py
```

You can replace this dataset with your own.

```text
data/benchmark_dataset.json
```

The dataset must include:

```json
{
  "id": "...",
  "question": "..."
}
```

The system will output the following information:

```text
Average Parser TTFT
Average Retrieval Latency
Average Generator TTFT
Average Generator TPS
```

And the result will be saved at:

```text
benchmark_results.json
```

---

# Evaluation Methodology

## Benchmark Dataset

To evaluate the proposed RAG system, a custom benchmark dataset was created based on the official product specification page of the GIGABYTE AORUS MASTER 16 AM6H.

The dataset contains four categories of questions:

| Category                         |  Count |
| -------------------------------- | -----: |
| Retrieval (Single Fact)          |      4 |
| Retrieval (Comparison / Ranking) |      4 |
| Hallucination Detection          |      4 |
| Reasoning / Inference            |      4 |
| **Total**                        | **16** |

The benchmark includes:

* Traditional Chinese questions
* English questions
* Mixed Chinese-English questions

to evaluate multilingual query support.

---

## Quantitative Metrics

The following metrics were collected during evaluation:

### Parser TTFT (Time To First Token)

Measures the latency of the LLM-based query parser.

```text
User Query
    ↓
LLM Parser
    ↓
First Token
```

### Generator TTFT (Time To First Token)

Measures the latency of the final answer generation stage.

```text
Retrieved Context
    ↓
LLM Generator
    ↓
First Token
```

### TPS (Tokens Per Second)

Measures the average token generation throughput during answer generation.

---

## Quantitative Results

All models were evaluated using the same pipeline.

### Performance Comparison

| Model               | Avg Parser TTFT (s) | Avg Generator TTFT (s) | Avg TPS |
| ------------------- | ------------------: | ---------------------: | ------: |
| Qwen2.5-3B-Instruct |               1.742 |                  1.836 |  12.255 |
| Gemma 3 4B          |               5.710 |                  6.869 |   2.859 |
| Llama 3.2 3B        |               1.739 |                  9.180 |   2.906 |

## Analysis

**Qwen2.5-3B-Instruct** achieved the best overall performance across all latency and throughput metrics.

---

## Qualitative Results

| Model               | Correct Answers | Accuracy |
| ------------------- | --------------: | -------: |
| Qwen2.5-3B-Instruct |         15 / 16 |   93.75% |
| Gemma 3 4B          |         13 / 16 |   81.25% |
| Llama 3.2 3B        |         14 / 16 |   87.50% |


All benchmark questions were manually reviewed.

A response is considered **correct** if it contains the required information from the specification and does not introduce critical factual errors.

### Error Analysis

**Qwen2.5-3B-Instruct**

* Highest overall accuracy
* Strong multilingual understanding
* Occasionally outputs Simplified Chinese characters
* No significant factual errors observed

**Gemma 3 4B**

* Lower retrieval utilization efficiency
* Weaker performance on comparison and reasoning questions
* Less consistent handling of mixed Chinese-English queries

**Gemma 3 4B**

* Good factual accuracy
* Occasionally generates pinyin-like or unexpected language outputs
* Less stable Traditional Chinese generation compared to Qwen

---

# Conclusion

Based on both quantitative and qualitative evaluations, **Qwen2.5-3B-Instruct (Q4_K_M)** provides the best performance. Therefore, it was selected as the final model for the RAG system.
