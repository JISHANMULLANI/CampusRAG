from datetime import datetime, timezone


def create_metadata(
    document_id: str,
    document_name: str,
    page_number: int,
    chunk_id: str,
    user_id: str,
) -> dict:

    source_type = (
        "college"
        if user_id == "public"
        else "user_upload"
    )

    return {

        "document_id": document_id,

        "document_name": document_name,

        "page_number": page_number,

        "chunk_id": chunk_id,

        "user_id": user_id,

        "source_type": source_type,

        "created_at": (
            datetime.now(
                timezone.utc
            ).isoformat()
        ),
    }