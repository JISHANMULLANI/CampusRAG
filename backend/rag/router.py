def route_query(
    question: str,
) -> str:

    question_lower = (
        question.lower()
    )

    web_keywords = [

        "latest",
        "current",
        "today",
        "recent",
        "news",

        "latest rule",
        "latest regulation",

        "current regulation",
        "recent update",

        "2026",
    ]

    for keyword in web_keywords:

        if keyword in question_lower:

            return "hybrid"

    return "college"