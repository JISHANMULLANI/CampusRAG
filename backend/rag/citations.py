from models.schemas import (
    Citation,
)


def create_citations(
    documents: list[dict],
) -> list[Citation]:

    citations = []

    seen = set()

    for document in documents:

        metadata = document.get(
            "metadata",
            {},
        )

        source_type = metadata.get(
            "source_type",
            "unknown",
        )

        document_name = metadata.get(
            "document_name"
        )

        page_number = metadata.get(
            "page_number"
        )

        url = metadata.get(
            "url"
        )

        chunk_id = metadata.get(
            "chunk_id"
        )

        key = (
            source_type,
            document_name,
            page_number,
            url,
        )

        if key in seen:
            continue

        seen.add(key)

        citations.append(

            Citation(

                source_type=source_type,

                document_name=document_name,

                page_number=page_number,

                url=url,

                chunk_id=chunk_id,
            )
        )

    return citations