from collections import defaultdict


class DataIndex:
    """
    Build structured + fast lookup index from chunks.json
    """

    def __init__(self, chunks):
        self.chunks = chunks

        self.struct_index = defaultdict(list)

        self.sku_index = defaultdict(list)

        self._build()

    def _build(self):

        for item in self.chunks:

            if not isinstance(item, dict):
                continue

            meta = item.get("metadata", {})

            sku = meta.get("sku")
            field = meta.get("field")

            text = item.get("text")

            if sku and field and text:
                self.struct_index[(sku, field)].append(text)
                self.sku_index[sku].append(item)

    def get(self, sku, field):
        results = self.struct_index.get((sku, field), [])
        return results[0] if results else None

    def get_multi(self, skus, field):
        results = {}

        for sku in skus:
            texts = self.struct_index.get((sku, field), [])
            if texts:
                results[sku] = texts[0]

        return results if results else None