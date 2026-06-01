import math

print("=" * 40)
print("   Kronos Calculator V2 by Kronos English")
print("   Date: 26.05.2026")
print("=" * 40)

print("Welcome to Kronos Calculator V2! Choose an operation from the menu below. Enter '0' to exit.")
print("This calculator supports basic operations, powers, roots, logarithms, trigonometry, and factorials. Enjoy!")
print("Author: Kronos English — Kronos Calculator V2")

while True:
    try:
        a = float(input("Insert the first number: "))
        b = float(input("Insert the second number: "))
        break
    except ValueError:
        print("Error! Please enter a number, not a letter. Try again.")
        
print("The sum of the two numbers is:", a + b)
print("The difference of the two numbers is:", a - b)
print("The product of the two numbers is:", a * b)

if b != 0:
    print("The quotient of the two numbers is:", a / b)
    print("The modulus of the two numbers is:", a % b)
else:
    print("Cannot divide by zero; quotient and modulus skipped.")

if a >= 0:
    print("The square root of the first number is:", math.sqrt(a))
else:
    print("Cannot compute square root of the first number (negative).")

if b >= 0:
    print("The square root of the second number is:", math.sqrt(b))
else:
    print("Cannot compute square root of the second number (negative).")

print("""Thank you for using Kronos Calculator!
I hope I was able to help you with your calculations.
Have a great day!
Goodbye,
Kronos Calculator""")
while True:
    again = input("\nContinue? (yes/no): ")
    if again.lower() != "yes":
        break
    a = float(input("Enter the first number: "))
    b = float(input("Enter the second number: "))
    print("Addition:", a + b)
    print("Subtraction:", a - b)
    print("Multiplication:", a * b)
    if b != 0:
        print("Division:", a / b)
    else:
        print("Division by zero is not possible!")
    if a >= 0:
        print("Square root of a:", math.sqrt(a))
    else:
        print("Square root of negative number a is not possible!")
    if b >= 0:
        print("Square root of b:", math.sqrt(b))
    else:
        print("Square root of negative number b is not possible!")
        again = input("Generate another one? (yes/no): ")
while again.lower() == "yes":
    a = float(input("Enter the first number: "))
    b = float(input("Enter the second number: "))
    print("Addition:", a + b)
    print("Subtraction:", a - b)
    print("Multiplication:", a * b)
    if b != 0:
        print("Division:", a / b)
    else:
        print("Division by zero is not possible!")
    if a >= 0:
        print("Square root of a:", math.sqrt(a))
    else:
        print("Square root of negative number a is not possible!")
    if b >= 0:
        print("Square root of b:", math.sqrt(b))
    else:
        print("Square root of negative number b is not possible!")
    again = input("Generate another one? (yes/no): ")
    if again.lower() != "yes":
        break