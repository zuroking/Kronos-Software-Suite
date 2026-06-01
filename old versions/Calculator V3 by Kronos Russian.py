import math

print("=" * 40)
print("   Kronos Calculator V3 by Kronos Russian")
print("   Дата: 28.05.2026")
print("=" * 40)

print("Добро пожаловать в Kronos Calculator V3! Выберите операцию из меню ниже. Введите '0' для выхода.")
print("Этот калькулятор поддерживает базовые операции, степень, корни, логарифмы, тригонометрию и факториал. Наслаждайтесь!")
print("Автор: Kronos Russian — Kronos Calculator V3")

print("\n1. Базовые операции (+, -, *, /)")
print("2. Степень (a^b)")
print("3. Корень (√)")
print("4. Логарифм")
print("5. Тригонометрия (sin, cos, tan)")
print("6. Факториал")
print("0. Выход")

choice = input("\nВыбери операцию: ")

while True:
    try:
        if choice == "1":
            a = float(input("Первое число: "))
            b = float(input("Второе число: "))
            print("Сложение:", a + b)
            print("Вычитание:", a - b)
            print("Умножение:", a * b)
            if b != 0:
                print("Деление:", a / b)
            else:
                print("На ноль делить нельзя!")

        elif choice == "2":
            a = float(input("Основание: "))
            b = float(input("Степень: "))
            print(f"{a}^{b} =", a ** b)

        elif choice == "3":
            a = float(input("Число: "))
            n = float(input("Степень корня (2 = квадратный, 3 = кубический): "))
            if a >= 0:
                print(f"Корень степени {n} из {a} =", a ** (1/n))
            else:
                print("Нельзя взять корень из отрицательного числа!")

        elif choice == "4":
            a = float(input("Число: "))
            print("1. Натуральный логарифм (ln)")
            print("2. Десятичный логарифм (log10)")
            print("3. Логарифм по своему основанию")
            log_choice = input("Выбор: ")
            if log_choice == "1":
                print("ln =", math.log(a))
            elif log_choice == "2":
                print("log10 =", math.log10(a))
            elif log_choice == "3":
                base = float(input("Основание: "))
                print(f"log{base}({a}) =", math.log(a, base))

        elif choice == "5":
            a = float(input("Угол в градусах: "))
            r = math.radians(a)
            print(f"sin({a}°) =", round(math.sin(r), 10))
            print(f"cos({a}°) =", round(math.cos(r), 10))
            print(f"tan({a}°) =", round(math.tan(r), 10))

        elif choice == "6":
            a = int(input("Число: "))
            print(f"{a}! =", math.factorial(a))

        elif choice == "0":
            print("До свидания! — Kronos Calculator V3")
            input("\nНажми Enter для закрытия...")
            break

        else:
            print("Неверный выбор!")

    except ValueError:
        print("Ошибка! Введи число, а не букву.")
    except Exception as e:
        print(f"Ошибка: {e}")

    again = input("\nПосчитать ещё? (да/нет): ")
    if again.lower() != "да":
        print("До свидания! — Kronos Calculator V3")
        input("\nНажми Enter для закрытия...")
        break
    else:
        print("\n1. Базовые операции (+, -, *, /)")
        print("2. Степень (a^b)")
        print("3. Корень (√)")
        print("4. Логарифм")
        print("5. Тригонометрия (sin, cos, tan)")
        print("6. Факториал")
        print("0. Выход")
        choice = input("\nВыбери операцию: ")