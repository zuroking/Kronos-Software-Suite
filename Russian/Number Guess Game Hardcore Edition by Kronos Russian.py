import random
import time

def main():
    print("=" * 50)
    print("   Игра: Угадай Число от Kronos Russian")
    print("   Число от 1 до 1,000,000. Удачи...")
    print("=" * 50)

    while True:
        number = random.randint(1, 1_000_000)
        attempts = 0
        start_time = time.time()

        print("\nЯ загадал число от 1 до 1,000,000!")
        print("Угадай его!\n")

        while True:
            try:
                guess = int(input("Твоя попытка: "))
                attempts += 1

                if guess < 1 or guess > 1_000_000:
                    print("Число должно быть от 1 до 1,000,000!")
                    continue

                if guess < number:
                    diff = number - guess
                    if diff > 100_000:
                        print("Намного больше!")
                    elif diff > 10_000:
                        print("Больше!")
                    elif diff > 1_000:
                        print("Чуть больше!")
                    else:
                        print("Совсем чуть-чуть больше!")

                elif guess > number:
                    diff = guess - number
                    if diff > 100_000:
                        print(" Намного меньше!")
                    elif diff > 10_000:
                        print("Меньше!")
                    elif diff > 1_000:
                        print("Чуть меньше!")
                    else:
                        print("Совсем чуть-чуть меньше!")

                else:
                    end_time = time.time()
                    elapsed = round(end_time - start_time, 2)
                    print(f"\nУГАДАЛ за {attempts} попыток и {elapsed} секунд!")
                    if attempts <= 20:
                        print("Легенда!")
                    elif attempts <= 40:
                        print("Неплохо!")
                    else:
                        print("Тренируйся ещё!")
                    break

            except ValueError:
                print("Введи целое число!")

        again = input("\nСыграть ещё? (да/нет): ")
        if again.lower() != "да":
            print("\nДо свидания! — Hardcore Guess by Kronos Russian")
            input("\nНажми Enter для закрытия...")
            break

main()