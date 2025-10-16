from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from typing import List

from src.app.schemas.notes import Note as NoteResponse
from src.app.models.users import User
from src.app.dependencies.db import get_db
from src.app.dependencies.users import get_current_user
from src.app.services import notes
router = APIRouter(prefix="/notes", tags=["notes"])

@router.get("/", response_model=List[NoteResponse])    
def show_all_notes(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return notes.list_user_notes(db=db, user_id=current_user.id)
