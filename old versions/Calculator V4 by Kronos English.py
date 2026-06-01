import math
import cmath

print("=" * 40)
print("   Kronos Calculator V4 by Kronos Russian")
print("   Scientific calculator — everything in one!")
print("   Date: 30.05.2026")
print("=" * 40)

def show_menu():
    print("\n--- BASIC ---")
    print("1. Addition, subtraction, multiplication, division")
    print("2. Power (a^b)")
    print("3. Root")
    print("--- SCIENTIFIC ---")
    print("4. Logarithm")
    print("5. Trigonometry (sin, cos, tan)")
    print("6. Factorial")
    print("--- ADVANCED ---")
    print("7. Quadratic equation (ax²+bx+c=0)")
    print("8. Complex numbers (a+bj)")
    print("9. Matrices (2x2)")
    print("10. Degrees ↔ Radians")
    print("0. Exit")

show_menu()
choice = input("\nChoose an operation: ")

while True:
    try:
        if choice == "1":
            a = float(input("First number: "))
            b = float(input("Second number: "))
            print("Addition:", a + b)
            print("Subtraction:", a - b)
            print("Multiplication:", a * b)
            if b != 0:
                print("Division:", a / b)
                print("Remainder:", a % b)
            else:
                print("Cannot divide by zero!")

        elif choice == "2":
            a = float(input("Base: "))
            b = float(input("Exponent: "))
            print(f"{a}^{b} =", a ** b)

        elif choice == "3":
            a = float(input("Number: "))
            n = float(input("Root degree (2 = square root, 3 = cube root): "))
            if a >= 0:
                print(f"Root of degree {n} from {a} =", a ** (1/n))
            else:
                print("Cannot take root of negative number!")

        elif choice == "4":
            a = float(input("Number: "))
            print("1. Natural (ln)")
            print("2. Decimal (log10)")
            print("3. Custom base")
            log_choice = input("Choice: ")
            if log_choice == "1":
                print("ln =", math.log(a))
            elif log_choice == "2":
                print("log10 =", math.log10(a))
            elif log_choice == "3":
                base = float(input("Base: "))
                print(f"log{base}({a}) =", math.log(a, base))

        elif choice == "5":
            a = float(input("Angle in degrees: "))
            r = math.radians(a)
            print(f"sin({a}°) =", round(math.sin(r), 10))
            print(f"cos({a}°) =", round(math.cos(r), 10))
            print(f"tan({a}°) =", round(math.tan(r), 10))

        elif choice == "6":
            a = int(input("Number: "))
            print(f"{a}! =", math.factorial(a))

        elif choice == "7":
            print("Equation of the form ax² + bx + c = 0")
            a = float(input("a = "))
            b = float(input("b = "))
            c = float(input("c = "))
            discriminant = b**2 - 4*a*c
            if discriminant > 0:
                x1 = (-b + math.sqrt(discriminant)) / (2*a)
                x2 = (-b - math.sqrt(discriminant)) / (2*a)
                print(f"Two roots: x1 = {x1:.4f}, x2 = {x2:.4f}")
            elif discriminant == 0:
                x = -b / (2*a)
                print(f"One root: x = {x:.4f}")
            else:
                x1 = (-b + cmath.sqrt(discriminant)) / (2*a)
                x2 = (-b - cmath.sqrt(discriminant)) / (2*a)
                print(f"Complex roots:")
                print(f"x1 = {x1}")
                print(f"x2 = {x2}")

        elif choice == "8":
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
            print(f"Magnitude of first: {abs(c1):.4f}")
            print(f"Magnitude of second: {abs(c2):.4f}")

        elif choice == "9":
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
            print(f"| {a11+b11} {a12+b12} |")
            print(f"| {a21+b21} {a22+b22} |")
            print("\nA × B:")
            print(f"| {a11*b11+a12*b21} {a11*b12+a12*b22} |")
            print(f"| {a21*b11+a22*b21} {a21*b12+a22*b22} |")
            det_a = a11*a22 - a12*a21
            det_b = b11*b22 - b12*b21
            print(f"\nDeterminant of A: {det_a}")
            print(f"Determinant of B: {det_b}")

        elif choice == "10":
            print("1. Degrees → Radians")
            print("2. Radians → Degrees")
            conv = input("Choice: ")
            if conv == "1":
                deg = float(input("Degrees: "))
                print(f"{deg}° = {math.radians(deg):.6f} rad")
            elif conv == "2":
                rad = float(input("Radians: "))
                print(f"{rad} rad = {math.degrees(rad):.6f}°")

        elif choice == "0":
            print("Goodbye! — Kronos Calculator V4")
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
    show_menu()
    choice = input("\nChoose operation: ")