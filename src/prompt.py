def build_prompt(query, contexts, structured_context):

    # =========================
    # 1. FAISS context
    # =========================
    context_text = "\n\n".join(
        [c["text"] for c in contexts]
    )

    # =========================
    # 3. Build prompt
    # =========================
    prompt = f"""
You are a strict laptop specification QA system.

You must answer using ONLY the provided context.

========================
[STRUCTURED CONTEXT]
========================
{structured_context}

========================
[UNSTRUCTURED CONTEXT]
========================
{context_text}

========================
RULES:
========================
- Do not hallucinate, infer from the provided infomation.
- Be concise.
- Do NOT repeat the raw context.
- Do NOT copy any text after "*" or "(".
- If question is English, answer in English.
- If question is Chinese, answer in Traditional Chinese(繁體中文).

========================
QUESTION:
========================
{query}

========================
ANSWER:
========================
""".strip()

    return prompt