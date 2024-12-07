from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class Prompt(BaseModel):
    prompt: str


class Response(BaseModel):
    response: str

class FileResponse(BaseModel):
    id: int
    name: str
    type: str
    title: str

    class Config:
        from_attributes = True

class FileInfo(BaseModel):
    id: int
    name: str
    type: str
    size: str
    url: str