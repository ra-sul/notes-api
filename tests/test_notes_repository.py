from src.app.models.notes import Note

def test_create(repo):
	note = Note(title="Test title", body="Test body", user_id=1)
	repo.create(note)
	repo.db.commit()
	repo.db.refresh(note)

	assert note.id is not None