import requests
import time
import json


def stream_generate(prompt: str):
    url = "http://127.0.0.1:8080/v1/chat/completions"

    payload = {
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1,
        "stream": True
    }

    start = time.perf_counter()
    first_token_time = None

    r = requests.post(url, json=payload, stream=True)

    output = ""
    token_count = 0

    for line in r.iter_lines():
        if not line:
            continue

        line = line.decode("utf-8")

        if not line.startswith("data:"):
            continue

        data = line[5:].strip()

        if data == "[DONE]":
            break

        try:
            obj = json.loads(data)
            delta = obj["choices"][0]["delta"].get("content", "")

            if delta:
                if first_token_time is None:
                    first_token_time = time.perf_counter()

                output += delta
                token_count += 1

        except:
            continue

    end = time.perf_counter()

    ttft = (first_token_time - start) if first_token_time else None
    total_time = end - start
    tps = token_count / total_time if total_time > 0 else 0.0

    return {
        "text": output,
        "ttft": ttft,
        "tps": tps,
        "tokens": token_count,
        "latency": total_time
    }