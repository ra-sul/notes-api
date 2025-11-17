from src.app.models.notes import Note

def test_create(notes_repo, user):
	note = Note(title="Test title", body="Test body", user_id=user.id)

	notes_repo.create(note)
	notes_repo.db.commit()
	notes_repo.db.refresh(note)

	assert note.id is not None
	assert note.title == "Test title"
	assert note.body == "Test body"
	assert note.user_id == user.id


def test_get(notes_repo, note):
	received_note = notes_repo.get(note.id)

	assert received_note is not None
	assert received_note.title == "Test title"
	assert received_note.body == "Test body"
	assert received_note.user_id == note.user_id

def test_list(notes_repo, user):
	first_note = Note(title="Test title 1", body="Test body 1", user_id=user.id)
	second_note = Note(title="Test title 2", body="Test body 2", user_id=user.id)
	notes_repo.db.add(first_note)
	notes_repo.db.add(second_note)
	notes_repo.db.commit()
	notes_repo.db.refresh(first_note)
	notes_repo.db.refresh(second_note)

	notes_list = notes_repo.list(user.id)

	assert notes_list is not None
	assert len(notes_list) == 2
	assert notes_list[0].id == first_note.id
	assert notes_list[0].title == "Test title 1"
	assert notes_list[0].body == "Test body 1"
	assert notes_list[1].id == second_note.id
	assert notes_list[1].title == "Test title 2"
	assert notes_list[1].body == "Test body 2"


def test_update(notes_repo, note):
	data = {"title": "Updated title", "body": "Updated body"}

	updated_note = notes_repo.update(note, data)

	assert updated_note is not None
	assert updated_note.id == note.id
	assert updated_note.user_id == note.user_id
	assert updated_note.title == "Updated title"
	assert updated_note.body == "Updated body"


def test_delete(notes_repo, note):
	notes_repo.delete(note)
	notes_repo.db.commit()

	deleted_note = notes_repo.db.query(Note).filter(Note.id == note.id).first()

	assert deleted_note is None