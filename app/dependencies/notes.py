from fastapi import Depends
from sqlalchemy.orm import Session

from app.repositories.notes import NoteRepository
from app.services.notes import NoteService
from app.dependencies.db import get_db

def get_note_repo(db: Session = Depends(get_db)) -> NoteRepository:
	return NoteRepository(db)


def get_note_service(repo: NoteRepository = Depends(get_note_repo)) -> NoteService:
	return NoteService(repo)