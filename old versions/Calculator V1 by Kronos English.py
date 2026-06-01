# Kronos Calculator V1 by Kronos English

import math
from py_compile import main
print("Kronos Calculator V1 by Kronos English")
def add(x, y):
    return x + y
def subtract(x, y):
    return x - y
def multiply(x, y):
    return x * y
def divide(x, y):
    if y == 0:
        return "Error: Division by zero"
    return x / y
def power(x, y):
    return x ** y
def square_root(x):
    if x < 0:
        return "Error: Cannot take square root of a negative number"
    return math.sqrt(x)
def logarithm(x, base=math.e):
    if x <= 0:
        return "Error: Logarithm undefined for non-positive numbers"
    if base <= 1:
        return "Error: Logarithm base must be greater than 1"
    return math.log(x, base)
def factorial(n):
    if n < 0:
        return "Error: Factorial undefined for negative numbers"
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
def main():
    print("Select operation:")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    print("5. Power")
    print("6. Square Root")
    print("7. Logarithm")
    print("8. Factorial")
    choice = input("Enter choice (1-8): ")
    if choice in ['1', '2', '3', '4', '5']:
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        if choice == '1':
            print(f"{num1} + {num2} = {add(num1, num2)}")
        elif choice == '2':
            print(f"{num1} - {num2} = {subtract(num1, num2)}")
        elif choice == '3':
            print(f"{num1} * {num2} = {multiply(num1, num2)}")
        elif choice == '4':
            print(f"{num1} / {num2} = {divide(num1, num2)}")
        elif choice == '5':
            print(f"{num1} ^ {num2} = {power(num1, num2)}")
    elif choice == '6':
        num = float(input("Enter number: "))
        print(f"Square root of {num} = {square_root(num)}")
    
    elif choice == '7':
        num = float(input("Enter number: "))
        base = input("Enter base (default is e): ")
        if base:
            base = float(base)
            print(f"Logarithm of {num} with base {base} = {logarithm(num, base)}")
        else:
            print(f"Natural logarithm of {num} = {logarithm(num)}")
    elif choice == '8':
        num = int(input("Enter number: "))
        print(f"Factorial of {num} = {factorial(num)}")
    else:
        print("Invalid input")
while True:
    main()
    cont = input("Do you want to perform another calculation? (yes/no): ")
    if cont.lower() != 'yes':
        print("Goodbye!")
        break
if __name__ == "__main__":
    main()