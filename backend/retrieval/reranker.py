from sentence_transformers import (
    CrossEncoder,
)

from config import settings


class Reranker:

    def __init__(self):

        self.model = CrossEncoder(
            settings.reranker_model
        )

    def rerank(
        self,
        query: str,
        documents: list[dict],
        top_k: int = 5,
    ):

        if not documents:
            return []

        pairs = [

            (
                query,
                document["text"],
            )

            for document in documents
        ]

        scores = self.model.predict(
            pairs
        )

        ranked = sorted(

            zip(
                documents,
                scores,
            ),

            key=lambda item: float(
                item[1]
            ),

            reverse=True,
        )

        output = []

        for document, score in (
            ranked[:top_k]
        ):

            document = document.copy()

            document[
                "rerank_score"
            ] = float(score)

            output.append(
                document
            )

        return output


reranker = Reranker()