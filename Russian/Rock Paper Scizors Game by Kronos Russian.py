print("Камень, Ножницы, Бумага. ")
print("Игра от Kronos Russian")
import random
while True:
    user_input = input("Выберите камень, ножницы или бумагу (или 'выход' для завершения): ").lower()
    if user_input == 'выход':
        print("Спасибо за игру!")
        break
    elif user_input not in ['камень', 'ножницы', 'бумага']:
        print("Неверный ввод. Пожалуйста, выберите камень, ножницы или бумагу.")
        continue

    options = ['камень', 'ножницы', 'бумага']
    computer_choice = random.choice(options)
    print(f"Компьютер выбрал: {computer_choice}")

    if user_input == computer_choice:
        print("Ничья!")
    elif (user_input == 'камень' and computer_choice == 'ножницы') or (user_input == 'ножницы' and computer_choice == 'бумага') or (user_input == 'бумага' and computer_choice == 'камень'):
        print("Вы выиграли!")
    else:
        print("Вы проиграли!")