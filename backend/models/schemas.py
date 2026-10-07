from pydantic import BaseModel, Field


class ChatRequest(BaseModel):

    question: str = Field(
        ...,
        min_length=1,
        max_length=2000,
    )

    user_id: str = Field(
        default="anonymous",
        min_length=1,
        max_length=100,
    )


class Citation(BaseModel):

    source_type: str

    document_name: str | None = None

    page_number: int | None = None

    url: str | None = None

    chunk_id: str | None = None


class ChatResponse(BaseModel):

    answer: str

    citations: list[Citation]

    route: str


class UploadResponse(BaseModel):

    document_id: str

    filename: str

    chunks_created: int

    user_id: str

    message: str


class HealthResponse(BaseModel):

    status: str