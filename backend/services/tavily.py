from tavily import TavilyClient

from config import settings


class TavilyService:

    def __init__(self):

        self.client = TavilyClient(
            api_key=(
                settings.tavily_api_key
            )
        )

    def search(
        self,
        query: str,
        max_results: int = 5,
    ):

        response = self.client.search(

            query=query,

            search_depth="advanced",

            max_results=max_results,

            include_answer=False,
        )

        return response.get(
            "results",
            [],
        )


tavily_service = (
    TavilyService()
)