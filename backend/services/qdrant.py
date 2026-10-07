from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
)

from config import settings


class QdrantService:

    def __init__(self):

        if settings.qdrant_api_key:

            self.client = QdrantClient(
                url=settings.qdrant_url,
                api_key=settings.qdrant_api_key,
            )

        else:

            self.client = QdrantClient(
                url=settings.qdrant_url
            )

    def collection_exists(self) -> bool:

        collections = (
            self.client.get_collections()
        )

        names = {
            collection.name
            for collection in collections.collections
        }

        return (
            settings.collection_name
            in names
        )

    def create_collection(
        self,
        vector_size: int,
    ):

        if self.collection_exists():
            return

        self.client.create_collection(

            collection_name=(
                settings.collection_name
            ),

            vectors_config=VectorParams(

                size=vector_size,

                distance=Distance.COSINE,
            ),
        )

    def upsert(
        self,
        points: list[PointStruct],
    ):

        if not points:
            return

        self.client.upsert(

            collection_name=(
                settings.collection_name
            ),

            points=points,
        )

    def search(
        self,
        query_vector: list[float],
        user_id: str,
        limit: int = 10,
    ):

        # User can access:
        #
        # 1. Their own uploaded documents
        # 2. Public college documents
        #
        query_filter = Filter(

            should=[

                FieldCondition(
                    key="user_id",
                    match=MatchValue(
                        value=user_id
                    ),
                ),

                FieldCondition(
                    key="user_id",
                    match=MatchValue(
                        value="public"
                    ),
                ),
            ]
        )

        result = self.client.query_points(

            collection_name=(
                settings.collection_name
            ),

            query=query_vector,

            query_filter=query_filter,

            limit=limit,

            with_payload=True,
        )

        return result.points

    def delete_document(
        self,
        document_id: str,
        user_id: str,
    ):

        document_filter = Filter(

            must=[

                FieldCondition(
                    key="document_id",
                    match=MatchValue(
                        value=document_id
                    ),
                ),

                FieldCondition(
                    key="user_id",
                    match=MatchValue(
                        value=user_id
                    ),
                ),
            ]
        )

        self.client.delete(

            collection_name=(
                settings.collection_name
            ),

            points_selector=document_filter,
        )


qdrant_service = QdrantService()