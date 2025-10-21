from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from typing import List

from src.app.schemas.notes import Note as NoteResponse, NoteCreate, NotePatch
from src.app.models.users import User
from src.app.dependencies.db import get_db
from src.app.dependencies.users import get_current_user
from src.app.services import notes
router = APIRouter(prefix="/notes", tags=["notes"])

@router.get("/", response_model=List[NoteResponse])    
def show_all_notes(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return notes.list_user_notes(db=db, user_id=current_user.id)

@router.get("/{note_id}", response_model=NoteResponse)
def show_user_note(note_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return notes.select_note(note_id=note_id, db=db, user_id=current_user.id)

@router.post("/", response_model=NoteResponse)
def create_user_note(note: NoteCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return notes.add_note_for_user(db=db, title=note.title, body=note.body,  user_id=current_user.id)

@router.patch("/{note_id}", response_model=NoteResponse)
def update_user_note(note_id: int, update_data: NotePatch, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return notes.patch_user_note(db=db, note_id=note_id, user_id=current_user.id, update_data=update_data)

@router.delete("/{note_id}")
def delete_user_note(note_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    notes.delete_user_note(db=db, note_id=note_id, user_id=current_user.id)
    return {"message": "Note deleted successfully"}