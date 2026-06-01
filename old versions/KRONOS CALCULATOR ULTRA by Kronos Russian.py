# KRONOS CALCULATOR ULTRA

from __future__ import annotations

import math
import os
import random
import secrets
from dataclasses import dataclass
from datetime import datetime
from fractions import Fraction
from typing import List, Optional, Tuple

# ==========================================
# ЯДРО И ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ==========================================

def clear_screen() -> None:
    try:
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")
    except Exception:
        pass

def safe_int(prompt: str) -> int:
    while True:
        try:
            s = input(prompt).strip()
            return int(s)
        except Exception:
            print("Ошибка: пожалуйста, введите целое число.")

def safe_float(prompt: str) -> float:
    while True:
        try:
            s = input(prompt).replace(",", ".").strip()
            return float(s)
        except Exception:
            print("Ошибка: пожалуйста, введите число.")

def safe_choice(prompt: str, valid: set[int]) -> int:
    while True:
        n = safe_int(prompt)
        if n in valid:
            return n
        print(f"Ошибка: допустимые варианты: {sorted(valid)}")

def pause() -> None:
    try:
        input("\nНажмите Enter для продолжения...")
    except Exception:
        pass

def banner() -> None:
    now = datetime.now().strftime("%d.%m.%Y")
    print("=" * 60)
    print("   ██╗  ██╗██████╗  ██████╗ ███╗   ██╗██████╗ ███████╗")
    print("   ██║ ██╔╝██╔══██╗██╔═══██╗████╗  ██║██╔══██╗██╔════╝")
    print("   █████╔╝ ██████╔╝██║   ██║██╔██╗ ██║██║  ██║███████╗")
    print("   ██╔═██╗ ██╔══██╗██║   ██║██║╚██╗██║██║  ██║╚════██║")
    print("   ██║  ██╗██║  ██║╚██████╔╝██║ ╚████║██████╔╝███████║")
    print("   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═════╝ ╚══════╝")
    print("=" * 60)
    print("   Kronos Calculator ULTRA by Kronos Russian (2026)")
    print("   Многофункциональный калькулятор для сложных вычислений, анализа и графиков.")
    print(f"   Дата: {now}")
    print("=" * 60)

# ==========================================
# СИСТЕМА ИСТОРИИ
# ==========================================

@dataclass
class HistoryItem:
    timestamp: str
    action: str
    result: str

    def format_line(self) -> str:
        return f"[{self.timestamp}] {self.action} = {self.result}"

class History:
    def __init__(self) -> None:
        self._items: List[HistoryItem] = []

    def add(self, action: str, result: str) -> None:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._items.append(HistoryItem(timestamp=now, action=action, result=result))

    def clear(self) -> None:
        self._items.clear()

    def show(self) -> None:
        if not self._items:
            print("История пуста.")
            return
        print("\n--- История вычислений ---")
        for item in self._items:
            print(item.format_line())
        print("----------------------------")

# ==========================================
# БАЗОВЫЙ ПАРСЕР ВЫРАЖЕНИЙ (ОПЗ)
# ==========================================

Token = Tuple[str, str]

class ExpressionError(Exception):
    pass

def tokenize(expr: str) -> List[Token]:
    tokens: List[Token] = []
    i = 0
    n = len(expr)

    while i < n:
        ch = expr[i]
        if ch.isspace():
            i += 1
            continue
        if ch in "()":
            tokens.append(("PAREN", ch))
            i += 1
            continue
        if expr.startswith("**", i):
            tokens.append(("OP", "**"))
            i += 2
            continue
        if expr.startswith("//", i):
            tokens.append(("OP", "//"))
            i += 2
            continue
        if ch in "+-*/%":
            tokens.append(("OP", ch))
            i += 1
            continue
        if ch.isdigit() or ch == ".":
            start = i
            saw_dot = ch == "."
            i += 1
            while i < n:
                c = expr[i]
                if c.isdigit():
                    i += 1
                    continue
                if c == ".":
                    if saw_dot:
                        break
                    saw_dot = True
                    i += 1
                    continue
                break
            s = expr[start:i]
            if s in {".", ""}:
                raise ExpressionError("Неверный формат числа")
            tokens.append(("NUM", s))
            continue
        raise ExpressionError(f"Неизвестный символ: {ch!r}")
    return tokens

PRECEDENCE = {
    "**": (4, "right"), "*": (3, "left"), "/": (3, "left"),
    "//": (3, "left"), "%": (3, "left"), "+": (2, "left"), "-": (2, "left"),
}

def to_rpn(tokens: List[Token]) -> List[Token]:
    output, stack = [], []
    prev_type, prev_val = None, None

    for ttype, val in tokens:
        if ttype == "NUM":
            output.append((ttype, val))
        elif ttype == "PAREN" and val == "(":
            stack.append((ttype, val))
        elif ttype == "PAREN" and val == ")":
            while stack and stack[-1][1] != "(":
                output.append(stack.pop())
            if not stack: raise ExpressionError("Несогласованные скобки")
            stack.pop()
        elif ttype == "OP":
            op = val
            if op == "-" and (prev_type is None or (prev_type == "PAREN" and prev_val == "(") or prev_type == "OP"):
                op = "u-"
            if op == "u-":
                prec, assoc = (5, "right")
                while stack and stack[-1][0] == "OP":
                    top_prec, _ = PRECEDENCE.get(stack[-1][1], (0, "left"))
                    if top_prec > prec: output.append(stack.pop())
                    else: break
                stack.append(("OP", "u-"))
            else:
                prec, assoc = PRECEDENCE[op]
                while stack and stack[-1][0] == "OP":
                    top_prec, top_assoc = PRECEDENCE[stack[-1][1]]
                    if (assoc == "left" and prec <= top_prec) or (assoc == "right" and prec < top_prec):
                        output.append(stack.pop())
                    else: break
                stack.append(("OP", op))
        prev_type, prev_val = ttype, val

    while stack:
        if stack[-1][0] == "PAREN": raise ExpressionError("Несогласованные скобки")
        output.append(stack.pop())
    return output

def eval_rpn(rpn: List[Token]) -> float:
    stack: List[float] = []
    for ttype, val in rpn:
        if ttype == "NUM":
            stack.append(float(val))
        elif ttype == "OP":
            if val == "u-":
                stack.append(-stack.pop())
                continue
            if len(stack) < 2: raise ExpressionError("Недостаточно операндов")
            b, a = stack.pop(), stack.pop()
            if val == "+": stack.append(a + b)
            elif val == "-": stack.append(a - b)
            elif val == "*": stack.append(a * b)
            elif val == "/": stack.append(a / b)
            elif val == "//": stack.append(math.floor(a / b))
            elif val == "%": stack.append(a % b)
            elif val == "**": stack.append(a ** b)
    if len(stack) != 1: raise ExpressionError("Некорректное выражение")
    return stack[0]

def evaluate_base_expression(expr: str) -> float:
    return eval_rpn(to_rpn(tokenize(expr)))

# ==========================================
# НАУЧНЫЙ ПАРСЕР И ФУНКЦИИ
# ==========================================

def get_math_env() -> dict:
    env = {name: getattr(math, name) for name in dir(math) if not name.startswith("_")}
    env['ln'] = math.log
    return env

def safe_scientific_eval(expression: str, extra_vars: dict = None) -> float:
    env = get_math_env()
    if extra_vars:
        env.update(extra_vars)
        
    allowed_chars = set("0123456789+-*/%()., _abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
    if any(ch not in allowed_chars for ch in expression):
        raise ValueError("Обнаружен недопустимый символ.")

    result = eval(expression, {"__builtins__": {}}, env)
    return float(result)

# ==========================================
# МОДУЛЬ 1: МАТЕМАТИЧЕСКИЙ АНАЛИЗ (CALCULUS)
# ==========================================

def numerical_derivative(expr: str, x_val: float, h: float = 1e-5) -> float:
    f_plus = safe_scientific_eval(expr, {"x": x_val + h})
    f_minus = safe_scientific_eval(expr, {"x": x_val - h})
    return (f_plus - f_minus) / (2 * h)

def numerical_integral(expr: str, a: float, b: float, n: int = 10000) -> float:
    h = (b - a) / n
    s = 0.5 * (safe_scientific_eval(expr, {"x": a}) + safe_scientific_eval(expr, {"x": b}))
    for i in range(1, n):
        s += safe_scientific_eval(expr, {"x": a + i * h})
    return s * h

def calculus_menu(history: History) -> None:
    while True:
        clear_screen()
        print("\n--- МАТЕМАТИЧЕСКИЙ АНАЛИЗ ---")
        print("1) Производная функции в точке (f'(x))")
        print("2) Определенный интеграл (метод трапеций)")
        print("0) Назад")
        
        ch = safe_choice("Выберите пункт: ", {0, 1, 2})
        if ch == 0: return
        
        try:
            expr = input("Введите функцию f(x) (например, sin(x)*x**2): ").strip()
            
            if ch == 1:
                x_val = safe_float("Введите точку x: ")
                res = numerical_derivative(expr, x_val)
                print(f"f'({x_val}) ≈ {res:.8g}")
                history.add("Производная", f"d/dx ({expr}) при x={x_val} ≈ {res:.8g}")
            
            elif ch == 2:
                a = safe_float("Нижний предел (a): ")
                b = safe_float("Верхний предел (b): ")
                res = numerical_integral(expr, a, b)
                print(f"∫ от {a} до {b} ({expr}) dx ≈ {res:.8g}")
                history.add("Интеграл", f"∫[{a},{b}] ({expr})dx ≈ {res:.8g}")
        except Exception as e:
            print(f"Ошибка вычисления: {e}")
        pause()

# ==========================================
# МОДУЛЬ 2: ТЕОРИЯ ЧИСЕЛ И ДРОБИ
# ==========================================

def prime_factors(n: int) -> List[int]:
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors

def number_theory_menu(history: History) -> None:
    while True:
        clear_screen()
        print("\n--- ТЕОРИЯ ЧИСЕЛ И ДРОБИ ---")
        print("1) НОД и НОК двух чисел")
        print("2) Разложение на простые множители")
        print("3) Проверка на простое число")
        print("4) Калькулятор обыкновенных дробей")
        print("0) Назад")

        ch = safe_choice("Выберите пункт: ", {0, 1, 2, 3, 4})
        if ch == 0: return
        
        try:
            if ch == 1:
                a = safe_int("Введите первое число: ")
                b = safe_int("Введите второе число: ")
                gcd = math.gcd(a, b)
                lcm = abs(a*b) // gcd if gcd else 0
                print(f"НОД({a}, {b}) = {gcd}")
                print(f"НОК({a}, {b}) = {lcm}")
                history.add("НОД/НОК", f"НОД({a},{b})={gcd}, НОК={lcm}")

            elif ch == 2:
                n = safe_int("Введите натуральное число: ")
                if n < 2:
                    print("Разложение определено для чисел >= 2")
                else:
                    factors = prime_factors(n)
                    res = " * ".join(map(str, factors))
                    print(f"{n} = {res}")
                    history.add("Факторизация", f"{n} = {res}")

            elif ch == 3:
                n = safe_int("Введите натуральное число: ")
                if n < 2:
                    print(f"{n} не является простым.")
                else:
                    factors = prime_factors(n)
                    if len(factors) == 1:
                        print(f"{n} — ПРОСТОЕ число.")
                        history.add("Простое число?", f"{n} — Да")
                    else:
                        print(f"{n} — СОСТАВНОЕ число.")
                        history.add("Простое число?", f"{n} — Нет")

            elif ch == 4:
                print("Введите выражение с дробями (например: 1/2 + 1/3 или 5/8 * 2/3)")
                expr = input("Выражение: ").strip()
                parts = expr.split()
                if len(parts) == 3:
                    f1 = Fraction(parts[0])
                    op = parts[1]
                    f2 = Fraction(parts[2])
                    if op == '+': res = f1 + f2
                    elif op == '-': res = f1 - f2
                    elif op == '*': res = f1 * f2
                    elif op == '/': res = f1 / f2
                    else: raise ValueError("Неизвестный оператор")
                    print(f"Результат: {res} (или {float(res):.6g})")
                    history.add("Дроби", f"{expr} = {res}")
                else:
                    print("Формат: ДРОБЬ ОПЕРАТОР ДРОБЬ (через пробел).")
        except Exception as e:
            print(f"Ошибка: {e}")
        pause()

# ==========================================
# МОДУЛЬ 3: ВЕКТОРЫ И МАТРИЦЫ
# ==========================================

def matrix_menu(history: History) -> None:
    while True:
        clear_screen()
        print("\n--- ВЕКТОРЫ И МАТРИЦЫ ---")
        print("1) Длина вектора (2D / 3D)")
        print("2) Скалярное произведение векторов")
        print("3) Определитель матрицы 2x2")
        print("4) Определитель матрицы 3x3")
        print("0) Назад")

        ch = safe_choice("Выберите пункт: ", {0, 1, 2, 3, 4})
        if ch == 0: return

        try:
            if ch == 1:
                coords = input("Введите координаты через пробел (x y или x y z): ").split()
                v = [float(c) for c in coords]
                length = math.sqrt(sum(x**2 for x in v))
                print(f"Длина вектора |v| = {length:.8g}")
                history.add("Длина вектора", f"{v} -> {length:.8g}")

            elif ch == 2:
                v1 = [float(x) for x in input("Вектор 1 (через пробел): ").split()]
                v2 = [float(x) for x in input("Вектор 2 (через пробел): ").split()]
                if len(v1) != len(v2):
                    print("Ошибка: векторы должны быть одинаковой размерности.")
                else:
                    dot = sum(a * b for a, b in zip(v1, v2))
                    print(f"Скалярное произведение = {dot:.8g}")
                    history.add("Скалярное произведение", f"{v1} * {v2} = {dot:.8g}")

            elif ch == 3:
                print("Матрица:\n[a b]\n[c d]")
                a, b = map(float, input("Строка 1 (a b): ").split())
                c, d = map(float, input("Строка 2 (c d): ").split())
                det = a*d - b*c
                print(f"Определитель (Det) = {det:.8g}")
                history.add("Det 2x2", f"Det = {det:.8g}")

            elif ch == 4:
                print("Вводите по 3 числа через пробел для каждой строки.")
                m = []
                for i in range(3):
                    m.append(list(map(float, input(f"Строка {i+1}: ").split())))
                det = (m[0][0]*(m[1][1]*m[2][2] - m[1][2]*m[2][1]) -
                       m[0][1]*(m[1][0]*m[2][2] - m[1][2]*m[2][0]) +
                       m[0][2]*(m[1][0]*m[2][1] - m[1][1]*m[2][0]))
                print(f"Определитель (Det) = {det:.8g}")
                history.add("Det 3x3", f"Det = {det:.8g}")
        except Exception as e:
            print(f"Ошибка ввода/вычислений: {e}")
        pause()

# ==========================================
# МОДУЛЬ 4: ФИНАНСОВЫЙ КАЛЬКУЛЯТОР
# ==========================================

def financial_menu(history: History) -> None:
    while True:
        clear_screen()
        print("\n--- ФИНАНСОВЫЙ КАЛЬКУЛЯТОР ---")
        print("1) Сложный процент (Депозит / Инвестиции)")
        print("2) Аннуитетный платеж (Кредит / Ипотека)")
        print("3) Расчет НДС")
        print("0) Назад")

        ch = safe_choice("Выберите пункт: ", {0, 1, 2, 3})
        if ch == 0: return

        try:
            if ch == 1:
                p = safe_float("Начальная сумма: ")
                r = safe_float("Годовая ставка (в %): ") / 100
                t = safe_float("Срок (в годах): ")
                n = safe_int("Кол-во капитализаций в год (12 для ежемесячной): ")
                a = p * (1 + r/n)**(n*t)
                profit = a - p
                print(f"\nИтоговая сумма: {a:.2f}")
                print(f"Чистая прибыль: {profit:.2f}")
                history.add("Сложный процент", f"Сумма={a:.2f}, Прибыль={profit:.2f}")

            elif ch == 2:
                s = safe_float("Сумма кредита: ")
                r_annual = safe_float("Годовая ставка (в %): ")
                m = safe_int("Срок кредита (в месяцах): ")
                r_month = (r_annual / 100) / 12
                if r_month == 0:
                    payment = s / m
                else:
                    payment = s * (r_month * (1 + r_month)**m) / ((1 + r_month)**m - 1)
                total = payment * m
                overpay = total - s
                print(f"\nЕжемесячный платеж: {payment:.2f}")
                print(f"Общая сумма выплат: {total:.2f}")
                print(f"Переплата: {overpay:.2f}")
                history.add("Аннуитет", f"Платеж={payment:.2f}, Переплата={overpay:.2f}")

            elif ch == 3:
                amount = safe_float("Сумма: ")
                rate = safe_float("Ставка НДС (в %): ")
                print("1 - Выделить НДС из суммы")
                print("2 - Начислить НДС на сумму")
                mode = safe_choice("Выбор: ", {1, 2})
                if mode == 1:
                    tax = amount * rate / (100 + rate)
                    net = amount - tax
                    print(f"Сумма без НДС: {net:.2f}, Сам НДС: {tax:.2f}")
                else:
                    tax = amount * (rate / 100)
                    total = amount + tax
                    print(f"Сумма с НДС: {total:.2f}, Сам НДС: {tax:.2f}")
        except Exception as e:
            print(f"Ошибка: {e}")
        pause()

# ==========================================
# ДОПОЛНИТЕЛЬНЫЕ И СИСТЕМНЫЕ РЕЖИМЫ
# ==========================================

def plot_function(expression: str) -> None:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("Библиотека matplotlib не установлена. Для графиков выполните: pip install matplotlib")
        return

    env = get_math_env()
    try:
        xs = [i / 20.0 for i in range(-200, 201)]
        ys = []
        for x in xs:
            env["x"] = x
            y = eval(expression, {"__builtins__": {}}, env)
            ys.append(float(y))

        plt.style.use('dark_background')
        plt.figure(figsize=(10, 6))
        plt.plot(xs, ys, color="#00ffcc", linewidth=2, label=f"y = {expression}")
        plt.grid(True, color="#333333", linestyle='--')
        plt.axhline(0, color="white", linewidth=1.5)
        plt.axvline(0, color="white", linewidth=1.5)
        plt.legend()
        plt.title(f"Kronos Ultra Графики: {expression}", fontsize=14)
        plt.xlabel("Ось X")
        plt.ylabel("Ось Y")
        plt.show()
    except Exception as e:
        print(f"Ошибка при построении графика: {e}")

def formula_menu(history: History) -> None:
    while True:
        clear_screen()
        print("\n--- СПРАВОЧНИК ФОРМУЛ ---")
        print("1) Квадратное уравнение (ax^2 + bx + c = 0)")
        print("2) Геометрия (Круг, Сфера, Цилиндр)")
        print("3) Теорема Пифагора")
        print("4) Физика: Кинематика и Энергия")
        print("5) Физика: Закон Ома")
        print("0) Назад")

        ch = safe_choice("Выберите пункт: ", set(range(0, 6)))
        if ch == 0: return

        try:
            if ch == 1:
                a = safe_float("a: ")
                b = safe_float("b: ")
                c = safe_float("c: ")
                d = b**2 - 4*a*c
                if d < 0:
                    print(f"D = {d} < 0. Корней в действительных числах нет.")
                else:
                    x1 = (-b + math.sqrt(d)) / (2*a)
                    x2 = (-b - math.sqrt(d)) / (2*a)
                    print(f"D = {d}, x1 = {x1:.6g}, x2 = {x2:.6g}")
                    history.add("Квадратное ур-ние", f"x1={x1:.6g}, x2={x2:.6g}")
            elif ch == 3:
                print("1 - Найти гипотенузу (c)\n2 - Найти катет (a/b)")
                sub = safe_choice("Выбор: ", {1, 2})
                if sub == 1:
                    a = safe_float("Катет a: ")
                    b = safe_float("Катет b: ")
                    c = math.hypot(a, b)
                    print(f"Гипотенуза c = {c:.6g}")
                else:
                    c = safe_float("Гипотенуза c: ")
                    a = safe_float("Известный катет: ")
                    if c <= a: print("Гипотенуза должна быть больше катета!")
                    else:
                        b = math.sqrt(c**2 - a**2)
                        print(f"Неизвестный катет = {b:.6g}")
            else:
                print("Модуль расширяется. Используйте классические вычисления для остальных формул.")
        except Exception as e:
            print(f"Ошибка: {e}")
        pause()

def statistics_menu(history: History) -> None:
    while True:
        clear_screen()
        print("\n--- СТАТИСТИКА И АНАЛИЗ ДАННЫХ ---")
        print("Введите числа через пробел (0 для выхода)")
        
        line = input("Данные: ").strip()
        if line == "0" or not line: return
        
        try:
            nums = [float(x) for x in line.split()]
            n = len(nums)
            nums.sort()
            
            mean = sum(nums) / n
            median = nums[n//2] if n % 2 != 0 else (nums[n//2 - 1] + nums[n//2]) / 2
            variance = sum((x - mean)**2 for x in nums) / n
            std_dev = math.sqrt(variance)
            
            print(f"\nКоличество элементов (N): {n}")
            print(f"Минимум: {nums[0]:.6g} | Максимум: {nums[-1]:.6g}")
            print(f"Сумма: {sum(nums):.6g}")
            print(f"Среднее арифметическое: {mean:.6g}")
            print(f"Медиана: {median:.6g}")
            print(f"Дисперсия (генеральная): {variance:.6g}")
            print(f"Стандартное отклонение: {std_dev:.6g}")
            
            history.add("Статистика", f"Среднее={mean:.6g}, Откл={std_dev:.6g}")
        except Exception as e:
            print(f"Ошибка обработки данных: {e}")
        pause()

def unit_converter_menu(history: History) -> None:
    cats = {
        1: ("Длина", {"m": 1, "km": 1000, "cm": 0.01, "mm": 0.001, "mile": 1609.34, "inch": 0.0254}),
        2: ("Масса", {"kg": 1, "g": 0.001, "t": 1000, "lb": 0.453592, "oz": 0.0283495}),
        3: ("Скорость", {"m/s": 1, "km/h": 0.277778, "mph": 0.44704, "knot": 0.514444}),
    }
    
    while True:
        clear_screen()
        print("\n--- КОНВЕРТЕР ЕДИНИЦ ---")
        print("1) Длина  |  2) Масса  |  3) Скорость  |  4) Температура  |  0) Назад")
        ch = safe_choice("Выбор: ", {0, 1, 2, 3, 4})
        if ch == 0: return
        
        if ch == 4:
            val = safe_float("Введите градусы Цельсия: ")
            f = val * 9/5 + 32
            k = val + 273.15
            print(f"{val} °C = {f:.2f} °F = {k:.2f} K")
            history.add("Температура", f"{val}C -> {f}F")
            pause()
            continue

        cat_name, rates = cats[ch]
        keys = list(rates.keys())
        print(f"\nДоступные единицы ({cat_name}): {', '.join(keys)}")
        
        f_unit = input("Из какой единицы: ").strip()
        t_unit = input("В какую единицу: ").strip()
        
        if f_unit in rates and t_unit in rates:
            val = safe_float("Значение: ")
            base_val = val * rates[f_unit]
            res = base_val / rates[t_unit]
            print(f"\n{val} {f_unit} = {res:.6g} {t_unit}")
            history.add("Конвертер", f"{val}{f_unit} -> {res:.6g}{t_unit}")
        else:
            print("Ошибка: неверно указаны единицы измерения.")
        pause()

def programmer_mode(history: History) -> None:
    while True:
        clear_screen()
        print("\n--- РЕЖИМ ПРОГРАММИСТА ---")
        print("1) Перевод систем счисления (BIN/OCT/DEC/HEX)")
        print("2) Побитовые операции (AND, OR, XOR, NOT, SHIFT)")
        print("0) Назад")
        
        ch = safe_choice("Выберите: ", {0, 1, 2})
        if ch == 0: return
        
        try:
            if ch == 1:
                base_str = input("В какой системе вводите? (2, 8, 10, 16): ").strip()
                val_str = input("Введите число: ").strip()
                n = int(val_str, int(base_str))
                print(f"\nDEC: {n}")
                print(f"BIN: {bin(n)}")
                print(f"OCT: {oct(n)}")
                print(f"HEX: {hex(n).upper()}")
                history.add("СС перевод", f"{val_str}({base_str}) -> {n}(10)")
            elif ch == 2:
                print("Доступно: &, |, ^, ~, <<, >>")
                expr = input("Введите выражение (например: 15 & 7, ~10, 1 << 3): ").strip()
                res = eval(expr, {"__builtins__": {}}, {})
                print(f"Результат (DEC): {res}")
                print(f"Результат (BIN): {bin(res)}")
                history.add("Побитовая", f"{expr} = {res}")
        except Exception as e:
            print(f"Ошибка: {e}")
        pause()

def base_calculator(history: History) -> None:
    while True:
        clear_screen()
        print("\n--- БАЗОВЫЙ / НАУЧНЫЙ КАЛЬКУЛЯТОР ---")
        print("Поддержка: +, -, *, /, //, %, **, скобки.")
        print("Функции math: sin, cos, tan, sqrt, log, pi, e, factorial и др.")
        expr = input("\nВведите выражение (0 для выхода): ").strip()
        if expr == "0": return
        if not expr: continue

        try:
            res = safe_scientific_eval(expr)
            out = str(int(round(res))) if abs(res - round(res)) < 1e-12 else f"{res:.10g}"
            print(f"\nРезультат: = {out}")
            history.add("Калькулятор", f"{expr} = {out}")
        except Exception as e:
            print(f"\nОшибка: {e}")
        pause()

# ==========================================
# ГЛАВНЫЙ ЦИКЛ ПРОГРАММЫ
# ==========================================

def main() -> None:
    history = History()

    while True:
        clear_screen()
        banner()

        print("\n   [ ОСНОВНЫЕ ИНСТРУМЕНТЫ ]")
        print("   1. Калькулятор (Базовый + Научный)")
        print("   2. Построение графиков функций")
        
        print("\n   [ ВЫСШАЯ МАТЕМАТИКА И АНАЛИЗ ]")
        print("   3. Математический анализ (Производные и Интегралы)")
        print("   4. Векторы и Матрицы (Линейная алгебра)")
        print("   5. Теория чисел и Дроби")
        
        print("\n   [ ПРИКЛАДНЫЕ ИНСТРУМЕНТЫ ]")
        print("   6. Финансовый калькулятор")
        print("   7. Статистика и анализ данных")
        print("   8. Конвертер величин")
        print("   9. Справочник формул (Геометрия, Физика)")
        
        print("\n   [ IT & БЕЗОПАСНОСТЬ ]")
        print("   10. Режим программиста (Системы счисления, биты)")
        print("   11. Generator безопасных паролей")
        
        print("\n   [ СИСТЕМА ]")
        print("   12. История вычислений")
        print("   0. Выход")

        choice = safe_choice("\nВыберите модуль: ", set(range(0, 13)))

        if choice == 0:
            break
        elif choice == 1:
            base_calculator(history)
        elif choice == 2:
            clear_screen()
            print("\n--- ПОСТРОЕНИЕ ГРАФИКОВ ---")
            expr = input("Введите функцию y(x) (например: sin(x)*x): ").strip()
            if expr: plot_function(expr)
        elif choice == 3:
            calculus_menu(history)
        elif choice == 4:
            matrix_menu(history)
        elif choice == 5:
            number_theory_menu(history)
        elif choice == 6:
            financial_menu(history)
        elif choice == 7:
            statistics_menu(history)
        elif choice == 8:
            unit_converter_menu(history)
        elif choice == 9:
            formula_menu(history)
        elif choice == 10:
            programmer_mode(history)
        elif choice == 11:
            clear_screen()
            print("\n--- ГЕНЕРАТОР ПАРОЛЕЙ ---")
            length = safe_int("Длина пароля: ")
            if length > 0:
                chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+"
                pwd = "".join(secrets.choice(chars) for _ in range(length))
                print(f"\nВаш пароль: {pwd}")
                history.add("Пароль", f"Сгенерирован (длина {length})")
            pause()
        elif choice == 12:
            clear_screen()
            history.show()
            if input("\nОчистить историю? (y/n): ").strip().lower() == 'y':
                history.clear()
                print("История очищена.")
            pause()

if __name__ == "__main__":
    main()