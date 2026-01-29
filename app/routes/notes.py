from fastapi import APIRouter, Request, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.notes import NoteResponse, NoteCreate, NotePatch
from app.models.users import User
from app.dependencies.notes import get_note_service
from app.auth.dependencies import get_current_user
from app.services.notes import NoteService
from app.logging_config import logger

router = APIRouter(prefix="/notes", tags=["notes"])

@router.get("/", response_model=List[NoteResponse])    
def list_notes(service: NoteService = Depends(get_note_service), current_user: User = Depends(get_current_user)):
    note_lst = service.list(user_id=current_user.id)
    logger.info("User %s retrieved notes list (count=%s)", current_user.id, len(note_lst))
    return note_lst

@router.get("/{note_id}", response_model=NoteResponse)
def get_note(note_id: int, service: NoteService = Depends(get_note_service),current_user: User = Depends(get_current_user)):
    note = service.get(user_id=current_user.id, note_id=note_id)
    logger.info("User %s retrieved note %s", current_user.id, note_id)
    return note

@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(note: NoteCreate, service: NoteService = Depends(get_note_service), current_user: User = Depends(get_current_user)):
    note = service.create(user_id=current_user.id, title=note.title, body=note.body)
    logger.info("User %s created note %s", current_user.id, note.id)
    return note

@router.patch("/{note_id}", response_model=NoteResponse)
def patch_note(note_id: int, update_data: NotePatch, service: NoteService = Depends(get_note_service), current_user: User = Depends(get_current_user)):
    note = service.patch(user_id=current_user.id, note_id=note_id, update_data=update_data)
    logger.info("User %s patched note %s", current_user.id, note_id)
    return note

@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int, service: NoteService = Depends(get_note_service), current_user: User = Depends(get_current_user)):
    service.delete(user_id=current_user.id, note_id=note_id)
    logger.info("User %s deleted note %s", current_user.id, note_id)