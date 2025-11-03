from typing import List

from src.app.models.notes import Note
from src.app.repositories.notes import NoteRepository
from src.app.schemas.notes import NotePatch
from src.app.exceptions.notes import NoteNotFoundError, NoteAccessDeniedError

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

	def update(self, user_id: int, note_id: int, new_title: str, new_body: str) -> Note:
		note = self.get(user_id, note_id)
		updated_note = self.repo.update(note, new_title, new_body)
		self.repo.db.commit()
		self.repo.db.refresh(updated_note)
		return updated_note

	def delete(self, user_id: int, note_id: int) -> None:
		note = self.get(user_id, note_id)
		self.repo.delete(note)
		self.repo.db.commit()

	def list(self, user_id: int) -> List[Note]:
		return self.repo.list(user_id)

	def patch(self, user_id: int, note_id: int, update_data: NotePatch) -> Note:
		note = self.get(user_id, note_id)
		patched_note = self.repo.patch(note, update_data)
		self.repo.db.commit()
		self.repo.db.refresh(patched_note)
		return patched_note