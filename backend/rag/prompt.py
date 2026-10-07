SYSTEM_PROMPT = """
You are a College Knowledge Assistant.

Your job is to answer student questions using
the retrieved context.

STRICT RULES:

1. Use only information supported by the context.
2. Never invent facts.
3. If the retrieved context does not contain enough
   information, say that sufficient information was
   not found.
4. Prefer official college documents for college-specific
   questions.
5. Web sources may contain current information.
6. Clearly distinguish official college information
   from web information when both are used.
7. Give concise and student-friendly answers.
8. Do not mention internal implementation details.
"""


def build_prompt(
    question: str,
    documents: list[dict],
) -> str:

    context_parts = []

    for index, document in enumerate(
        documents,
        start=1,
    ):

        metadata = document.get(
            "metadata",
            {},
        )

        source_type = metadata.get(
            "source_type",
            "unknown",
        )

        document_name = metadata.get(
            "document_name",
            "Unknown source",
        )

        page_number = metadata.get(
            "page_number"
        )

        url = metadata.get(
            "url"
        )

        source = (
            f"[Source {index}] "
            f"{source_type} - "
            f"{document_name}"
        )

        if page_number:
            source += (
                f", page {page_number}"
            )

        if url:
            source += (
                f", URL: {url}"
            )

        context_parts.append(
            f"{source}\n"
            f"{document['text']}"
        )

    context = "\n\n".join(
        context_parts
    )

    return f"""
{SYSTEM_PROMPT}

====================
RETRIEVED CONTEXT
====================

{context}

====================
STUDENT QUESTION
====================

{question}

====================
ANSWER
====================
"""