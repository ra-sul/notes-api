from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine("sqlite:///./test.db")

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

class Note(Base):
	__tablename__ = "notes"
	id = Column(Integer, primary_key=True, index=True)
	title = Column(String, index=True)
	body = Column(String)


Base.metadata.create_all(engine)

db = SessionLocal()

on_procces = True


print("Hi, welcome to the Notes!")
print("Введите \"?\", чтобы получить подсказку")
while on_procces:
	comand = input("notes>")

	match comand:
		case "create":
			new_title = input("Заголовок заметки:")
			new_body = input("Тело заметки:")
			new_note = Note(title=new_title, body=new_body)
			db.add(new_note)
			db.commit()
			print("Заметка добавлена!")
		case "select":
			in_select = True
			id = int(input("Введите номер заметки>"))
			note = db.query(Note).filter(Note.id == id).first()

			while in_select:
				print("\n---------",note.title, "---------")
				print(note.body,'\n')
				print("Выберите действие:")
				print("1. Обновить заметку \n2. Удалить заметку \n3. Отмена")
				cmd = int(input(f"{note.title}>"))

				if cmd == 1:
					new_title = input("Заголовок заметки:")
					new_body = input("Тело заметки:")
					sure = input("Обновить заметку? (д/н)>")
					if sure == 'д':
						note.title = new_title
						note.body = new_body
						db.commit()
						print("Заметка обновлена!")
						in_select = False
					elif sure == 'н':
						pass
				elif cmd == 2:
					sure = input("Удалить заметку? (д/н)>")
					if sure == 'д':
						db.delete(note)
						db.commit()
						print("Заметка удалена!")
						in_select = False
					elif sure == 'н':
						pass
						
				elif cmd == 3:
					in_select = False
				else:
					print("Неверный ввод")
		case "show_all":
			notes = db.query(Note).all()

			print("---------------------------------")
			for note in notes:
				print(f"{note.id}. {note.title}")
			print("---------------------------------")
		case "exit":
			on_procces = False
		case '?':
			print("create - Создать заметку \nselect - Выбор заметки \nshow_all - Показать все заметки \nexit - Выйти")
		case _:
			print("Неверная команда, введите \"?\", чтобы получить подсказку")

print("Bye")
