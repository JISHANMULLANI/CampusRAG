def normalize_web_result(
    result: dict,
) -> dict:

    return {

        "text": result.get(
            "content",
            "",
        ),

        "metadata": {

            "source_type": "web",

            "document_name": result.get(
                "title",
                "Web source",
            ),

            "url": result.get(
                "url"
            ),
        },
    }