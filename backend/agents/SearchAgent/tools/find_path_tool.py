import os
from agency_swarm import BaseTool
from pydantic import BaseModel, Field

class FilePathFinder(BaseTool, BaseModel):

    file_name: str = Field(
        ..., description="The name of the file."
    )

    def run(self):
        current_dir =os.path.dirname(self.file_name)
        file_path = os.path.join(current_dir, 'backend/pdfs', self.file_name)
        abs_path = os.path.abspath(file_path)
        return f"This is the file path: r'{abs_path}."

find_path_tool = FilePathFinder