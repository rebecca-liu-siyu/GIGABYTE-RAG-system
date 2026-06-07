import json
import time

from retriever import FAISSRetriever
from prompt import build_prompt
from generate import stream_generate
from llm_parser import llm_parse_query

from data_index import DataIndex

def structured_lookup_multi(index, skus, field):
    return index.get_multi(skus, field)


class RAGPipeline:

    def __init__(self):

        with open("data/chunks.json", "r", encoding="utf-8") as f:
            raw = json.load(f)
            
        self.chunks = raw

        self.index = DataIndex(self.chunks)

        self.retriever = FAISSRetriever()

    def query(self, user_query: str):

        # =========================
        # 1. PARSER
        # =========================
        t0 = time.perf_counter()
        intent = llm_parse_query(user_query)
        parser_ttft = time.perf_counter() - t0

        skus = intent.get("skus", [])
        field = intent.get("field", None)

        if not skus:
            skus = list(self.index.sku_index.keys())

        # =========================
        # 2. STRUCTURED RETRIEVAL
        # =========================
        structured_context = None

        if field:
            structured_context = structured_lookup_multi(
                self.index,
                skus,
                field
            )

        # =========================
        # 3. VECTOR RETRIEVAL
        # =========================
        contexts = self.retriever.search(user_query, k=3)

        # =========================
        # 4. PROMPT
        # =========================
        prompt = build_prompt(
            user_query,
            contexts,
            structured_context=structured_context
        )

        # =========================
        # 5. GENERATE
        # =========================
        gen_result = stream_generate(prompt)

        return {
            "answer": gen_result["text"],
            "parser_ttft": parser_ttft,
            "ttft": gen_result["ttft"],
            "tps": gen_result["tps"]
        }