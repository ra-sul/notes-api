from fastapi import APIRouter, Request, Depends, status
from sqlalchemy.orm import Session
from typing import List

from src.app.schemas.notes import NoteResponse, NoteCreate, NotePatch
from src.app.models.users import User
from src.app.dependencies.notes import get_note_service
from src.app.dependencies.users import get_current_user
from src.app.services.notes import NoteService
router = APIRouter(prefix="/notes", tags=["notes"])

@router.get("/", response_model=List[NoteResponse])    
def list_notes(service: NoteService = Depends(get_note_service), current_user: User = Depends(get_current_user)):
    return service.list(user_id=current_user.id)

@router.get("/{note_id}", response_model=NoteResponse)
def get_note(note_id: int, service: NoteService = Depends(get_note_service),current_user: User = Depends(get_current_user)):
    return service.get(user_id=current_user.id, note_id=note_id)

@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(note: NoteCreate, service: NoteService = Depends(get_note_service), current_user: User = Depends(get_current_user)):
    return service.create(user_id=current_user.id, title=note.title, body=note.body)

@router.patch("/{note_id}", response_model=NoteResponse)
def patch_note(note_id: int, update_data: NotePatch, service: NoteService = Depends(get_note_service), current_user: User = Depends(get_current_user)):
    return service.patch(user_id=current_user.id, note_id=note_id, update_data=update_data)

@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int, service: NoteService = Depends(get_note_service), current_user: User = Depends(get_current_user)):
    service.delete(user_id=current_user.id, note_id=note_id)