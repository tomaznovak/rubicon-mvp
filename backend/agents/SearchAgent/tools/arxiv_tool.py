import arxiv
from pydantic import Field, BaseModel
from agency_swarm import BaseTool
from backend.db import models, database
from sqlalchemy import exists
import requests
from io import BytesIO


class ARXIVTool(BaseTool, BaseModel):

    keyword: str = Field(
        ..., description="Gives information for what is the search keyword."
    )
    
    def run(self):

        client = arxiv.Client()

        db = next(database.get_db())

        search = arxiv.Search(
                query = f"ti:{self.keyword}",
                max_results = 1,
                sort_by = arxiv.SortCriterion.Relevance
                )       

        results = client.results(search)
        all_results = list(results)
        if not all_results:
            return "No results found"
        
        for a in all_results:
            paper_id = a.entry_id.split('/')[-1]
            title = a.title

            if not db.query(exists().where(models.Papers.arxiv_id == paper_id)).scalar():
                pdf_url = a.pdf_url
                response = requests.get(pdf_url, stream=True)
                if response.status_code == 200:
                    pdf_content = BytesIO(response.content).read()

                    new_article = models.Papers(arxiv_id=paper_id, title=title)
                    db.add(new_article)

                    file = models.PDF(
                        name=f"paper-{paper_id}.pdf",
                        title=title,
                        data=pdf_content
                    )
                    db.add(file)
                    db.commit()
                return f"File paper-{paper_id}.pdf was downloaded successfully and uploaded to database. Continue with the next step"
    
        return f"Paper with the title {title} and id {paper_id} was already downloaded."

arxiv_tool = ARXIVTool
