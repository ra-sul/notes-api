from fastapi import APIRouter, Request, Depends, status
from sqlalchemy.orm import Session
from typing import List

from src.app.schemas.notes import NoteResponse, NoteCreate, NotePatch
from src.app.models.users import User
from src.app.dependencies.db import get_db
from src.app.dependencies.users import get_current_user
from src.app.services import notes as notes_services
router = APIRouter(prefix="/notes", tags=["notes"])

@router.get("/", response_model=List[NoteResponse])    
def list_notes(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return notes_services.list_notes(db=db, user_id=current_user.id)

@router.get("/{note_id}", response_model=NoteResponse)
def get_note(note_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return notes_services.get_note(db=db, user_id=current_user.id, note_id=note_id)

@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(note: NoteCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return notes_services.create_note(db=db, user_id=current_user.id, title=note.title, body=note.body)

@router.patch("/{note_id}", response_model=NoteResponse)
def update_note(note_id: int, update_data: NotePatch, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return notes_services.patch_note(db=db, user_id=current_user.id, note_id=note_id, update_data=update_data)

@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    notes_services.delete_note(db=db, user_id=current_user.id, note_id=note_id)