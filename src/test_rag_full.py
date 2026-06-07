from rag_pipeline import RAGPipeline

rag = RAGPipeline()

while True:

    q = input("\nQuestion: ")

    result = rag.query(q)

    print(result.get("answer", ""))