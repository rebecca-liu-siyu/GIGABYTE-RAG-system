import json
import re
from bs4 import BeautifulSoup


def clean_text(text: str) -> str:
    text = text.replace("\xa0", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def html_to_dict(html_file, model_names):

    with open(html_file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    titles = [
        clean_text(x.get_text(" ", strip=True))
        for x in soup.select(".spec-column .multiple-title")
    ]

    slides = soup.select(".swiper-slide")

    if len(slides) != len(model_names):
        raise ValueError(
            f"Model數({len(model_names)}) != slides數({len(slides)})"
        )

    result = {}

    for model, slide in zip(model_names, slides):

        spec_dict = {}

        items = slide.select(".spec-item-list")

        for title, item in zip(titles, items):

            value = clean_text(item.get_text(" ", strip=True))
            spec_dict[title] = value

        result[model] = spec_dict

    return result

def build_chunks(data: dict):

    chunks = []

    for sku, specs in data.items():
        text_lines = [f"Model: {sku}"]

        for k, v in specs.items():
            text_lines.append(f"{k}: {v}")

        chunks.append({
            "text": "\n".join(text_lines),
            "metadata": {
                "sku": sku,
                "type": "sku"
            }
        })

        for k, v in specs.items():

            chunks.append({
                "text": f"{sku} | {k}: {v}",
                "metadata": {
                    "sku": sku,
                    "field": k,
                    "type": "field"
                }
            })

    return chunks

if __name__ == "__main__":

    html_path = "data/spec.html"

    model_names = ["BZH", "BYH", "BXH"]

    data = html_to_dict(html_path, model_names)

    chunks = build_chunks(data)

    with open("data/chunks.json", "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    print("chunks generated:", len(chunks))