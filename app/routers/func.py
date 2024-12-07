from fastapi import HTTPException, status, Depends, Request, APIRouter
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from backend.db import models
from backend.db.database import get_db
from sqlalchemy.orm import Session
import os
import tempfile

router = APIRouter(
    prefix='/agent',
    tags=['Agent']
)

templates = Jinja2Templates(directory="frontend")

@router.get('', response_class=HTMLResponse)
async def frontend(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get('/settings')
def settings():
    return {"response": "In development"}

@router.get('/about')
def about():
    return {"response": "In development"}


@router.get('/download/pdf/{pdf_id}')
async def dow_pdf(pdf_id: int, db: Session = Depends(get_db)):
    try:
        file_record = db.query(models.PDF).filter(models.PDF.id == pdf_id).first()

        if not file_record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="PDF file not found",
            )
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(file_record.data)
            tmp_path = tmp_file.name

        def cleanup_temp_file():
            try:
                os.unlink(tmp_path)
            except:
                pass

        return FileResponse(
            path=tmp_path,
            media_type='application/pdf',
            filename=file_record.name,
            background=cleanup_temp_file
            )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get('/download/md/{md_id}')
async def dow_md(md_id: int, db: Session = Depends(get_db)):
    try:
        file_record = db.query(models.MD).filter(models.MD.id == md_id).first()

        if not file_record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Markdown file not found"
            )
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.md') as tmp_file:
            tmp_file.write(file_record.data)
            tmp_path = tmp_file.name
        
        def cleanup_temp_file():
            try:
                os.unlink(tmp_file)
            except:
                pass

        return FileResponse(
            path=tmp_path,
            media_type='text/markdown',
            filename=file_record.name,
            background=cleanup_temp_file
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
