import re


def clean_text(text: str) -> str:

    text = text.replace(
        "\x00",
        " ",
    )

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()


def chunk_text(
    text: str,
    chunk_size: int = 1200,
    overlap: int = 200,
) -> list[str]:

    text = clean_text(text)

    if not text:
        return []

    paragraphs = re.split(
        r"\n\s*\n",
        text,
    )

    chunks = []

    current = ""

    for paragraph in paragraphs:

        paragraph = paragraph.strip()

        if not paragraph:
            continue

        if len(current) + len(
            paragraph
        ) <= chunk_size:

            current += (
                "\n\n" + paragraph
            )

        else:

            if current.strip():

                chunks.append(
                    current.strip()
                )

            overlap_text = (
                current[-overlap:]
                if len(current) > overlap
                else current
            )

            current = (
                overlap_text
                + "\n\n"
                + paragraph
            )

    if current.strip():
        chunks.append(
            current.strip()
        )

    return chunks