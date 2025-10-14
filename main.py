from fastapi  import  FastAPI, Depends
from sqlalchemy.orm import Session
from scemas import Note
from database import SessionLocal, init_db
import services

app = FastAPI()

init_db()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close

@app.get("/notes/{user_id}", response_model=list[Note])    
def show_all_notes(user_id, db: Session = Depends(get_db)):
    return services.list_user_notes(db=db, user_id=user_id)

