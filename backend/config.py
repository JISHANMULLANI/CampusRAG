from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # Qdrant
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str | None = None

    # Tavily
    tavily_api_key: str

    # LLM
    groq_api_key: str
    llm_model: str = "openai/gpt-oss-120b"

    # Embedding
    embedding_model: str = (
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    # Reranker
    reranker_model: str = (
        "cross-encoder/ms-marco-MiniLM-L-6-v2"
    )

    # Qdrant collection
    collection_name: str = "college_documents"

    # Upload limits
    max_file_size_mb: int = 20
    max_pages: int = 100

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()