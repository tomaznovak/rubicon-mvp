from fastapi import FastAPI, HTTPException, status, Depends, Request
from fastapi.templating import Jinja2Templates
from typing import Dict, List
from backend import swarm
from app import schemas
from backend.db import database, models
from backend.db.database import get_db
from sqlalchemy.orm import Session
from app.routers import func
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

origins = [
    "https://www.google.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(func.router)

templates = Jinja2Templates(directory="frontend")

@app.get('/', status_code=status.HTTP_200_OK)
async def root():
    return {"response": "OK"}

@app.post('/run/',status_code=status.HTTP_200_OK, response_model=schemas.Response)
async def run(prompt: schemas.Prompt, db: Session = Depends(get_db)) -> Dict:
    try:
        response = swarm.agency.get_completion(prompt.prompt)
        return {'response': response}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.get('/api/files', response_model=List[schemas.FileInfo])
async def api(request: Request, db: Session = Depends(get_db)):
    try:
        pdf_files = db.query(models.PDF).all()
        md_files = db.query(models.MD).all()

        base_url = str(request.base_url).rstrip('/').replace('http://', '').replace('https://', '')
        files = []
        for p in pdf_files:
            files.append(schemas.FileInfo(
                id=p.id,
                name=p.name,
                type="pdf",
                size=f"{len(p.data) / 1024:.2f}KB",
                url=f"https://{base_url}/agent/download/pdf/{p.id}"
            ))

        for m in md_files:
            files.append(schemas.FileInfo(
                id=m.id,
                name=m.name,
                type="md",
                size=f"{len(m.data) / 1024:.2f}KB",
                url=f"https://{base_url}/agent/download/md/{m.id}"
            ))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return files


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080
    )