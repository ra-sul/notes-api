from src.app.models.users import User

def test_create(users_repo):
    user = User(name="User", password="password")

    users_repo.create(user)
    users_repo.db.commit()
    users_repo.db.refresh(user)

    assert user.id is not None
    assert user.name == "User"
    assert user.password == "password"

def test_get(users_repo, user):
    received_user = users_repo.get(name=user.name, password=user.password)

    assert received_user.id is not None
    assert received_user.name == user.name
    assert received_user.password == user.password

def test_get_by_name(users_repo, user):
    received_user = users_repo.get_by_name(name=user.name)

    assert received_user.id is not None
    assert received_user.name == user.name
    assert received_user.password == user.password