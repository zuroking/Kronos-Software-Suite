# Kronos Calculator V1 by Kronos Russian

import math
from py_compile import main

print("Kronos Calculator V1 от Kronos Russian")
def add(x, y):
    return x + y
def subtract(x, y):
    return x - y
def multiply(x, y):
    return x * y
def divide(x, y):
    if y == 0:
        return "Ошибка: Деление на ноль невозможно"
    return x / y
def power(x, y):
    return x ** y
def square_root(x):
    if x < 0:
        return "Ошибка: Невозможно извлечь квадратный корень из отрицательного числа"
    return math.sqrt(x)
def logarithm(x, base=math.e):
    if x <= 0:
        return "Ошибка: Логарифм не определен для неположительных чисел"
    if base <= 1:
        return "Ошибка: Основание логарифма должно быть больше 1"
    return math.log(x, base)
def factorial(n):
    if n < 0:
        return "Ошибка: Факториал не определен для отрицательных чисел"
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def main():
    print("Выберите операцию:")
    print("1. Сложение")
    print("2. Вычитание")
    print("3. Умножение")
    print("4. Деление")
    print("5. Возведение в степень")
    print("6. Квадратный корень")
    print("7. Логарифм")
    print("8. Факториал")
    
    choice = input("Введите выбор (1-8): ")
    
    if choice in ['1', '2', '3', '4', '5']:
        num1 = float(input("Введите первое число: "))
        num2 = float(input("Введите второе число: "))
        
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
        num = float(input("Введите число: "))
        print(f"Квадратный корень из {num} = {square_root(num)}")
    
    elif choice == '7':
        num = float(input("Введите число: "))
        base = input("Введите основание (по умолчанию e): ")
        if base:
            base = float(base)
            print(f"Логарифм {num} с основанием {base} = {logarithm(num, base)}")
        else:
            print(f"Натуральный логарифм {num} = {logarithm(num)}")
    
    elif choice == '8':
        num = int(input("Введите число: "))
        print(f"Факториал {num} = {factorial(num)}")
    
    else:
        print("Invalid input")
while True:
    main()
    cont = input("Хотите выполнить еще одну операцию? (да/нет): ")
    if cont.lower() != 'да':
        print("До свидания!")
        break

if __name__ == "__main__":
    main()