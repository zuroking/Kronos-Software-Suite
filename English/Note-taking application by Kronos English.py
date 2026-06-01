import os

print("Note-taking application by Kronos English")
print("A simple note-taking application for creating and managing notes.")
def create_note():
    title = input("Enter the title of the note: ")
    content = input("Enter the content of the note: ")
    filename = f"{title}.txt"
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"Note '{title}' saved.")
def view_notes():
    notes = [f for f in os.listdir() if f.endswith('.txt')]
    if not notes:
        print("No notes to display.")
        return
    print("Your notes:")
    for note in notes:
        print(note)
def read_note():
    title = input("Enter the title of the note to read: ")
    filename = f"{title}.txt"
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            print(f"\n=== {title} ===")
            print(file.read())
    else:
        print(f"Note '{title}' not found.")
def delete_note():
    title = input("Enter the title of the note to delete: ")
    filename = f"{title}.txt"
    if os.path.exists(filename):
        os.remove(filename)
        print(f"Note '{title}' deleted.")
    else:
        print(f"Note '{title}' not found.")
while True:
    print("\nChoose an action:")
    print("1. Create a note")
    print("2. View notes")
    print("3. Delete a note")
    print("4. Read a note")
    print("5. Exit")
    choice = input("Enter the number of the action: ")
    if choice == '1':
        create_note()
    elif choice == '2':
        view_notes()
    elif choice == '3':
        delete_note()
    elif choice == '4':
        read_note()
    elif choice == '5':
        print("Thank you for using the note-taking app by Kronos English!")
        print("We hope you enjoyed it! Goodbye!")
        input("\nPress Enter to exit: ")
        break
    else:
        print("Invalid choice. Please select an action from 1 to 5.")