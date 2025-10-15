from fastapi  import  FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware
from fastapi import Request

from src.app.scemas.scemas import Note, Login
from src.app.models.models import User
from src.app.database import SessionLocal, init_db
from src.app.services import users, notes

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="very_secret_key")

init_db()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close

def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    user = db.query(User).get(user_id)

    if not user:
        request.session.clear()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    return user


@app.post("/login")
def login(request: Request, login: Login, db: Session = Depends(get_db)):
    current_user = users.login_user(db=db, name=login.name, password=login.password)
    request.session["user_id"] = current_user.id

    return {"message": f"Привет, {current_user.name}!"}

@app.post("/logout")
def logout(request: Request):
    request.session.clear()
    return {"message": "Logget out successfully"}

@app.get("/notes", response_model=list[Note])    
def show_all_notes(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return notes.list_user_notes(db=db, user_id=current_user.id)
