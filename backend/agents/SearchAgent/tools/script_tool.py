from agency_swarm.tools import BaseTool
import pdfplumber
from openai import OpenAI
from markd import Markdown
from pydantic import BaseModel, Field
from backend.db import models, database
from io import BytesIO

class Script_Tool(BaseTool, BaseModel):

    title: str = Field(
        ..., description="Title of the research paper"
    )
    id: str = Field(
        ..., description="ARXIV id of the given file."
    )


    def run(self):

        db = next(database.get_db())

        pdf_record = db.query(models.PDF).filter(
            models.PDF.name == f"paper-{self.id}.pdf"
        ).first()

        if not pdf_record:
            return "PDF not found in database"
        pdf_binary = BytesIO(pdf_record.data)
        with pdfplumber.open(pdf_binary) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()

        text.split(maxsplit=10)
        client = OpenAI()

        completion = client.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system",
                "content": """
                You are an expert in extracting valuable information from the text chunks and making them into a well rounded text.
                Always list the authors and the title of the research paper first before you procced.
                Format the output text into markdown file.
                """},
                {
                    "role": "user",
                    "content": f"extract the meaningfull and important facts from this text: {text}"
                }
            ]
        )
        response = completion.choices[0].message.content

        markdown_data = response.encode('utf-8')
        new_file = models.MD(
            name=f'script-{self.id}.md',
            title=self.title,
            data=markdown_data
        )
        db.add(new_file)
        db.commit()
        
        return f"Script for {self.title} has been generated and stored in the database"


script_tool = Script_Tool
