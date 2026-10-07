from fastapi import (
    APIRouter,
)

from models.schemas import (
    ChatRequest,
    ChatResponse,
)

from rag.pipeline import (
    rag_pipeline,
)


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "",
    response_model=ChatResponse,
)
def chat(
    request: ChatRequest,
):

    result = (
        rag_pipeline.run(

            question=request.question,

            user_id=request.user_id,
        )
    )

    return ChatResponse(

        answer=result["answer"],

        citations=result[
            "citations"
        ],

        route=result["route"],
    )