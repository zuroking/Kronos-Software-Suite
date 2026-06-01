import math

print("=" * 40)
print("   Kronos Calculator V3 by Kronos English")
print("   Date: 28.05.2026")
print("=" * 40)

print("Welcome to Kronos Calculator V3! Choose an operation from the menu below. Enter '0' to exit.")
print("This calculator supports basic operations, powers, roots, logarithms, trigonometry, and factorials. Enjoy!")
print("Author: Kronos English — Kronos Calculator V3")

print("\n1. Basic operations (+, -, *, /)")
print("2. Power (a^b)")
print("3. Root (√)")
print("4. Logarithm")
print("5. Trigonometry (sin, cos, tan)")
print("6. Factorial")
print("0. Exit")

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
            print("1. Natural logarithm (ln)")
            print("2. Decimal logarithm (log10)")
            print("3. Logarithm with custom base")
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

        elif choice == "0":
            print("Goodbye! — Kronos Calculator V3")
            input("\nPress Enter to close...")
            break

        else:
            print("Invalid choice!")

    except ValueError:
        print("Error! Please enter a number, not a letter.")
    except Exception as e:
        print(f"Error: {e}")

    again = input("\nCalculate again? (yes/no): ")
    if again.lower() != "yes":
        print("Goodbye!")
        input("\nPress Enter to close...")
        break
    else:
        print("\n1. Basic operations (+, -, *, /)")
        print("2. Power (a^b)")
        print("3. Root (√)")
        print("4. Logarithm")
        print("5. Trigonometry (sin, cos, tan)")
        print("6. Factorial")
        print("0. Exit")
        choice = input("\nChoose an operation: ")