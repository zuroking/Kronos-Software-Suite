import os

print("Блокнот от Kronos Russian")
print("Программа от Kronos Russian для создания заметок на русском языке")
def create_note():
    title = input("Введите название заметки: ")
    content = input("Введите содержание заметки: ")
    filename = f"{title}.txt"
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"Заметка '{title}' сохранена.")
def view_notes():
    notes = [f for f in os.listdir() if f.endswith('.txt')]
    if not notes:
        print("Нет заметок для отображения.")
        return
    print("Ваши заметки:")
    for note in notes:
        print(note)
def read_note():
    title = input("Введите название заметки для чтения: ")
    filename = f"{title}.txt"
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            print(f"\n=== {title} ===")
            print(file.read())
    else:
        print(f"Заметка '{title}' не найдена.")
def delete_note():
    title = input("Введите название заметки для удаления: ")
    filename = f"{title}.txt"
    if os.path.exists(filename):
        os.remove(filename)
        print(f"Заметка '{title}' удалена.")
    else:
        print(f"Заметка '{title}' не найдена.")
while True:
    print("\nВыберите действие:")
    print("1. Создать заметку")
    print("2. Просмотреть заметки")
    print("3. Удалить заметку")
    print("4. Читать заметку")
    print("5. Выйти")
    choice = input("Введите номер действия: ")
    if choice == '1':
        create_note()
    elif choice == '2':
        view_notes()
    elif choice == '3':
        delete_note()
    elif choice == '4':
        read_note()
    elif choice == '5':
        print("Спасибо за использование блокнота от Kronos Russian!")
        print("Надеемся, вам понравилось! До свидания!")
        input("\nНажмите Enter для выхода: ")
        break
    else:
        print("Неверный выбор. Пожалуйста, выберите действие от 1 до 5.")