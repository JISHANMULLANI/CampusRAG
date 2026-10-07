from retrieval.vector_retriever import (
    vector_retriever,
)

from retrieval.web_retriever import (
    web_retriever,
)

from retrieval.reranker import (
    reranker,
)


class HybridRetriever:

    def retrieve(
        self,
        query: str,
        user_id: str,
        use_web: bool = False,
        vector_limit: int = 10,
        web_limit: int = 5,
        top_k: int = 5,
    ):

        documents = []

        # -----------------------------
        # College / user documents
        # -----------------------------

        vector_results = (
            vector_retriever.retrieve(

                query=query,

                user_id=user_id,

                limit=vector_limit,
            )
        )

        for result in vector_results:

            payload = (
                result.payload or {}
            )

            text = payload.get(
                "text",
                "",
            )

            if not text.strip():
                continue

            documents.append(
                {
                    "text": text,

                    "metadata": payload,
                }
            )

        # -----------------------------
        # Web documents
        # -----------------------------

        if use_web:

            web_results = (
                web_retriever.retrieve(
                    query=query,
                    limit=web_limit,
                )
            )

            documents.extend(
                web_results
            )

        # -----------------------------
        # Reranking
        # -----------------------------

        return reranker.rerank(

            query=query,

            documents=documents,

            top_k=top_k,
        )


hybrid_retriever = (
    HybridRetriever()
)