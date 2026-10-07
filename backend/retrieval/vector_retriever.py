from uuid import uuid4

from sentence_transformers import (
    SentenceTransformer,
)

from qdrant_client.models import (
    PointStruct,
)

from config import settings
from services.qdrant import qdrant_service


class VectorRetriever:

    def __init__(self):

        self.model = SentenceTransformer(
            settings.embedding_model
        )

        vector_size = (
            self.model
            .get_sentence_embedding_dimension()
        )

        qdrant_service.create_collection(
            vector_size=vector_size
        )

    def embed(
        self,
        text: str,
    ) -> list[float]:

        vector = self.model.encode(
            text,
            normalize_embeddings=True,
        )

        return vector.tolist()

    def add_documents(
        self,
        chunks: list[dict],
    ) -> int:

        points = []

        for chunk in chunks:

            vector = self.embed(
                chunk["text"]
            )

            point_id = str(
                uuid4()
            )

            payload = {
                **chunk["metadata"],
                "text": chunk["text"],
            }

            points.append(
                PointStruct(

                    id=point_id,

                    vector=vector,

                    payload=payload,
                )
            )

        qdrant_service.upsert(
            points
        )

        return len(points)

    def retrieve(
        self,
        query: str,
        user_id: str,
        limit: int = 10,
    ):

        query_vector = self.embed(
            query
        )

        return qdrant_service.search(
            query_vector=query_vector,
            user_id=user_id,
            limit=limit,
        )


vector_retriever = (
    VectorRetriever()
)