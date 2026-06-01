# KRONOS CALCULATOR ULTRA v2.0 [ RUSSIFIED EDITION BY KRONOS RUSSIAN ]
from __future__ import annotations

import math
import os
import random
import secrets
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from fractions import Fraction
from typing import List, Tuple, Optional

# ЯДРО АНИМАЦИИ И СИСТЕМНЫЕ ФУНКЦИИ

def type_print(text: str, delay: float = 0.01, end: str = "\n") -> None:
    """Эффект посимвольного вывода текста в терминал."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(end)
    sys.stdout.flush()

def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")

def safe_int(prompt: str) -> int:
    while True:
        try:
            type_print(prompt, delay=0.01, end="")
            return int(input().strip())
        except ValueError:
            type_print("Ошибка: пожалуйста, введите целое число.", delay=0.01)

def safe_float(prompt: str) -> float:
    while True:
        try:
            type_print(prompt, delay=0.01, end="")
            return float(input().replace(",", ".").strip())
        except ValueError:
            type_print("Ошибка: пожалуйста, введите число.", delay=0.01)

def safe_choice(prompt: str, valid: set[int]) -> int:
    while True:
        n = safe_int(prompt)
        if n in valid:
            return n
        type_print(f"Ошибка: допустимые варианты: {sorted(valid)}", delay=0.01)

def pause() -> None:
    type_print("\nНажмите Enter для продолжения...", delay=0.01, end="")
    input()

def banner() -> None:
    now = datetime.now().strftime("%d.%m.%Y")
    # Построчный быстрый вывод логотипа для динамики
    lines = [
        "=" * 65,
        "   ██╗  ██╗██████╗  ██████╗ ███╗   ██╗██████╗ ███████╗",
        "   ██║ ██╔╝██╔══██╗██╔═══██╗████╗  ██║██╔══██╗██╔════╝",
        "   █████╔╝ ██████╔╝██║   ██║██╔██╗ ██║██║  ██║███████╗",
        "   ██╔═██╗ ██╔══██╗██║   ██║██║╚██╗██║██║  ██║╚════██║",
        "   ██║  ██╗██║  ██║╚██████╔╝██║ ╚████║██████╔╝███████║",
        "   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═════╝ ╚══════╝",
        "=" * 65
    ]
    for line in lines:
        print(line)
        time.sleep(0.02)
    
    type_print("  Kronos Calculator ULTRA v2.0 by Kronos Russian | Engine: Python 3.14", delay=0.008)
    type_print("  Многофункциональный аналитический и физико-математический хаб.", delay=0.005)
    type_print(f"  Сессия запущена: {now}", delay=0.008)
    print("=" * 65)

# СИСТЕМА ИСТОРИИ ВЫЧИСЛЕНИЙ

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
        now = datetime.now().strftime("%H:%M:%S")
        self._items.append(HistoryItem(timestamp=now, action=action, result=result))

    def show(self) -> None:
        if not self._items:
            type_print("История вычислений пуста.", delay=0.01)
            return
        type_print("\n--- ИСТОРИЯ ВЫЧИСЛЕНИЙ ---", delay=0.01)
        for item in self._items:
            type_print(item.format_line(), delay=0.005)
        print("-" * 30)

    def clear(self) -> None:
        self._items.clear()

# НАУЧНЫЙ ПАРСЕР И ДВИЖОК ОПЗ (RPN)

Token = Tuple[str, str]

def tokenize(expr: str) -> List[Token]:
    tokens: List[Token] = []
    i, n = 0, len(expr)
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
                if c.isdigit(): i += 1
                elif c == "." and not saw_dot:
                    saw_dot = True
                    i += 1
                else: break
            tokens.append(("NUM", expr[start:i]))
            continue
        raise ValueError(f"Неизвестный символ: {ch}")
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
            if not stack: raise ValueError("Несогласованные скобки")
            stack.pop()
        elif ttype == "OP":
            op = val
            if op == "-" and (prev_type is None or (prev_type == "PAREN" and prev_val == "(") or prev_type == "OP"):
                op = "u-"
            if op == "u-":
                prec = 5
                while stack and stack[-1][0] == "OP" and PRECEDENCE.get(stack[-1][1], (0, ""))[0] > prec:
                    output.append(stack.pop())
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
        if stack[-1][0] == "PAREN": raise ValueError("Несогласованные скобки")
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
            if len(stack) < 2: raise ValueError("Недостаточно операндов")
            b, a = stack.pop(), stack.pop()
            match val:
                case "+": stack.append(a + b)
                case "-": stack.append(a - b)
                case "*": stack.append(a * b)
                case "/": stack.append(a / b)
                case "//": stack.append(math.floor(a / b))
                case "%": stack.append(a % b)
                case "**": stack.append(a ** b)
    return stack[0]

def get_math_env() -> dict:
    env = {name: getattr(math, name) for name in dir(math) if not name.startswith("_")}
    env.update({'ln': math.log, 'log': math.log10, 'pi': math.pi, 'e': math.e})
    return env

def safe_scientific_eval(expression: str, extra_vars: dict | None = None) -> float:
    env = get_math_env()
    if extra_vars: env.update(extra_vars)
    allowed_chars = set("0123456789+-*/%()., _abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
    if any(ch not in allowed_chars for ch in expression):
        raise ValueError("Обнаружен недопустимый символ.")
    return float(eval(expression, {"__builtins__": {}}, env))

def base_calculator(history: History) -> None:
    while True:
        clear_screen()
        type_print("\n--- БАЗОВЫЙ И НАУЧНЫЙ КАЛЬКУЛЯТОР ---", delay=0.01)
        type_print("Поддерживает ОПЗ-парсинг и стандартные функции: sin, cos, sqrt, log, pi, e.", delay=0.005)
        type_print("Введите выражение (или 0 для выхода): ", delay=0.01, end="")
        expr = input().strip()
        if expr == "0": return
        if not expr: continue
        try:
            if any(func in expr for func in ["sin", "cos", "tan", "sqrt", "log", "ln", "pi", "e"]):
                res = safe_scientific_eval(expr)
            else:
                res = eval_rpn(to_rpn(tokenize(expr)))
            out = f"{int(res)}" if res.is_integer() else f"{res:.10g}"
            type_print(f"\nРезультат: {out}", delay=0.01)
            history.add("Калькулятор", f"{expr} = {out}")
        except Exception as e:
            type_print(f"\nОшибка синтаксиса: {e}", delay=0.01)
        pause()

# МОДУЛЬ 1: МАТЕМАТИЧЕСКИЙ АНАЛИЗ (CALCULUS)

def calculus_menu(history: History) -> None:
    while True:
        clear_screen()
        type_print("\n--- МАТЕМАТИЧЕСКИЙ АНАЛИЗ ---", delay=0.01)
        type_print("1) Производная функции в точке (f'(x))", delay=0.005)
        type_print("2) Определенный интеграл (Высокоточный метод Симпсона)", delay=0.005)
        type_print("0) Назад", delay=0.005)
        
        match safe_choice("Выберите пункт: ", {0, 1, 2}):
            case 0: return
            case 1:
                type_print("Функция f(x) (например: sin(x)*x**2): ", delay=0.01, end="")
                expr = input().strip()
                x_val = safe_float("Точка x: ")
                h = 1e-5
                try:
                    res = (safe_scientific_eval(expr, {"x": x_val + h}) - safe_scientific_eval(expr, {"x": x_val - h})) / (2 * h)
                    type_print(f"f'({x_val}) ≈ {res:.8g}", delay=0.01)
                    history.add("Производная", f"d/dx ({expr}) |x={x_val} ≈ {res:.8g}")
                except Exception as e: type_print(f"Ошибка: {e}", delay=0.01)
            case 2:
                type_print("Функция f(x): ", delay=0.01, end="")
                expr = input().strip()
                a, b = safe_float("Нижний предел (a): "), safe_float("Верхний предел (b): ")
                n = 10000
                h = (b - a) / n
                try:
                    s = safe_scientific_eval(expr, {"x": a}) + safe_scientific_eval(expr, {"x": b})
                    for i in range(1, n, 2): s += 4 * safe_scientific_eval(expr, {"x": a + i * h})
                    for i in range(2, n-1, 2): s += 2 * safe_scientific_eval(expr, {"x": a + i * h})
                    res = s * h / 3
                    type_print(f"∫ от {a} до {b} dx ≈ {res:.8g}", delay=0.01)
                    history.add("Интеграл", f"∫[{a},{b}] ({expr})dx ≈ {res:.8g}")
                except Exception as e: type_print(f"Ошибка: {e}", delay=0.01)
        pause()

# МОДУЛЬ 2: РАСШИРЕННАЯ АЛГЕБРА

def algebra_menu(history: History) -> None:
    while True:
        clear_screen()
        type_print("\n--- АЛГЕБРА, ВЕКТОРЫ И МАТРИЦЫ ---", delay=0.01)
        type_print("1) Квадратное уравнение (ax^2 + bx + c = 0)", delay=0.005)
        type_print("2) Решение СЛАУ 2x2 (Метод Крамера)", delay=0.005)
        type_print("3) Операции с векторами (Длина и Скалярное произведение)", delay=0.005)
        type_print("4) Определитель матрицы 3x3", delay=0.005)
        type_print("0) Назад", delay=0.005)

        match safe_choice("Выберите пункт: ", {0, 1, 2, 3, 4}):
            case 0: return
            case 1:
                a, b, c = safe_float("a: "), safe_float("b: "), safe_float("c: ")
                if a == 0:
                    type_print("Ошибка: это линейное уравнение, так как a=0!", delay=0.01)
                else:
                    d = b**2 - 4*a*c
                    if d < 0:
                        real = -b / (2*a)
                        imag = math.sqrt(abs(d)) / (2*a)
                        type_print(f"D = {d} < 0. Комплексные корни:\nx1 = {real:.4g} + {imag:.4g}i\nx2 = {real:.4g} - {imag:.4g}i", delay=0.01)
                    else:
                        x1 = (-b + math.sqrt(d)) / (2*a)
                        x2 = (-b - math.sqrt(d)) / (2*a)
                        type_print(f"D = {d}\nx1 = {x1:.6g}\nx2 = {x2:.6g}", delay=0.01)
                        history.add("Квадратное ур-ние", f"x1={x1:.4g}, x2={x2:.4g}")
            case 2:
                type_print("Система вида:\na1*x + b1*y = c1\na2*x + b2*y = c2", delay=0.005)
                type_print("Введите через пробел (a1 b1 c1): ", delay=0.01, end="")
                a1, b1, c1 = map(float, input().split())
                type_print("Введите через пробел (a2 b2 c2): ", delay=0.01, end="")
                a2, b2, c2 = map(float, input().split())
                det = a1*b2 - a2*b1
                if det == 0:
                    type_print("Определитель равен 0. Система не имеет однозначных решений.", delay=0.01)
                else:
                    x = (c1*b2 - c2*b1) / det
                    y = (a1*c2 - a2*c1) / det
                    type_print(f"Решение: x = {x:.6g}, y = {y:.6g}", delay=0.01)
                    history.add("СЛАУ 2x2", f"x={x:.4g}, y={y:.4g}")
            case 3:
                type_print("Введите координаты Вектора 1 через пробел: ", delay=0.01, end="")
                v1 = [float(x) for x in input().split()]
                type_print("Введите координаты Вектора 2 через пробел (или 0): ", delay=0.01, end="")
                v2 = [float(x) for x in input().split()]
                len_v1 = math.sqrt(sum(x**2 for x in v1))
                type_print(f"Длина Вектора 1: {len_v1:.6g}", delay=0.01)
                if len(v1) == len(v2) and v2 != [0.0]:
                    dot = sum(a * b for a, b in zip(v1, v2))
                    type_print(f"Скалярное произведение: {dot:.6g}", delay=0.01)
            case 4:
                type_print("Вводите по 3 числа через пробел для каждой строки матрицы 3x3:", delay=0.01)
                m = []
                for i in range(3):
                    type_print(f"Строка {i+1}: ", delay=0.01, end="")
                    m.append(list(map(float, input().split())))
                det = (m[0][0]*(m[1][1]*m[2][2] - m[1][2]*m[2][1]) -
                       m[0][1]*(m[1][0]*m[2][2] - m[1][2]*m[2][0]) +
                       m[0][2]*(m[1][0]*m[2][1] - m[1][1]*m[2][0]))
                type_print(f"Определитель (Det) = {det:.8g}", delay=0.01)
        pause()

# МОДУЛЬ 3: ГЕОМЕТРИЯ (2D И 3D)

def geometry_menu(history: History) -> None:
    while True:
        clear_screen()
        type_print("\n--- ГЕОМЕТРИЯ И ОБЪЕМЫ ---", delay=0.01)
        type_print("1) Треугольник (Пифагор и Площадь Герона)", delay=0.005)
        type_print("2) Круг (Площадь и Длина окружности)", delay=0.005)
        type_print("3) 3D Тела (Объемы Сферы, Цилиндра, Конуса)", delay=0.005)
        type_print("0) Назад", delay=0.005)

        match safe_choice("Выберите: ", {0, 1, 2, 3}):
            case 0: return
            case 1:
                type_print("1 - Найти сторону (Теорема Пифагора) | 2 - Площадь по формуле Герона", delay=0.005)
                if safe_choice("Выбор: ", {1, 2}) == 1:
                    type_print("Оставьте неизвестную сторону равной 0", delay=0.005)
                    a, b, c = safe_float("Катет a: "), safe_float("Катет b: "), safe_float("Гипотенуза c: ")
                    if c == 0: type_print(f"Гипотенуза c = {math.hypot(a, b):.6g}", delay=0.01)
                    elif a == 0: type_print(f"Катет a = {math.sqrt(c**2 - b**2):.6g}", delay=0.01)
                    elif b == 0: type_print(f"Катет b = {math.sqrt(c**2 - a**2):.6g}", delay=0.01)
                else:
                    a, b, c = safe_float("Сторона a: "), safe_float("Сторона b: "), safe_float("Сторона c: ")
                    p = (a + b + c) / 2
                    s = math.sqrt(p * (p - a) * (p - b) * (p - c))
                    type_print(f"Площадь по Герону S = {s:.6g}", delay=0.01)
            case 2:
                r = safe_float("Радиус R: ")
                type_print(f"Площадь S = {math.pi * r**2:.6g}\nДлина окружности C = {2 * math.pi * r:.6g}", delay=0.01)
            case 3:
                type_print("1 - Сфера | 2 - Цилиндр | 3 - Конус", delay=0.005)
                fig = safe_choice("Фигура: ", {1, 2, 3})
                r = safe_float("Радиус R: ")
                match fig:
                    case 1: type_print(f"Объем Сферы V = {(4/3) * math.pi * r**3:.6g}", delay=0.01)
                    case _:
                        h = safe_float("Высота H: ")
                        coef = 1.0 if fig == 2 else (1/3)
                        name = "Цилиндра" if fig == 2 else "Конуса"
                        type_print(f"Объем {name} V = {coef * math.pi * r**2 * h:.6g}", delay=0.01)
        pause()

# МОДУЛЬ 4: ПРИКЛАДНАЯ ФИЗИКА

def physics_menu(history: History) -> None:
    while True:
        clear_screen()
        type_print("\n--- ФИЗИЧЕСКИЙ МОДУЛЬ ---", delay=0.01)
        type_print("1) Кинематика (Равноускоренное движение, путь, скорость)", delay=0.005)
        type_print("2) Динамика и Энергия (Сила тяжести, Ek, Ep)", delay=0.005)
        type_print("3) Электродинамика (Закон Ома и Мощность тока)", delay=0.005)
        type_print("0) Назад", delay=0.005)

        match safe_choice("Выберите: ", {0, 1, 2, 3}):
            case 0: return
            case 1:
                v0 = safe_float("Начальная скорость v0 (м/с): ")
                t = safe_float("Время движения t (с): ")
                a = safe_float("Ускорение a (м/с²): ")
                s = v0 * t + 0.5 * a * t**2
                v = v0 + a * t
                type_print(f"Пройденный путь S = {s:.5g} м\nКонечная скорость V = {v:.5g} м/с", delay=0.01)
            case 2:
                m = safe_float("Масса тела m (кг): ")
                v = safe_float("Скорость v (м/с): ")
                h = safe_float("Высота h (м): ")
                g = 9.81
                type_print(f"Сила тяжести F = {m * g:.5g} Н\nКинетическая энергия Ek = {0.5 * m * v**2:.5g} Дж\nПотенциальная энергия Ep = {m * g * h:.5g} Дж", delay=0.01)
            case 3:
                type_print("Введите параметры электрической цепи. Неизвестный параметр укажите как 0.", delay=0.005)
                u = safe_float("Напряжение U (В): ")
                i = safe_float("Сила тока I (А): ")
                r = safe_float("Сопротивление R (Ом): ")
                if u == 0 and i > 0 and r > 0: u = i * r
                elif i == 0 and u > 0 and r > 0: i = u / r
                elif r == 0 and u > 0 and i > 0: r = u / i
                type_print(f"U = {u:.4g} В | I = {i:.4g} А | R = {r:.4g} Ом\nМощность тока P = {u * i:.5g} Вт", delay=0.01)
        pause()

# МОДУЛЬ 5: ПРОДВИНУТЫЕ ФИНАНСЫ

def financial_menu(history: History) -> None:
    while True:
        clear_screen()
        type_print("\n--- ФИНАНСЫ И ИНВЕСТИЦИОННЫЙ АНАЛИЗ ---", delay=0.01)
        type_print("1) Сложный процент (Депозиты с капитализацией)", delay=0.005)
        type_print("2) Аннуитетный платеж (Кредитный калькулятор)", delay=0.005)
        type_print("3) Расчет коэффициента ROI (Окупаемость инвестиций)", delay=0.005)
        type_print("4) Расчет НДС (Выделение / Начисление)", delay=0.005)
        type_print("0) Назад", delay=0.005)

        match safe_choice("Выберите: ", {0, 1, 2, 3, 4}):
            case 0: return
            case 1:
                p = safe_float("Начальный капитал P: ")
                r = safe_float("Годовая ставка (%): ") / 100
                t = safe_float("Срок размещения (лет): ")
                n = safe_int("Частота капитализации в год (12 - ежемесячно): ")
                a = p * (1 + r/n)**(n*t)
                type_print(f"Итоговый баланс: {a:.2f} | Чистая прибыль: {a - p:.2f}", delay=0.01)
            case 2:
                s = safe_float("Сумма займа: ")
                r_annual = safe_float("Годовая ставка (%): ")
                m = safe_int("Срок погашения (месяцев): ")
                r_m = (r_annual / 100) / 12
                pmt = s * (r_m * (1 + r_m)**m) / ((1 + r_m)**m - 1) if r_m > 0 else s / m
                type_print(f"Ежемесячный платеж: {pmt:.2f} | Общая переплата: {(pmt * m) - s:.2f}", delay=0.01)
            case 3:
                revenue = safe_float("Общий доход от проекта: ")
                cost = safe_float("Инвестиционные затраты: ")
                roi = ((revenue - cost) / cost) * 100
                type_print(f"Рентабельность вложений ROI = {roi:.2f}%", delay=0.01)
            case 4:
                amt = safe_float("Сумма денежных средств: ")
                rate = safe_float("Ставка налога НДС (%): ")
                type_print("1 - Выделить налог из суммы | 2 - Начислить налог поверх", delay=0.005)
                if safe_choice("Выбор: ", {1, 2}) == 1:
                    tax = amt * rate / (100 + rate)
                    type_print(f"Чистая сумма: {amt - tax:.2f} | НДС: {tax:.2f}", delay=0.01)
                else:
                    tax = amt * (rate / 100)
                    type_print(f"Итоговая сумма: {amt + tax:.2f} | НДС: {tax:.2f}", delay=0.01)
        pause()

# ДОПОЛНИТЕЛЬНЫЕ МОДУЛИ (ТЕОРИЯ ЧИСЕЛ, СТАТИСТИКА, IT)

def number_theory_menu(history: History) -> None:
    while True:
        clear_screen()
        type_print("\n--- ТЕОРИЯ ЧИСЕЛ И ДРОБИ ---", delay=0.01)
        type_print("1) НОД и НОК двух чисел\n2) Проверка на простое число\n3) Калькулятор обыкновенных дробей\n0) Назад", delay=0.005)
        match safe_choice("Выбор: ", {0, 1, 2, 3}):
            case 0: return
            case 1:
                a, b = safe_int("Число 1: "), safe_int("Число 2: ")
                gcd = math.gcd(a, b)
                lcm = abs(a * b) // gcd if gcd else 0
                type_print(f"НОД = {gcd} | НОК = {lcm}", delay=0.01)
            case 2:
                n = safe_int("Число: ")
                if n < 2: is_prime = False
                else: is_prime = all(n % i != 0 for i in range(2, int(math.isqrt(n)) + 1))
                type_print(f"Число {'ПРОСТОЕ' if is_prime else 'СОСТАВНОЕ'}", delay=0.01)
            case 3:
                type_print("Введите пример (формат: 1/2 + 2/3): ", delay=0.01, end="")
                expr = input().strip().split()
                try:
                    f1, op, f2 = Fraction(expr[0]), expr[1], Fraction(expr[2])
                    match op:
                        case "+": res = f1 + f2
                        case "-": res = f1 - f2
                        case "*": res = f1 * f2
                        case "/": res = f1 / f2
                    type_print(f"Результат: {res} ({float(res):.6g})", delay=0.01)
                except Exception as e: type_print(f"Ошибка формата: {e}", delay=0.01)
        pause()

def statistics_menu(history: History) -> None:
    clear_screen()
    type_print("\n--- СТАТИСТИЧЕСКИЙ АНАЛИЗ ДАННЫХ ---", delay=0.01)
    type_print("Введите числовую выборку через пробел: ", delay=0.01, end="")
    try:
        nums = sorted([float(x) for x in input().split()])
        n = len(nums)
        mean = sum(nums) / n
        med = nums[n//2] if n % 2 != 0 else (nums[n//2 - 1] + nums[n//2]) / 2
        var = sum((x - mean)**2 for x in nums) / n
        type_print(f"\nЭлементов: {n}\nСреднее значение: {mean:.5g}\nМедиана выборки: {med:.5g}\nДисперсия: {var:.5g}\nСтандартное отклонение: {math.sqrt(var):.5g}", delay=0.01)
    except Exception as e: type_print(f"Ошибка: {e}", delay=0.01)
    pause()

def plot_function() -> None:
    clear_screen()
    type_print("\n--- ВИЗУАЛИЗАЦИЯ ГРАФИКОВ ---", delay=0.01)
    type_print("Введите математическую функцию y(x) (например: sin(x)*x): ", delay=0.01, end="")
    expression = input().strip()
    if not expression: return
    try:
        import matplotlib.pyplot as plt
        env = get_math_env()
        xs = [i / 20.0 for i in range(-200, 201)]
        ys = []
        for x in xs:
            env["x"] = x
            ys.append(float(eval(expression, {"__builtins__": {}}, env)))
        plt.style.use('dark_background')
        plt.figure(figsize=(9, 5))
        plt.plot(xs, ys, color="#00ffcc", linewidth=2, label=f"y = {expression}")
        plt.axhline(0, color="white", linewidth=1)
        plt.axvline(0, color="white", linewidth=1)
        plt.grid(True, color="#333333", linestyle="--")
        plt.legend()
        plt.title("Kronos Engine Graphics")
        type_print("Отрисовка интерактивного окна...", delay=0.01)
        plt.show()
    except ImportError:
        type_print("Ошибка: Модуль matplotlib не обнаружен. Выполните в консоли: pip install matplotlib", delay=0.01)
    except Exception as e:
        type_print(f"Ошибка рендеринга: {e}", delay=0.01)
    pause()

def programmer_mode(history: History) -> None:
    while True:
        clear_screen()
        type_print("\n--- РЕЖИМ ПРОГРАММИСТА (IT-МОДУЛЬ) ---", delay=0.01)
        type_print("1) Конвертер систем счисления (BIN/OCT/DEC/HEX)\n2) Побитовые бинарные операции\n0) Назад", delay=0.005)
        match safe_choice("Выбор: ", {0, 1, 2}):
            case 0: return
            case 1:
                base = safe_int("Основание системы счисления источника (2, 8, 10, 16): ")
                type_print("Введите число: ", delay=0.01, end="")
                val = input().strip()
                try:
                    n = int(val, base)
                    type_print(f"\nDEC: {n}\nBIN: {bin(n)}\nOCT: {oct(n)}\nHEX: {hex(n).upper()}", delay=0.005)
                except Exception as e: type_print(f"Ошибка парсинга: {e}", delay=0.01)
            case 2:
                type_print("Поддерживаются битовые операторы (&, |, ^, ~, <<, >>)\nВыражение (например: 12 & 7): ", delay=0.01, end="")
                try:
                    res = eval(input().strip(), {"__builtins__": {}}, {})
                    type_print(f"Результат (DEC): {res} | (BIN): {bin(res)}", delay=0.01)
                except Exception as e: type_print(f"Ошибка: {e}", delay=0.01)
        pause()

# ГЛАВНЫЙ ВХОДНОЙ ЦИКЛ СИСТЕМЫ

def main() -> None:
    history = History()
    while True:
        clear_screen()
        banner()
        
        menu = [
            "\n   [ МАТЕМАТИЧЕСКИЙ ХАБ ]",
            "   1. Базовый / Научный калькулятор (ОПЗ движок)",
            "   2. Высшая математика (Производные, Интегралы Симпсона)",
            "   3. Линейная алгебра (Квадратные уравнения, СЛАУ, Векторы)",
            "   4. Теория чисел и Обыкновенные дроби",
            "\n   [ АНАЛИТИКА И ПРИКЛАДНЫЕ НАУКИ ]",
            "   5. Прикладная физика (Кинематика, Энергия, Закон Ома)",
            "   6. Геометрия (Метрика плоскости и Объемы 3D-тел)",
            "   7. Финансовый анализ и Инвестиции (ROI, Депозиты, Кредиты)",
            "   8. Статистика и обработка числовых выборок",
            "   9. Визуализация и рендеринг графиков функций",
            "\n   [ IT-МОДУЛЬ И ИНСТРУМЕНТЫ ]",
            "   10. Режим программиста (Побитовые операции, Системы счисления)",
            "   11. Криптостойкий генератор паролей (secrets)",
            "   12. Просмотр системного лога истории вычислений",
            "   0. Завершить сессию терминала"
        ]
        
        for line in menu:
            type_print(line, delay=0.001) # Сверхбыстрый вывод меню

        match safe_choice("\nВыберите рабочий модуль: ", set(range(13))):
            case 0: 
                type_print("\n[ЗАВЕРШЕНИЕ РАБОТЫ] Сессия успешно закрыта. До встречи, Зуро!", delay=0.01)
                break
            case 1: base_calculator(history)
            case 2: calculus_menu(history)
            case 3: algebra_menu(history)
            case 4: number_theory_menu(history)
            case 5: physics_menu(history)
            case 6: geometry_menu(history)
            case 7: financial_menu(history)
            case 8: statistics_menu(history)
            case 9: plot_function()
            case 10: programmer_mode(history)
            case 11:
                clear_screen()
                type_print("\n--- ГЕНЕРАТОР БЕЗОПАСНЫХ ПАРОЛЕЙ ---", delay=0.01)
                length = safe_int("Задайте длину генерируемого пароля: ")
                if length > 0:
                    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+"
                    pwd = "".join(secrets.choice(chars) for _ in range(length))
                    type_print(f"\nВаш сгенерированный пароль: {pwd}", delay=0.01)
                    history.add("Пароль", f"Сгенерирован (длина {length})")
                pause()
            case 12:
                clear_screen()
                history.show()
                type_print("\nОчистить лог истории вычислений? (y/n): ", delay=0.01, end="")
                if input().strip().lower() == 'y':
                    history.clear()
                    type_print("Лог очищен.", delay=0.01)
                pause()

if __name__ == "__main__":
    main()