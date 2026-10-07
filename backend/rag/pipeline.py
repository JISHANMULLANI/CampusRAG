from rag.router import (
    route_query,
)

from rag.prompt import (
    build_prompt,
)

from rag.citations import (
    create_citations,
)

from retrieval.hybrid_retriever import (
    hybrid_retriever,
)

from services.llm import (
    llm_service,
)


class RAGPipeline:

    def run(
        self,
        question: str,
        user_id: str,
    ):

        route = route_query(
            question
        )

        use_web = (
            route == "hybrid"
        )

        documents = (
            hybrid_retriever.retrieve(

                query=question,

                user_id=user_id,

                use_web=use_web,

                vector_limit=10,

                web_limit=5,

                top_k=5,
            )
        )

        if not documents:

            return {

                "answer": (
                    "I could not find "
                    "relevant information "
                    "in the available sources."
                ),

                "citations": [],

                "route": route,
            }

        prompt = build_prompt(

            question=question,

            documents=documents,
        )

        answer = (
            llm_service.generate(
                prompt
            )
        )

        citations = (
            create_citations(
                documents
            )
        )

        return {

            "answer": answer,

            "citations": citations,

            "route": route,
        }


rag_pipeline = (
    RAGPipeline()
)