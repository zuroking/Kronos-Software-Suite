import math
import cmath
import random
import matplotlib.pyplot as plt

history = []

print("=" * 40)
print("   Kronos Calculator V5 by Kronos Russian")
print("   Научно-инженерный калькулятор — всё в одном")
print("   Дата: 02.06.2026")
print("=" * 40)


def save_history(text):
    history.append(text)

    with open("history.txt", "a", encoding="utf-8") as file:
        file.write(text + "\n")


def show_history():
    print("\n--- ИСТОРИЯ ВЫЧИСЛЕНИЙ ---")

    if not history:
        print("История пуста.")
        return

    for item in history:
        print(item)


def show_menu():
    print("\n--- БАЗОВЫЕ ---")
    print("1. Сложение, вычитание, умножение, деление")
    print("2. Степень (a^b)")
    print("3. Корень")

    print("--- НАУЧНЫЕ ---")
    print("4. Логарифм")
    print("5. Тригонометрия (sin, cos, tan)")
    print("6. Факториал")

    print("--- ПРОДВИНУТЫЕ ---")
    print("7. Квадратное уравнение (ax²+bx+c=0)")
    print("8. Комплексные числа")
    print("9. Матрицы (2x2)")
    print("10. Градусы ↔ Радианы")

    print("--- РАСШИРЕННЫЕ ФУНКЦИИ ---")
    print("11. Проценты")
    print("12. Простое число / НОД / НОК")
    print("13. История вычислений")
    print("14. Парсер выражений")
    print("15. Построение графика")
    print("0. Выход")


def basic_operations():
    a = float(input("Первое число: "))
    b = float(input("Второе число: "))

    add = a + b
    sub = a - b
    mul = a * b

    print("Сложение:", round(add, 4))
    print("Вычитание:", round(sub, 4))
    print("Умножение:", round(mul, 4))

    save_history(f"{a} + {b} = {add}")
    save_history(f"{a} - {b} = {sub}")
    save_history(f"{a} * {b} = {mul}")

    if b != 0:
        div = a / b
        mod = a % b

        print("Деление:", round(div, 4))
        print("Остаток:", round(mod, 4))

        save_history(f"{a} / {b} = {div}")
        save_history(f"{a} % {b} = {mod}")

    else:
        print("На ноль делить нельзя!")


def power_operation():
    a = float(input("Основание: "))
    b = float(input("Степень: "))

    result = a ** b

    print(f"{a}^{b} =", round(result, 4))

    save_history(f"{a}^{b} = {result}")


def root_operation():
    a = float(input("Число: "))
    n = float(input("Степень корня (2 = квадратный, 3 = кубический): "))

    if n == 0:
        print("Степень корня не может быть 0!")
        return

    if a >= 0:
        result = a ** (1 / n)

        print(f"Корень степени {n} из {a} =", round(result, 4))

        save_history(f"Корень степени {n} из {a} = {result}")

    else:
        print("Нельзя взять корень из отрицательного числа!")


def logarithm_operation():
    a = float(input("Число: "))

    if a <= 0:
        print("Логарифм определён только для положительных чисел")
        return

    print("1. Натуральный (ln)")
    print("2. Десятичный (log10)")
    print("3. По своему основанию")

    log_choice = input("Выбор: ")

    if log_choice == "1":
        result = math.log(a)

        print("ln =", round(result, 6))

        save_history(f"ln({a}) = {result}")

    elif log_choice == "2":
        result = math.log10(a)

        print("log10 =", round(result, 6))

        save_history(f"log10({a}) = {result}")

    elif log_choice == "3":
        base = float(input("Основание: "))

        if base <= 0 or base == 1:
            print("Некорректное основание логарифма!")
        else:
            result = math.log(a, base)

            print(f"log{base}({a}) =", round(result, 6))

            save_history(f"log{base}({a}) = {result}")


def trigonometry_operation():
    a = float(input("Угол в градусах: "))

    r = math.radians(a)

    sin_value = round(math.sin(r), 10)
    cos_value = round(math.cos(r), 10)
    tan_value = round(math.tan(r), 10)

    print(f"sin({a}°) =", sin_value)
    print(f"cos({a}°) =", cos_value)
    print(f"tan({a}°) =", tan_value)

    save_history(f"sin({a}) = {sin_value}")
    save_history(f"cos({a}) = {cos_value}")
    save_history(f"tan({a}) = {tan_value}")


def factorial_operation():
    a = int(input("Число: "))

    if a < 0:
        print("Факториал отрицательного числа невозможен")
        return

    result = math.factorial(a)

    print(f"{a}! =", result)

    save_history(f"{a}! = {result}")


def quadratic_operation():
    print("Уравнение вида ax² + bx + c = 0")

    a = float(input("a = "))
    b = float(input("b = "))
    c = float(input("c = "))

    if a == 0:
        print("Коэффициент a не может быть равен 0!")
        return

    discriminant = b**2 - 4*a*c

    if discriminant > 0:
        x1 = (-b + math.sqrt(discriminant)) / (2*a)
        x2 = (-b - math.sqrt(discriminant)) / (2*a)

        print(f"Два корня: x1 = {x1:.4f}, x2 = {x2:.4f}")

        save_history(f"Квадратное уравнение: x1={x1}, x2={x2}")

    elif discriminant == 0:
        x = -b / (2*a)

        print(f"Один корень: x = {x:.4f}")

        save_history(f"Квадратное уравнение: x={x}")

    else:
        x1 = (-b + cmath.sqrt(discriminant)) / (2*a)
        x2 = (-b - cmath.sqrt(discriminant)) / (2*a)

        print(f"Комплексные корни:")
        print(f"x1 = {x1}")
        print(f"x2 = {x2}")

        save_history(f"Комплексные корни: {x1}, {x2}")


def complex_numbers_operation():
    print("Комплексные числа вида a+bj")

    a1 = float(input("Первое число — вещественная часть: "))
    b1 = float(input("Первое число — мнимая часть: "))

    a2 = float(input("Второе число — вещественная часть: "))
    b2 = float(input("Второе число — мнимая часть: "))

    c1 = complex(a1, b1)
    c2 = complex(a2, b2)

    print(f"Сложение: {c1 + c2}")
    print(f"Вычитание: {c1 - c2}")
    print(f"Умножение: {c1 * c2}")

    if c2 != 0:
        print(f"Деление: {c1 / c2}")
    else:
        print("На ноль делить нельзя!")

    print(f"Модуль первого: {abs(c1):.4f}")
    print(f"Модуль второго: {abs(c2):.4f}")

    save_history(f"Комплексные числа: {c1} и {c2}")


def matrix_operation():
    print("Матрица A (2x2):")

    a11 = float(input("A[1][1]: "))
    a12 = float(input("A[1][2]: "))
    a21 = float(input("A[2][1]: "))
    a22 = float(input("A[2][2]: "))

    print("Матрица B (2x2):")

    b11 = float(input("B[1][1]: "))
    b12 = float(input("B[1][2]: "))
    b21 = float(input("B[2][1]: "))
    b22 = float(input("B[2][2]: "))

    print("\nA + B:")
    print(f"| {a11+b11:.2f} {a12+b12:.2f} |")
    print(f"| {a21+b21:.2f} {a22+b22:.2f} |")

    print("\nA × B:")
    print(f"| {a11*b11+a12*b21:.2f} {a11*b12+a12*b22:.2f} |")
    print(f"| {a21*b11+a22*b21:.2f} {a21*b12+a22*b22:.2f} |")

    det_a = a11*a22 - a12*a21
    det_b = b11*b22 - b12*b21

    print(f"\nОпределитель A: {det_a:.2f}")
    print(f"Определитель B: {det_b:.2f}")

    save_history("Операции с матрицами выполнены")


def conversion_operation():
    print("1. Градусы → Радианы")
    print("2. Радианы → Градусы")

    conv = input("Выбор: ")

    if conv == "1":
        deg = float(input("Градусы: "))

        result = math.radians(deg)

        print(f"{deg}° = {result:.6f} рад")

        save_history(f"{deg}° = {result} рад")

    elif conv == "2":
        rad = float(input("Радианы: "))

        result = math.degrees(rad)

        print(f"{rad} рад = {result:.6f}°")

        save_history(f"{rad} рад = {result}°")


def percent_operation():
    print("1. Найти процент от числа")
    print("2. Сколько процентов число составляет от другого")

    choice = input("Выбор: ")

    if choice == "1":
        number = float(input("Число: "))
        percent = float(input("Процент: "))

        result = number * percent / 100

        print("Ответ:", result)

        save_history(f"{percent}% от {number} = {result}")

    elif choice == "2":
        a = float(input("Первое число: "))
        b = float(input("Второе число: "))

        result = (a / b) * 100

        print("Ответ:", result, "%")

        save_history(f"{a} от {b} = {result}%")


def number_tools():
    print("1. Проверка на простое число")
    print("2. НОД")
    print("3. НОК")

    choice = input("Выбор: ")

    if choice == "1":
        n = int(input("Число: "))

        prime = True

        if n < 2:
            prime = False
        else:
            for i in range(2, int(math.sqrt(n)) + 1):
                if n % i == 0:
                    prime = False
                    break

        if prime:
            print("Число простое")
        else:
            print("Число не простое")

        save_history(f"Проверка простого числа: {n}")

    elif choice == "2":
        a = int(input("Первое число: "))
        b = int(input("Второе число: "))

        result = math.gcd(a, b)

        print("НОД =", result)

        save_history(f"НОД({a}, {b}) = {result}")

    elif choice == "3":
        a = int(input("Первое число: "))
        b = int(input("Второе число: "))

        result = abs(a * b) // math.gcd(a, b)

        print("НОК =", result)

        save_history(f"НОК({a}, {b}) = {result}")


def expression_parser():
    expression = input("Введите выражение: ")

    allowed = "0123456789+-*/().% "

    for char in expression:
        if char not in allowed:
            print("Недопустимые символы!")
            return

    result = eval(expression)

    print("Ответ:", result)

    save_history(f"{expression} = {result}")


def plot_graph():
    expression = input("Введите функцию от x (например, x**2): ")

    x_values = []
    y_values = []

    for i in range(-100, 101):
        x = i / 10  
        try:
            y = eval(expression)
            x_values.append(x)
            y_values.append(y)
        except:
            pass

    plt.figure(figsize=(8, 6))
    plt.plot(x_values, y_values, color="blue", linewidth=2)
    plt.title(f"y = {expression}")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.axhline(0, color="black", linewidth=0.8)
    plt.axvline(0, color="black", linewidth=0.8)
    plt.show()

    save_history(f"График построен: y = {expression}")


def main():
    while True:
        show_menu()

        choice = input("\nВыбери операцию: ")

        try:
            if choice == "1":
                basic_operations()

            elif choice == "2":
                power_operation()

            elif choice == "3":
                root_operation()

            elif choice == "4":
                logarithm_operation()

            elif choice == "5":
                trigonometry_operation()

            elif choice == "6":
                factorial_operation()

            elif choice == "7":
                quadratic_operation()

            elif choice == "8":
                complex_numbers_operation()

            elif choice == "9":
                matrix_operation()

            elif choice == "10":
                conversion_operation()

            elif choice == "11":
                percent_operation()

            elif choice == "12":
                number_tools()

            elif choice == "13":
                show_history()

            elif choice == "14":
                expression_parser()

            elif choice == "15":
                plot_graph()

            elif choice == "0":
                print("До свидания! — Kronos Calculator V5")
                input("\nНажми Enter для закрытия...")
                break

            else:
                print("Неверный выбор!")

        except ValueError:
            print("Ошибка! Введи число, а не букву.")

        except ZeroDivisionError:
            print("Ошибка! Деление на ноль.")

        except Exception as e:
            print(f"Ошибка: {e}")

        again = input("\nПосчитать ещё? (да/нет): ")

        if again.lower() != "да":
            print("До свидания!")
            input("\nНажми Enter для закрытия...")
            break


if __name__ == "__main__":
    main()