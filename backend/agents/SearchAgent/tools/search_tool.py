from agency_swarm.tools import BaseTool
from pydantic import Field, BaseModel
import arxiv

class Search_Tool(BaseTool, BaseModel):

    keyword: str = Field(
        ..., description="The term to be searched for."
    )

    def run(self):
        client = arxiv.Client()
        search = arxiv.Search(
            query = self.keyword,
            max_results = 10,
            sort_by = arxiv.SortCriterion.SubmittedDate
            )

        results = client.results(search)

        return [r.title for r in client.results(search)]


search_tool = Search_Tool


