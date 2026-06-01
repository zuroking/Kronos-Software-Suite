import random

number = random.randint(1, 100)
print("Игра от Kronos Russian.")
print("Игра: Угадайте число от 1 до 100!")
print("У вас есть неограниченное количество попыток. Удачи!")

while True:
    attempt = int(input("Введите число: "))
    if attempt < number:
        print("Слишком мало! Попробуйте снова.")
    elif attempt > number:
        print("Слишком много! Попробуйте снова.")
    else:
        print("Поздравляем! Вы угадали число!")
        input("\nНажмите Enter для закрытия...")
        break