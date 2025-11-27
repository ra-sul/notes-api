from typing import List

from app.models.notes import Note
from app.repositories.notes import NoteRepository
from app.schemas.notes import NotePatch, NoteUpdate
from app.exceptions.notes import NoteNotFoundError, NoteAccessDeniedError

class NoteService:
	def __init__(self, repo: NoteRepository):
		self.repo = repo

	def create(self, user_id: int, title: str, body: str) -> Note:
		new_note = Note(title=title, body=body, user_id=user_id)
		self.repo.create(new_note)
		self.repo.db.commit()
		self.repo.db.refresh(new_note)
		return new_note

	def get(self, user_id: int, note_id: int) -> Note:
		note = self.repo.get(note_id)
		if not note:
			raise NoteNotFoundError()
		if note.user_id != user_id:
			raise NoteAccessDeniedError()
		return note

	def list(self, user_id: int) -> List[Note]:
		return self.repo.list(user_id)

	def update(self, user_id: int, note_id: int, update_data: NoteUpdate) -> Note:
		note = self.get(user_id, note_id)
		data = update_data.model_dump()
		updated_note = self.repo.update(note, data)
		
		self.repo.db.commit()
		self.repo.db.refresh(updated_note)
		return updated_note


	def patch(self, user_id: int, note_id: int, update_data: NotePatch) -> Note:
		note = self.get(user_id, note_id)
		data = update_data.model_dump(exclude_unset=True)
		patched_note = self.repo.update(note, data)

		self.repo.db.commit()
		self.repo.db.refresh(patched_note)
		return patched_note

	def delete(self, user_id: int, note_id: int) -> None:
		note = self.get(user_id, note_id)
		self.repo.delete(note)
		self.repo.db.commit()
