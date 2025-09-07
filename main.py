from database import SessionLocal, init_db
import services


init_db()
db = SessionLocal()

current_user = None
on_procces = True

print("Hi, welcome to the Notes!")

while not current_user:
	print("1. Войти в аккаунт \n2. Зарегистрироваться \n3. Выйти")
	action = input("notes>")

	if action == '1':
		name = input("Введите имя:")
		password = input("Введите пароль:")
		try:
			current_user = services.login_user(db=db, name=name, password=password)
		except ValueError as e:
			print(e)
		print(f"Привет {current_user.name}!")
		print("Введите \"?\", чтобы получить подсказку")

	elif action == '2':
		new_name = input("Введите имя:")
		new_password = input("Введите пароль:")
		in_sure = True
		while in_sure:
			sure = input("Зарегистрироваться? (д/н)>")
			if sure == 'д':
				try:
					services.register_user(db=db, name=new_name, password=new_password)
				except ValueError as e:
					print(e)
				print("Регистрация прошла успешно!")
				in_sure = False
			elif sure == 'н':
				in_sure = False
			else:
				print("Неверный ввод!")

	elif action == '3':
		on_procces = False

	else:
		print("Неверный ввод!")


while on_procces:
	comand = input(f"notes>")

	match comand:
		case "create":
			new_title = input("Заголовок заметки:")
			new_body = input("Тело заметки:")
			services.add_note_for_user(db=db, title=new_title, body=new_body, user_id=current_user)
			print("Заметка добавлена!")
		case "select":
			in_select = True
			id = int(input("Введите номер заметки>"))
			note = services.select_note(db=db, id=id, user_id=current_user.id)
			if note:
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
							services.update_user_note(db=db, note=note, new_title=new_title, new_body=new_body)
							print("Заметка обновлена!")
							in_select = False
						elif sure == 'н':
							pass
					elif cmd == 2:
						sure = input("Удалить заметку? (д/н)>")
						if sure == 'д':
							services.delete_user_note(db=db, note=note)
							print("Заметка удалена!")
							in_select = False
						elif sure == 'н':
							pass
							
					elif cmd == 3:
						in_select = False
					else:
						print("Неверный ввод")
			else:
				print("Заметка не доступна или не существует!")
		case "show_all":
			notes = services.lits_user_notes(db=db, user_id=current_user.id)

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
