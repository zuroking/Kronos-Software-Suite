import math
import cmath

print("=" * 40)
print("   Kronos Calculator V4 by ZuroCode")
print("   Научный калькулятор — всё в одном")
print("   Дата: 28.05.2026")
print("=" * 40)


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
    print("0. Выход")


def basic_operations():
    a = float(input("Первое число: "))
    b = float(input("Второе число: "))

    print("Сложение:", round(a + b, 4))
    print("Вычитание:", round(a - b, 4))
    print("Умножение:", round(a * b, 4))

    if b != 0:
        print("Деление:", round(a / b, 4))
        print("Остаток:", round(a % b, 4))
    else:
        print("На ноль делить нельзя!")


def power_operation():
    a = float(input("Основание: "))
    b = float(input("Степень: "))

    print(f"{a}^{b} =", round(a ** b, 4))


def root_operation():
    a = float(input("Число: "))
    n = float(input("Степень корня (2 = квадратный, 3 = кубический): "))

    if n == 0:
        print("Степень корня не может быть 0!")
        return

    if a >= 0:
        print(f"Корень степени {n} из {a} =", round(a ** (1 / n), 4))
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
        print("ln =", round(math.log(a), 6))

    elif log_choice == "2":
        print("log10 =", round(math.log10(a), 6))

    elif log_choice == "3":
        base = float(input("Основание: "))

        if base <= 0 or base == 1:
            print("Некорректное основание логарифма!")
        else:
            print(f"log{base}({a}) =", round(math.log(a, base), 6))


def trigonometry_operation():
    a = float(input("Угол в градусах: "))

    r = math.radians(a)

    print(f"sin({a}°) =", round(math.sin(r), 10))
    print(f"cos({a}°) =", round(math.cos(r), 10))
    print(f"tan({a}°) =", round(math.tan(r), 10))


def factorial_operation():
    a = int(input("Число: "))

    if a < 0:
        print("Факториал отрицательного числа невозможен")
        return

    print(f"{a}! =", math.factorial(a))


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

    elif discriminant == 0:
        x = -b / (2*a)

        print(f"Один корень: x = {x:.4f}")

    else:
        x1 = (-b + cmath.sqrt(discriminant)) / (2*a)
        x2 = (-b - cmath.sqrt(discriminant)) / (2*a)

        print(f"Комплексные корни:")
        print(f"x1 = {x1}")
        print(f"x2 = {x2}")


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


def conversion_operation():
    print("1. Градусы → Радианы")
    print("2. Радианы → Градусы")

    conv = input("Выбор: ")

    if conv == "1":
        deg = float(input("Градусы: "))
        print(f"{deg}° = {math.radians(deg):.6f} рад")

    elif conv == "2":
        rad = float(input("Радианы: "))
        print(f"{rad} рад = {math.degrees(rad):.6f}°")


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

            elif choice == "0":
                print("До свидания! — Kronos Calculator V4")
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