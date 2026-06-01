import math
import cmath
import random
import matplotlib.pyplot as plt

history = []

print("=" * 40)
print("   Kronos Calculator V5 by Kronos Russian")
print("   Scientific-engineering calculator — all-in-one")
print("   Date: 02.06.2026")
print("=" * 40)


def save_history(text):
    history.append(text)

    with open("history.txt", "a", encoding="utf-8") as file:
        file.write(text + "\n")


def show_history():
    print("\n--- CALCULATION HISTORY ---")

    if not history:
        print("History is empty.")
        return

    for item in history:
        print(item)


def show_menu():
    print("\n--- BASIC ---")
    print("1. Addition, subtraction, multiplication, division")
    print("2. Power (a^b)")
    print("3. Root (n-th root)")

    print("--- SCIENTIFIC ---")
    print("4. Logarithm")
    print("5. Trigonometry (sin, cos, tan)")
    print("6. Factorial")

    print("--- ADVANCED ---")
    print("7. Quadratic equation (ax²+bx+c=0)")
    print("8. Complex numbers")
    print("9. Matrices (2x2)")
    print("10. Degrees ↔ Radians")

    print("--- ADVANCED FUNCTIONS ---")
    print("11. Percentages")
    print("12. Prime number / GCD / LCM")
    print("13. Calculation History")
    print("14. Expression Parser")
    print("15. Graph Plotting")
    print("0. Exit")


def basic_operations():
    a = float(input("First number: "))
    b = float(input("Second number: "))

    add = a + b
    sub = a - b
    mul = a * b

    print("Addition:", round(add, 4))
    print("Subtraction:", round(sub, 4))
    print("Multiplication:", round(mul, 4))

    save_history(f"{a} + {b} = {add}")
    save_history(f"{a} - {b} = {sub}")
    save_history(f"{a} * {b} = {mul}")

    if b != 0:
        div = a / b
        mod = a % b

        print("Division:", round(div, 4))
        print("Remainder:", round(mod, 4))

        save_history(f"{a} / {b} = {div}")
        save_history(f"{a} % {b} = {mod}")

    else:
        print("You cannot divide by zero!")


def power_operation():
    a = float(input("Base: "))
    b = float(input("Exponent: "))

    result = a ** b

    print(f"{a}^{b} =", round(result, 4))

    save_history(f"{a}^{b} = {result}")


def root_operation():
    a = float(input("Number: "))
    n = float(input("Root degree (2 = square, 3 = cube): "))

    if n == 0:
        print("Root degree cannot be 0!")
        return

    if a >= 0:
        result = a ** (1 / n)

        print(f"Root of degree {n} from {a} =", round(result, 4))

        save_history(f"Root of degree {n} from {a} = {result}")

    else:
        print("You cannot take the root of a negative number!")


def logarithm_operation():
    a = float(input("Number: "))

    if a <= 0:
        print("Logarithm is only defined for positive numbers")
        return

    print("1. Natural (ln)")
    print("2. Decimal (log10)")
    print("3. Custom base")

    log_choice = input("Choice: ")

    if log_choice == "1":
        result = math.log(a)

        print("ln =", round(result, 6))

        save_history(f"ln({a}) = {result}")

    elif log_choice == "2":
        result = math.log10(a)

        print("log10 =", round(result, 6))

        save_history(f"log10({a}) = {result}")

    elif log_choice == "3":
        base = float(input("Base: "))

        if base <= 0 or base == 1:
            print("Invalid base for logarithm!")
        else:
            result = math.log(a, base)

            print(f"log{base}({a}) =", round(result, 6))

            save_history(f"log{base}({a}) = {result}")


def trigonometry_operation():
    a = float(input("Angle in degrees: "))

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
    a = int(input("Number: "))

    if a < 0:
        print("Factorial of a negative number is not possible")
        return

    result = math.factorial(a)

    print(f"{a}! =", result)

    save_history(f"{a}! = {result}")


def quadratic_operation():
    print("Equation of the form ax² + bx + c = 0")

    a = float(input("a = "))
    b = float(input("b = "))
    c = float(input("c = "))

    if a == 0:
        print("Coefficient a cannot be equal to 0!")
        return

    discriminant = b**2 - 4*a*c

    if discriminant > 0:
        x1 = (-b + math.sqrt(discriminant)) / (2*a)
        x2 = (-b - math.sqrt(discriminant)) / (2*a)

        print(f"Two roots: x1 = {x1:.4f}, x2 = {x2:.4f}")

        save_history(f"Quadratic equation: x1={x1}, x2={x2}")

    elif discriminant == 0:
        x = -b / (2*a)

        print(f"One root: x = {x:.4f}")

        save_history(f"Quadratic equation: x={x}")

    else:
        x1 = (-b + cmath.sqrt(discriminant)) / (2*a)
        x2 = (-b - cmath.sqrt(discriminant)) / (2*a)

        print(f"Complex roots:")
        print(f"x1 = {x1}")
        print(f"x2 = {x2}")

        save_history(f"Complex roots: {x1}, {x2}")


def complex_numbers_operation():
    print("Complex numbers of the form a+bj")

    a1 = float(input("First number — real part: "))
    b1 = float(input("First number — imaginary part: "))

    a2 = float(input("Second number — real part: "))
    b2 = float(input("Second number — imaginary part: "))

    c1 = complex(a1, b1)
    c2 = complex(a2, b2)

    print(f"Addition: {c1 + c2}")
    print(f"Subtraction: {c1 - c2}")
    print(f"Multiplication: {c1 * c2}")

    if c2 != 0:
        print(f"Division: {c1 / c2}")
    else:
        print("You cannot divide by zero!")

    print(f"Magnitude of first: {abs(c1):.4f}")
    print(f"Magnitude of second: {abs(c2):.4f}")

    save_history(f"Complex numbers: {c1} and {c2}")


def matrix_operation():
    print("Matrix A (2x2):")

    a11 = float(input("A[1][1]: "))
    a12 = float(input("A[1][2]: "))
    a21 = float(input("A[2][1]: "))
    a22 = float(input("A[2][2]: "))

    print("Matrix B (2x2):")

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

    print(f"\nDeterminant of A: {det_a:.2f}")
    print(f"Determinant of B: {det_b:.2f}")

    save_history("Matrix operations completed")


def conversion_operation():
    print("1. Degrees → Radians")
    print("2. Radians → Degrees")

    conv = input("Choice: ")

    if conv == "1":
        deg = float(input("Degrees: "))

        result = math.radians(deg)

        print(f"{deg}° = {result:.6f} rad")

        save_history(f"{deg}° = {result} rad")

    elif conv == "2":
        rad = float(input("Radians: "))

        result = math.degrees(rad)

        print(f"{rad} rad = {result:.6f}°")

        save_history(f"{rad} rad = {result}°")


def percent_operation():
    print("1. Find percentage of a number")
    print("2. What percentage of a number is another number")

    choice = input("Choice: ")

    if choice == "1":
        number = float(input("Number: "))
        percent = float(input("Percentage: "))

        result = number * percent / 100

        print("Answer:", result)

        save_history(f"{percent}% of {number} = {result}")

    elif choice == "2":
        a = float(input("First number: "))
        b = float(input("Second number: "))

        result = (a / b) * 100

        print("Answer:", result, "%")

        save_history(f"{a} of {b} = {result}%")


def number_tools():
    print("1. Check if a number is prime")
    print("2. GCD")
    print("3. LCM")

    choice = input("Choice: ")

    if choice == "1":
        n = int(input("Number: "))

        prime = True

        if n < 2:
            prime = False
        else:
            for i in range(2, int(math.sqrt(n)) + 1):
                if n % i == 0:
                    prime = False
                    break

        if prime:
            print("The number is prime")
        else:
            print("The number is not prime")

        save_history(f"Prime number check: {n}")

    elif choice == "2":
        a = int(input("First number: "))
        b = int(input("Second number: "))

        result = math.gcd(a, b)

        print("GCD =", result)

        save_history(f"GCD({a}, {b}) = {result}")

    elif choice == "3":
        a = int(input("First number: "))
        b = int(input("Second number: "))

        result = abs(a * b) // math.gcd(a, b)

        print("LCM =", result)

        save_history(f"LCM({a}, {b}) = {result}")


def expression_parser():
    expression = input("Enter expression: ")

    allowed = "0123456789+-*/().% "

    for char in expression:
        if char not in allowed:
            print("Invalid characters!")
            return

    result = eval(expression)

    print("Answer:", result)

    save_history(f"{expression} = {result}")


def plot_graph():
    expression = input("Enter function of x (e.g., x**2): ")

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

    save_history(f"Graph plotted: y = {expression}")

def main():
    while True:
        show_menu()

        choice = input("\nChoose operation: ")

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
                print("Goodbye! — Kronos Calculator V5")
                input("\nPress Enter to close...")
                break

            else:
                print("Invalid choice!")

        except ValueError:
            print("Error! Please enter a number, not a letter.")

        except ZeroDivisionError:
            print("Error! Division by zero.")

        except Exception as e:
            print(f"Error: {e}")

        again = input("\nCalculate again? (yes/no): ")

        if again.lower() != "yes":
            print("Goodbye!")
            input("\nPress Enter to close...")
            break


if __name__ == "__main__":
    main()