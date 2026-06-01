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
# CORE & HELPER FUNCTIONS
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
            print("Error: please enter an integer.")

def safe_float(prompt: str) -> float:
    while True:
        try:
            s = input(prompt).replace(",", ".").strip()
            return float(s)
        except Exception:
            print("Error: please enter a number.")

def safe_choice(prompt: str, valid: set[int]) -> int:
    while True:
        n = safe_int(prompt)
        if n in valid:
            return n
        print(f"Error: valid options are: {sorted(valid)}")

def pause() -> None:
    try:
        input("\nPress Enter to continue...")
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
    print("   Kronos Calculator ULTRA by Kronos English (2026)")
    print("   Multifunctional calculator for advanced calculations, analysis & graphs.")
    print(f"   Date: {now}")
    print("=" * 60)

# ==========================================
# HISTORY SYSTEM
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
            print("History is empty.")
            return
        print("\n--- Calculation History ---")
        for item in self._items:
            print(item.format_line())
        print("----------------------------")

# ==========================================
# BASE EXPRESSION PARSER (RPN)
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
                raise ExpressionError("Invalid number format")
            tokens.append(("NUM", s))
            continue
        raise ExpressionError(f"Unknown symbol: {ch!r}")
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
            if not stack: raise ExpressionError("Mismatched parentheses")
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
        if stack[-1][0] == "PAREN": raise ExpressionError("Mismatched parentheses")
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
            if len(stack) < 2: raise ExpressionError("Insufficient operands")
            b, a = stack.pop(), stack.pop()
            if val == "+": stack.append(a + b)
            elif val == "-": stack.append(a - b)
            elif val == "*": stack.append(a * b)
            elif val == "/": stack.append(a / b)
            elif val == "//": stack.append(math.floor(a / b))
            elif val == "%": stack.append(a % b)
            elif val == "**": stack.append(a ** b)
    if len(stack) != 1: raise ExpressionError("Invalid expression structure")
    return stack[0]

def evaluate_base_expression(expr: str) -> float:
    return eval_rpn(to_rpn(tokenize(expr)))

# ==========================================
# SCIENTIFIC EVALUATOR & FUNCTIONS
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
        raise ValueError("Disallowed character detected.")

    result = eval(expression, {"__builtins__": {}}, env)
    return float(result)

# ==========================================
# MODULE 1: MATHEMATICAL ANALYSIS (CALCULUS)
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
        print("\n--- MATHEMATICAL ANALYSIS (CALCULUS) ---")
        print("1) Derivative of a function at a point (f'(x))")
        print("2) Definite integral (Trapezoidal rule)")
        print("0) Back")
        
        ch = safe_choice("Select an option: ", {0, 1, 2})
        if ch == 0: return
        
        try:
            expr = input("Enter a function f(x) (e.g., sin(x)*x**2): ").strip()
            
            if ch == 1:
                x_val = safe_float("Enter point x: ")
                res = numerical_derivative(expr, x_val)
                print(f"f'({x_val}) ≈ {res:.8g}")
                history.add("Derivative", f"d/dx ({expr}) at x={x_val} ≈ {res:.8g}")
            
            elif ch == 2:
                a = safe_float("Lower limit (a): ")
                b = safe_float("Upper limit (b): ")
                res = numerical_integral(expr, a, b)
                print(f"∫ from {a} to {b} ({expr}) dx ≈ {res:.8g}")
                history.add("Integral", f"∫[{a},{b}] ({expr})dx ≈ {res:.8g}")
        except Exception as e:
            print(f"Calculation error: {e}")
        pause()

# ==========================================
# MODULE 2: NUMBER THEORY & FRACTIONS
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
        print("\n--- NUMBER THEORY & FRACTIONS ---")
        print("1) GCD and LCM of two numbers")
        print("2) Prime factorization")
        print("3) Primality test")
        print("4) Fraction calculator")
        print("0) Back")

        ch = safe_choice("Select an option: ", {0, 1, 2, 3, 4})
        if ch == 0: return
        
        try:
            if ch == 1:
                a = safe_int("Enter first number: ")
                b = safe_int("Enter second number: ")
                gcd = math.gcd(a, b)
                lcm = abs(a*b) // gcd if gcd else 0
                print(f"GCD({a}, {b}) = {gcd}")
                print(f"LCM({a}, {b}) = {lcm}")
                history.add("GCD/LCM", f"GCD({a},{b})={gcd}, LCM={lcm}")

            elif ch == 2:
                n = safe_int("Enter a natural number: ")
                if n < 2:
                    print("Factorization is defined for numbers >= 2")
                else:
                    factors = prime_factors(n)
                    res = " * ".join(map(str, factors))
                    print(f"{n} = {res}")
                    history.add("Factorization", f"{n} = {res}")

            elif ch == 3:
                n = safe_int("Enter a natural number: ")
                if n < 2:
                    print(f"{n} is not a prime number.")
                else:
                    factors = prime_factors(n)
                    if len(factors) == 1:
                        print(f"{n} is a PRIME number.")
                        history.add("Prime test?", f"{n} — Yes")
                    else:
                        print(f"{n} is a COMPOSITE number.")
                        history.add("Prime test?", f"{n} — No")

            elif ch == 4:
                print("Enter an expression with fractions (e.g., 1/2 + 1/3 or 5/8 * 2/3)")
                expr = input("Expression: ").strip()
                parts = expr.split()
                if len(parts) == 3:
                    f1 = Fraction(parts[0])
                    op = parts[1]
                    f2 = Fraction(parts[2])
                    if op == '+': res = f1 + f2
                    elif op == '-': res = f1 - f2
                    elif op == '*': res = f1 * f2
                    elif op == '/': res = f1 / f2
                    else: raise ValueError("Unknown operator")
                    print(f"Result: {res} (or {float(res):.6g})")
                    history.add("Fractions", f"{expr} = {res}")
                else:
                    print("Format: FRACTION OPERATOR FRACTION (separated by spaces).")
        except Exception as e:
            print(f"Error: {e}")
        pause()

# ==========================================
# MODULE 3: VECTORS & MATRICES
# ==========================================

def matrix_menu(history: History) -> None:
    while True:
        clear_screen()
        print("\n--- VECTORS & MATRICES ---")
        print("1) Vector length (2D / 3D)")
        print("2) Dot product of vectors")
        print("3) Determinant of a 2x2 matrix")
        print("4) Determinant of a 3x3 matrix")
        print("0) Back")

        ch = safe_choice("Select an option: ", {0, 1, 2, 3, 4})
        if ch == 0: return

        try:
            if ch == 1:
                coords = input("Enter components separated by spaces (x y or x y z): ").split()
                v = [float(c) for c in coords]
                length = math.sqrt(sum(x**2 for x in v))
                print(f"Vector length |v| = {length:.8g}")
                history.add("Vector length", f"{v} -> {length:.8g}")

            elif ch == 2:
                v1 = [float(x) for x in input("Vector 1 (space separated): ").split()]
                v2 = [float(x) for x in input("Vector 2 (space separated): ").split()]
                if len(v1) != len(v2):
                    print("Error: vectors must have the same dimension.")
                else:
                    dot = sum(a * b for a, b in zip(v1, v2))
                    print(f"Dot product = {dot:.8g}")
                    history.add("Dot product", f"{v1} * {v2} = {dot:.8g}")

            elif ch == 3:
                print("Matrix:\n[a b]\n[c d]")
                a, b = map(float, input("Row 1 (a b): ").split())
                c, d = map(float, input("Row 2 (c d): ").split())
                det = a*d - b*c
                print(f"Determinant (Det) = {det:.8g}")
                history.add("Det 2x2", f"Det = {det:.8g}")

            elif ch == 4:
                print("Enter 3 numbers separated by spaces for each row.")
                m = []
                for i in range(3):
                    m.append(list(map(float, input(f"Row {i+1}: ").split())))
                det = (m[0][0]*(m[1][1]*m[2][2] - m[1][2]*m[2][1]) -
                       m[0][1]*(m[1][0]*m[2][2] - m[1][2]*m[2][0]) +
                       m[0][2]*(m[1][0]*m[2][1] - m[1][1]*m[2][0]))
                print(f"Determinant (Det) = {det:.8g}")
                history.add("Det 3x3", f"Det = {det:.8g}")
        except Exception as e:
            print(f"Input/Calculation error: {e}")
        pause()

# ==========================================
# MODULE 4: FINANCIAL CALCULATOR
# ==========================================

def financial_menu(history: History) -> None:
    while True:
        clear_screen()
        print("\n--- FINANCIAL CALCULATOR ---")
        print("1) Compound interest (Deposit / Investments)")
        print("2) Annuity payment (Loan / Mortgage)")
        print("3) VAT (Value Added Tax) calculation")
        print("0) Back")

        ch = safe_choice("Select an option: ", {0, 1, 2, 3})
        if ch == 0: return

        try:
            if ch == 1:
                p = safe_float("Principal amount: ")
                r = safe_float("Annual interest rate (in %): ") / 100
                t = safe_float("Time period (in years): ")
                n = safe_int("Compounding periods per year (e.g., 12 for monthly): ")
                a = p * (1 + r/n)**(n*t)
                profit = a - p
                print(f"\nTotal balance: {a:.2f}")
                print(f"Total interest earned: {profit:.2f}")
                history.add("Compound interest", f"Balance={a:.2f}, Profit={profit:.2f}")

            elif ch == 2:
                s = safe_float("Loan amount: ")
                r_annual = safe_float("Annual interest rate (in %): ")
                m = safe_int("Loan term (in months): ")
                r_month = (r_annual / 100) / 12
                if r_month == 0:
                    payment = s / m
                else:
                    payment = s * (r_month * (1 + r_month)**m) / ((1 + r_month)**m - 1)
                total = payment * m
                overpay = total - s
                print(f"\nMonthly payment: {payment:.2f}")
                print(f"Total payment amount: {total:.2f}")
                print(f"Total interest overpayment: {overpay:.2f}")
                history.add("Annuity payment", f"Payment={payment:.2f}, Overpay={overpay:.2f}")

            elif ch == 3:
                amount = safe_float("Amount: ")
                rate = safe_float("VAT rate (in %): ")
                print("1 - Extract VAT from the total amount")
                print("2 - Apply VAT onto the amount")
                mode = safe_choice("Choice: ", {1, 2})
                if mode == 1:
                    tax = amount * rate / (100 + rate)
                    net = amount - tax
                    print(f"Net amount (excl. VAT): {net:.2f}, VAT amount: {tax:.2f}")
                else:
                    tax = amount * (rate / 100)
                    total = amount + tax
                    print(f"Total amount (incl. VAT): {total:.2f}, VAT amount: {tax:.2f}")
        except Exception as e:
            print(f"Error: {e}")
        pause()

# ==========================================
# ADDITIONAL & SYSTEM MODES
# ==========================================

def plot_function(expression: str) -> None:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("The matplotlib library is not installed. To plot graphs, run: pip install matplotlib")
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
        plt.title(f"Kronos Ultra Graphs: {expression}", fontsize=14)
        plt.xlabel("X Axis")
        plt.ylabel("Y Axis")
        plt.show()
    except Exception as e:
        print(f"Error plotting graph: {e}")

def formula_menu(history: History) -> None:
    while True:
        clear_screen()
        print("\n--- FORMULA REFERENCE BOOK ---")
        print("1) Quadratic equation (ax^2 + bx + c = 0)")
        print("2) Geometry (Circle, Sphere, Cylinder) [Coming soon]")
        print("3) Pythagorean theorem")
        print("4) Physics: Kinematics and Energy [Coming soon]")
        print("5) Physics: Ohm's law [Coming soon]")
        print("0) Back")

        ch = safe_choice("Select an option: ", set(range(0, 6)))
        if ch == 0: return

        try:
            if ch == 1:
                a = safe_float("Enter a: ")
                b = safe_float("Enter b: ")
                c = safe_float("Enter c: ")
                d = b**2 - 4*a*c
                if d < 0:
                    print(f"D = {d} < 0. No real roots exist.")
                else:
                    x1 = (-b + math.sqrt(d)) / (2*a)
                    x2 = (-b - math.sqrt(d)) / (2*a)
                    print(f"D = {d}, x1 = {x1:.6g}, x2 = {x2:.6g}")
                    history.add("Quadratic eq", f"x1={x1:.6g}, x2={x2:.6g}")
            elif ch == 3:
                print("1 - Find hypotenuse (c)\n2 - Find leg (a/b)")
                sub = safe_choice("Choice: ", {1, 2})
                if sub == 1:
                    a = safe_float("Enter side a: ")
                    b = safe_float("Enter side b: ")
                    c = math.hypot(a, b)
                    print(f"Hypotenuse c = {c:.6g}")
                else:
                    c = safe_float("Enter hypotenuse c: ")
                    a = safe_float("Enter known side: ")
                    if c <= a: print("Hypotenuse must be greater than the leg side!")
                    else:
                        b = math.sqrt(c**2 - a**2)
                        print(f"Unknown side leg = {b:.6g}")
            else:
                print("This module is expanding. Use the classic calculator for other formulas.")
        except Exception as e:
            print(f"Error: {e}")
        pause()

def statistics_menu(history: History) -> None:
    while True:
        clear_screen()
        print("\n--- STATISTICS & DATA ANALYSIS ---")
        print("Enter numbers separated by spaces (enter 0 to go back)")
        
        line = input("Data: ").strip()
        if line == "0" or not line: return
        
        try:
            nums = [float(x) for x in line.split()]
            n = len(nums)
            nums.sort()
            
            mean = sum(nums) / n
            median = nums[n//2] if n % 2 != 0 else (nums[n//2 - 1] + nums[n//2]) / 2
            variance = sum((x - mean)**2 for x in nums) / n
            std_dev = math.sqrt(variance)
            
            print(f"\nElement count (N): {n}")
            print(f"Minimum: {nums[0]:.6g} | Maximum: {nums[-1]:.6g}")
            print(f"Sum: {sum(nums):.6g}")
            print(f"Arithmetic mean: {mean:.6g}")
            print(f"Median: {median:.6g}")
            print(f"Variance (population): {variance:.6g}")
            print(f"Standard deviation: {std_dev:.6g}")
            
            history.add("Statistics", f"Mean={mean:.6g}, StdDev={std_dev:.6g}")
        except Exception as e:
            print(f"Data processing error: {e}")
        pause()

def unit_converter_menu(history: History) -> None:
    cats = {
        1: ("Length", {"m": 1, "km": 1000, "cm": 0.01, "mm": 0.001, "mile": 1609.34, "inch": 0.0254}),
        2: ("Mass", {"kg": 1, "g": 0.001, "t": 1000, "lb": 0.453592, "oz": 0.0283495}),
        3: ("Speed", {"m/s": 1, "km/h": 0.277778, "mph": 0.44704, "knot": 0.514444}),
    }
    
    while True:
        clear_screen()
        print("\n--- UNIT CONVERTER ---")
        print("1) Length  |  2) Mass  |  3) Speed  |  4) Temperature  |  0) Back")
        ch = safe_choice("Choice: ", {0, 1, 2, 3, 4})
        if ch == 0: return
        
        if ch == 4:
            val = safe_float("Enter temperature in Celsius: ")
            f = val * 9/5 + 32
            k = val + 273.15
            print(f"{val} °C = {f:.2f} °F = {k:.2f} K")
            history.add("Temperature", f"{val}C -> {f}F")
            pause()
            continue

        cat_name, rates = cats[ch]
        keys = list(rates.keys())
        print(f"\nAvailable units ({cat_name}): {', '.join(keys)}")
        
        f_unit = input("From unit: ").strip()
        t_unit = input("To unit: ").strip()
        
        if f_unit in rates and t_unit in rates:
            val = safe_float("Value: ")
            base_val = val * rates[f_unit]
            res = base_val / rates[t_unit]
            print(f"\n{val} {f_unit} = {res:.6g} {t_unit}")
            history.add("Unit Converter", f"{val}{f_unit} -> {res:.6g}{t_unit}")
        else:
            print("Error: Invalid units specified.")
        pause()

def programmer_mode(history: History) -> None:
    while True:
        clear_screen()
        print("\n--- PROGRAMMER MODE ---")
        print("1) Radix conversion (BIN/OCT/DEC/HEX)")
        print("2) Bitwise operations (AND, OR, XOR, NOT, SHIFT)")
        print("0) Back")
        
        ch = safe_choice("Select an option: ", {0, 1, 2})
        if ch == 0: return
        
        try:
            if ch == 1:
                base_str = input("Which base are you inputting? (2, 8, 10, 16): ").strip()
                val_str = input("Enter number: ").strip()
                n = int(val_str, int(base_str))
                print(f"\nDEC: {n}")
                print(f"BIN: {bin(n)}")
                print(f"OCT: {oct(n)}")
                print(f"HEX: {hex(n).upper()}")
                history.add("Base convert", f"{val_str}({base_str}) -> {n}(10)")
            elif ch == 2:
                print("Available operators: &, |, ^, ~, <<, >>")
                expr = input("Enter bitwise expression (e.g., 15 & 7, ~10, 1 << 3): ").strip()
                res = eval(expr, {"__builtins__": {}}, {})
                print(f"Result (DEC): {res}")
                print(f"Result (BIN): {bin(res)}")
                history.add("Bitwise op", f"{expr} = {res}")
        except Exception as e:
            print(f"Error: {e}")
        pause()

def base_calculator(history: History) -> None:
    while True:
        clear_screen()
        print("\n--- BASIC / SCIENTIFIC CALCULATOR ---")
        print("Supported: +, -, *, /, //, %, **, parentheses.")
        print("Math functions: sin, cos, tan, sqrt, log, pi, e, factorial, etc.")
        expr = input("\nEnter expression (0 to exit): ").strip()
        if expr == "0": return
        if not expr: continue

        try:
            res = safe_scientific_eval(expr)
            out = str(int(round(res))) if abs(res - round(res)) < 1e-12 else f"{res:.10g}"
            print(f"\nResult: = {out}")
            history.add("Calculator", f"{expr} = {out}")
        except Exception as e:
            print(f"\nError: {e}")
        pause()

# ==========================================
# MAIN ROUTINE LOOP
# ==========================================

def main() -> None:
    history = History()

    while True:
        clear_screen()
        banner()

        print("\n   [ MAIN TOOLS ]")
        print("   1. Calculator (Basic + Scientific)")
        print("   2. Plot Function Graphs")
        
        print("\n   [ ADVANCED MATHEMATICS & ANALYSIS ]")
        print("   3. Mathematical Analysis (Derivatives & Integrals)")
        print("   4. Vectors and Matrices (Linear Algebra)")
        print("   5. Number Theory and Fractions")
        
        print("\n   [ APPLIED UTILITIES ]")
        print("   6. Financial Calculator")
        print("   7. Statistics and Data Analysis")
        print("   8. Unit Converter")
        print("   9. Formula Reference Book (Geometry, Physics)")
        
        print("\n   [ IT & SECURITY ]")
        print("   10. Programmer Mode (Number Systems, Bitwise)")
        print("   11. Secure Password Generator")
        
        print("\n   [ SYSTEM ]")
        print("   12. Calculation History")
        print("   0. Exit")

        choice = safe_choice("\nSelect a module: ", set(range(0, 13)))

        if choice == 0:
            break
        elif choice == 1:
            base_calculator(history)
        elif choice == 2:
            clear_screen()
            print("\n--- PLOT GRAPHS ---")
            expr = input("Enter function y(x) (e.g., sin(x)*x): ").strip()
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
            print("\n--- SECURE PASSWORD GENERATOR ---")
            length = safe_int("Password length: ")
            if length > 0:
                chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+"
                pwd = "".join(secrets.choice(chars) for _ in range(length))
                print(f"\nYour password: {pwd}")
                history.add("Password", f"Generated (length {length})")
            pause()
        elif choice == 12:
            clear_screen()
            history.show()
            if input("\nClear calculation history? (y/n): ").strip().lower() == 'y':
                history.clear()
                print("History cleared.")
            pause()

if __name__ == "__main__":
    main()