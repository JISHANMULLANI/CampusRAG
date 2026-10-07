import fitz


def extract_pdf_pages(
    file_path: str,
) -> list[dict]:

    document = fitz.open(file_path)

    pages = []

    try:

        for page_number, page in enumerate(
            document,
            start=1,
        ):

            text = page.get_text(
                "text"
            )

            if text and text.strip():

                pages.append(
                    {
                        "page_number": page_number,
                        "text": text.strip(),
                    }
                )

    finally:

        document.close()

    return pages


def get_pdf_page_count(
    file_path: str,
) -> int:

    document = fitz.open(file_path)

    try:
        return len(document)

    finally:
        document.close()