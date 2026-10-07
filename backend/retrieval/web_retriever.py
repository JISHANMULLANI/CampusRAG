from services.tavily import (
    tavily_service,
)

from ingestion.web_loader import (
    normalize_web_result,
)


class WebRetriever:

    def retrieve(
        self,
        query: str,
        limit: int = 5,
    ):

        results = (
            tavily_service.search(
                query=query,
                max_results=limit,
            )
        )

        documents = []

        for result in results:

            document = (
                normalize_web_result(
                    result
                )
            )

            if document["text"].strip():

                documents.append(
                    document
                )

        return documents


web_retriever = (
    WebRetriever()
)