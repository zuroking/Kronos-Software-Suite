# KRONOS CALCULATOR ULTRA v2.0  [INTERNATIONAL VERSION BY KRONOS ENGLISH]
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

# ANIMATION CORE & SYSTEM UTILITIES

def type_print(text: str, delay: float = 0.01, end: str = "\n") -> None:
    """Creates a smooth character-by-character terminal printing effect."""
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
            type_print("Error: Please enter a valid integer.", delay=0.01)

def safe_float(prompt: str) -> float:
    while True:
        try:
            type_print(prompt, delay=0.01, end="")
            return float(input().replace(",", ".").strip())
        except ValueError:
            type_print("Error: Please enter a valid number.", delay=0.01)

def safe_choice(prompt: str, valid: set[int]) -> int:
    while True:
        n = safe_int(prompt)
        if n in valid:
            return n
        type_print(f"Error: Invalid option. Valid choices: {sorted(valid)}", delay=0.01)

def pause() -> None:
    type_print("\nPress Enter to continue...", delay=0.01, end="")
    input()

def banner() -> None:
    now = datetime.now().strftime("%Y-%m-%d")
    lines = [
        "=" * 90,
        "   ██╗  ██╗██████╗  ██████╗ ███╗   ██╗ ██████╗ ███████╗   ██╗   ██╗██╗     ███████╗ ██████╗  █████╗ ",
        "   ██║ ██╔╝██╔══██╗██╔═══██╗████╗  ██║██╔═══██╗██╔════╝   ██║   ██║██║     ╚══██╔══╝██╔══██╗██╔══██╗",
        "   █████╔╝ ██████╔╝██║   ██║██╔██╗ ██║██║   ██║███████╗   ██║   ██║██║        ██║   ██████╔╝███████║",
        "   ██╔═██╗ ██╔══██╗██║   ██║██║╚██╗██║██║   ██║╚════██║   ██║   ██║██║        ██║   ██╔══██╗██╔══██║",
        "   ██║  ██╗██║  ██║╚██████╔╝██║ ╚████║╚██████╔╝███████║   ╚██████╔╝███████╗   ██║   ██║  ██║██║  ██║",
        "   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚══════╝    ╚═════╝ ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝",
        "=" * 90
    ]
    for line in lines:
        print(line)
        time.sleep(0.02)
    
    type_print("   Kronos Calculator ULTRA v2.0 by Kronos English | Core Engine: Python 3.14", delay=0.008)
    type_print("   Multifunctional Analytical & Physico-Mathematical Hub.", delay=0.005)
    type_print(f"   Terminal Session Established: {now}", delay=0.008)
    print("=" * 65)

# SYSTEM LOG & HISTORY MANAGEMENT

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
            type_print("Calculation log is empty.", delay=0.01)
            return
        type_print("\n--- SYSTEM HISTORY LOG ---", delay=0.01)
        for item in self._items:
            type_print(item.format_line(), delay=0.005)
        print("-" * 30)

    def clear(self) -> None:
        self._items.clear()

# SCIENTIFIC PARSER & RPN ENGINE

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
        raise ValueError(f"Unknown symbol detected: {ch}")
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
            if not stack: raise ValueError("Mismatched parentheses")
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
        if stack[-1][0] == "PAREN": raise ValueError("Mismatched parentheses")
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
            if len(stack) < 2: raise ValueError("Insufficient operands")
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
        raise ValueError("Expression contains restricted characters.")
    return float(eval(expression, {"__builtins__": {}}, env))

def base_calculator(history: History) -> None:
    while True:
        clear_screen()
        type_print("\n--- STANDARD & SCIENTIFIC CALCULATOR ---", delay=0.01)
        type_print("Supports RPN engine parsing & native functions: sin, cos, sqrt, log, pi, e.", delay=0.005)
        type_print("Enter expression (or 0 to go back): ", delay=0.01, end="")
        expr = input().strip()
        if expr == "0": return
        if not expr: continue
        try:
            if any(func in expr for func in ["sin", "cos", "tan", "sqrt", "log", "ln", "pi", "e"]):
                res = safe_scientific_eval(expr)
            else:
                res = eval_rpn(to_rpn(tokenize(expr)))
            out = f"{int(res)}" if res.is_integer() else f"{res:.10g}"
            type_print(f"\nResult: {out}", delay=0.01)
            history.add("Calculator", f"{expr} = {out}")
        except Exception as e:
            type_print(f"\nSyntax Error: {e}", delay=0.01)
        pause()

# MODULE 1: CALCULUS ENGINE

def calculus_menu(history: History) -> None:
    while True:
        clear_screen()
        type_print("\n--- CALCULUS ENGINE ---", delay=0.01)
        type_print("1) Numerical Derivative at a given point (f'(x))", delay=0.005)
        type_print("2) Definite Integral (High-precision Simpson's Rule)", delay=0.005)
        type_print("0) Back", delay=0.005)
        
        match safe_choice("Select an option: ", {0, 1, 2}):
            case 0: return
            case 1:
                type_print("Function f(x) (e.g., sin(x)*x**2): ", delay=0.01, end="")
                expr = input().strip()
                x_val = safe_float("At evaluation point x: ")
                h = 1e-5
                try:
                    res = (safe_scientific_eval(expr, {"x": x_val + h}) - safe_scientific_eval(expr, {"x": x_val - h})) / (2 * h)
                    type_print(f"f'({x_val}) ≈ {res:.8g}", delay=0.01)
                    history.add("Derivative", f"d/dx ({expr}) at x={x_val} ≈ {res:.8g}")
                except Exception as e: type_print(f"Error: {e}", delay=0.01)
            case 2:
                type_print("Function f(x): ", delay=0.01, end="")
                expr = input().strip()
                a, b = safe_float("Lower bound limit (a): "), safe_float("Upper bound limit (b): ")
                n = 10000
                h = (b - a) / n
                try:
                    s = safe_scientific_eval(expr, {"x": a}) + safe_scientific_eval(expr, {"x": b})
                    for i in range(1, n, 2): s += 4 * safe_scientific_eval(expr, {"x": a + i * h})
                    for i in range(2, n-1, 2): s += 2 * safe_scientific_eval(expr, {"x": a + i * h})
                    res = s * h / 3
                    type_print(f"∫ from {a} to {b} dx ≈ {res:.8g}", delay=0.01)
                    history.add("Integral", f"∫[{a},{b}] ({expr})dx ≈ {res:.8g}")
                except Exception as e: type_print(f"Error: {e}", delay=0.01)
        pause()

# MODULE 2: ADVANCED ALGEBRA & VECTORS

def algebra_menu(history: History) -> None:
    while True:
        clear_screen()
        type_print("\n--- ALGEBRA, VECTORS & MATRICES ---", delay=0.01)
        type_print("1) Quadratic Equation Solver (ax^2 + bx + c = 0)", delay=0.005)
        type_print("2) Linear Systems 2x2 Solver (Cramer's Rule)", delay=0.005)
        type_print("3) Vector Arithmetic (Magnitude & Dot Product)", delay=0.005)
        type_print("4) Determinant calculation of a 3x3 Matrix", delay=0.005)
        type_print("0) Back", delay=0.005)

        match safe_choice("Select an option: ", {0, 1, 2, 3, 4}):
            case 0: return
            case 1:
                a, b, c = safe_float("Enter a: "), safe_float("Enter b: "), safe_float("Enter c: ")
                if a == 0:
                    type_print("Error: This is a linear equation because a = 0!", delay=0.01)
                else:
                    d = b**2 - 4*a*c
                    if d < 0:
                        real = -b / (2*a)
                        imag = math.sqrt(abs(d)) / (2*a)
                        type_print(f"D = {d} < 0. Complex roots found:\nx1 = {real:.4g} + {imag:.4g}i\nx2 = {real:.4g} - {imag:.4g}i", delay=0.01)
                    else:
                        x1 = (-b + math.sqrt(d)) / (2*a)
                        x2 = (-b - math.sqrt(d)) / (2*a)
                        type_print(f"D = {d}\nx1 = {x1:.6g}\nx2 = {x2:.6g}", delay=0.01)
                        history.add("Quadratic Eq", f"x1={x1:.4g}, x2={x2:.4g}")
            case 2:
                type_print("System Format:\na1*x + b1*y = c1\na2*x + b2*y = c2", delay=0.005)
                type_print("Enter values separated by space (a1 b1 c1): ", delay=0.01, end="")
                a1, b1, c1 = map(float, input().split())
                type_print("Enter values separated by space (a2 b2 c2): ", delay=0.01, end="")
                a2, b2, c2 = map(float, input().split())
                det = a1*b2 - a2*b1
                if det == 0:
                    type_print("Determinant is 0. System has no unique solutions.", delay=0.01)
                else:
                    x = (c1*b2 - c2*b1) / det
                    y = (a1*c2 - a2*c1) / det
                    type_print(f"Solutions: x = {x:.6g}, y = {y:.6g}", delay=0.01)
                    history.add("SLAU 2x2", f"x={x:.4g}, y={y:.4g}")
            case 3:
                type_print("Enter Vector 1 components separated by space: ", delay=0.01, end="")
                v1 = [float(x) for x in input().split()]
                type_print("Enter Vector 2 components separated by space (or 0): ", delay=0.01, end="")
                v2 = [float(x) for x in input().split()]
                len_v1 = math.sqrt(sum(x**2 for x in v1))
                type_print(f"Vector 1 Magnitude: {len_v1:.6g}", delay=0.01)
                if len(v1) == len(v2) and v2 != [0.0]:
                    dot = sum(a * b for a, b in zip(v1, v2))
                    type_print(f"Dot Product (v1 • v2): {dot:.6g}", delay=0.01)
            case 4:
                type_print("Enter 3 spaces-separated numbers for each matrix row:", delay=0.01)
                m = []
                for i in range(3):
                    type_print(f"Row {i+1}: ", delay=0.01, end="")
                    m.append(list(map(float, input().split())))
                det = (m[0][0]*(m[1][1]*m[2][2] - m[1][2]*m[2][1]) -
                       m[0][1]*(m[1][0]*m[2][2] - m[1][2]*m[2][0]) +
                       m[0][2]*(m[1][0]*m[2][1] - m[1][1]*m[2][0]))
                type_print(f"Matrix Determinant (Det) = {det:.8g}", delay=0.01)
        pause()

# MODULE 3: GEOMETRY & VOLUMES

def geometry_menu(history: History) -> None:
    while True:
        clear_screen()
        type_print("\n--- GEOMETRY & VOLUMETRICS ---", delay=0.01)
        type_print("1) Triangle Calculations (Pythagoras & Heron's Area)", delay=0.005)
        type_print("2) Circle Metrics (Area & Circumference)", delay=0.005)
        type_print("3) 3D Solids (Volume of Sphere, Cylinder, Cone)", delay=0.005)
        type_print("0) Back", delay=0.005)

        match safe_choice("Select choice: ", {0, 1, 2, 3}):
            case 0: return
            case 1:
                type_print("1 - Find side (Pythagoras) | 2 - Compute Area via Heron's Formula", delay=0.005)
                if safe_choice("Selection: ", {1, 2}) == 1:
                    type_print("Set the unknown length value to 0", delay=0.005)
                    a, b, c = safe_float("Side a: "), safe_float("Side b: "), safe_float("Hypotenuse c: ")
                    if c == 0: type_print(f"Hypotenuse c = {math.hypot(a, b):.6g}", delay=0.01)
                    elif a == 0: type_print(f"Side a = {math.sqrt(c**2 - b**2):.6g}", delay=0.01)
                    elif b == 0: type_print(f"Side b = {math.sqrt(c**2 - a**2):.6g}", delay=0.01)
                else:
                    a, b, c = safe_float("Side a: "), safe_float("Side b: "), safe_float("Side c: ")
                    p = (a + b + c) / 2
                    s = math.sqrt(p * (p - a) * (p - b) * (p - c))
                    type_print(f"Heron's Formula Area S = {s:.6g}", delay=0.01)
            case 2:
                r = safe_float("Radius R: ")
                type_print(f"Area S = {math.pi * r**2:.6g}\nCircumference C = {2 * math.pi * r:.6g}", delay=0.01)
            case 3:
                type_print("1 - Sphere | 2 - Cylinder | 3 - Cone", delay=0.005)
                fig = safe_choice("Solid type: ", {1, 2, 3})
                r = safe_float("Radius R: ")
                match fig:
                    case 1: type_print(f"Sphere Volume V = {(4/3) * math.pi * r**3:.6g}", delay=0.01)
                    case _:
                        h = safe_float("Height H: ")
                        coef = 1.0 if fig == 2 else (1/3)
                        name = "Cylinder" if fig == 2 else "Cone"
                        type_print(f"{name} Volume V = {coef * math.pi * r**2 * h:.6g}", delay=0.01)
        pause()

# MODULE 4: APPLIED PHYSICS

def physics_menu(history: History) -> None:
    while True:
        clear_screen()
        type_print("\n--- APPLIED PHYSICS COMPONENT ---", delay=0.01)
        type_print("1) Kinematics (Uniformly accelerated motion, displacement, velocity)", delay=0.005)
        type_print("2) Dynamics & Energy (Gravitational Force, Ek, Ep)", delay=0.005)
        type_print("3) Electrodynamics (Ohm's Law & Electric Power)", delay=0.005)
        type_print("0) Back", delay=0.005)

        match safe_choice("Select option: ", {0, 1, 2, 3}):
            case 0: return
            case 1:
                v0 = safe_float("Initial velocity v0 (m/s): ")
                t = safe_float("Time elapsed t (s): ")
                a = safe_float("Acceleration a (m/s²): ")
                s = v0 * t + 0.5 * a * t**2
                v = v0 + a * t
                type_print(f"Displacement S = {s:.5g} m\nFinal Velocity V = {v:.5g} m/s", delay=0.01)
            case 2:
                m = safe_float("Body mass m (kg): ")
                v = safe_float("Velocity v (m/s): ")
                h = safe_float("Height h (m): ")
                g = 9.81
                type_print(f"Gravity Force F = {m * g:.5g} N\nKinetic Energy Ek = {0.5 * m * v**2:.5g} J\nPotential Energy Ep = {m * g * h:.5g} J", delay=0.01)
            case 3:
                type_print("Enter electrical parameters. Set the unknown value to 0.", delay=0.005)
                u = safe_float("Voltage U (V): ")
                i = safe_float("Current I (A): ")
                r = safe_float("Resistance R (Ω): ")
                if u == 0 and i > 0 and r > 0: u = i * r
                elif i == 0 and u > 0 and r > 0: i = u / r
                elif r == 0 and u > 0 and i > 0: r = u / i
                type_print(f"U = {u:.4g} V | I = {i:.4g} A | R = {r:.4g} Ω\nTotal Circuit Power P = {u * i:.5g} W", delay=0.01)
        pause()

# MODULE 5: FINANCIAL ANALYTICS

def financial_menu(history: History) -> None:
    while True:
        clear_screen()
        type_print("\n--- FINANCIAL & INVESTMENT ANALYSIS ---", delay=0.01)
        type_print("1) Compound Interest (Principal compounding accumulation)", delay=0.005)
        type_print("2) Annuity Payment (Loan/Mortgage Calculator)", delay=0.005)
        type_print("3) Return on Investment Ratio (ROI analysis)", delay=0.005)
        type_print("4) VAT Calculation (Extraction / Allocation)", delay=0.005)
        type_print("0) Back", delay=0.005)

        match safe_choice("Select options: ", {0, 1, 2, 3, 4}):
            case 0: return
            case 1:
                p = safe_float("Initial Principal P: ")
                r = safe_float("Annual Interest Rate (%): ") / 100
                t = safe_float("Duration in Years (t): ")
                n = safe_int("Compounding frequency per year (12 = monthly): ")
                a = p * (1 + r/n)**(n*t)
                type_print(f"Ending Balance: {a:.2f} | Net Earnings Yield: {a - p:.2f}", delay=0.01)
            case 2:
                s = safe_float("Total Loan Amount: ")
                r_annual = safe_float("Annual Interest Rate (%): ")
                m = safe_int("Payback Period (months): ")
                r_m = (r_annual / 100) / 12
                pmt = s * (r_m * (1 + r_m)**m) / ((1 + r_m)**m - 1) if r_m > 0 else s / m
                type_print(f"Monthly Installment: {pmt:.2f} | Cumulative Overpayment: {(pmt * m) - s:.2f}", delay=0.01)
            case 3:
                revenue = safe_float("Gross Project Returns: ")
                cost = safe_float("Total Capital Venture Cost: ")
                roi = ((revenue - cost) / cost) * 100
                type_print(f"Investment Efficiency ROI = {roi:.2f}%", delay=0.01)
            case 4:
                amt = safe_float("Financial Gross Sum: ")
                rate = safe_float("Tax Rate VAT (%): ")
                type_print("1 - Deduct VAT from current sum | 2 - Surcharge VAT on top", delay=0.005)
                if safe_choice("Selection: ", {1, 2}) == 1:
                    tax = amt * rate / (100 + rate)
                    type_print(f"Net Amount: {amt - tax:.2f} | VAT Portion: {tax:.2f}", delay=0.01)
                else:
                    tax = amt * (rate / 100)
                    type_print(f"Gross Amount: {amt + tax:.2f} | VAT Surcharge: {tax:.2f}", delay=0.01)
        pause()

# MODULE 6: COMPLEMENTARY SCIENTIFIC UTILS

def number_theory_menu(history: History) -> None:
    while True:
        clear_screen()
        type_print("\n--- NUMBER THEORY & FRACTIONS ---", delay=0.01)
        type_print("1) GCD and LCM of two integers\n2) Primality Testing Algorithm\n3) Fraction Evaluator Core\n0) Back", delay=0.005)
        match safe_choice("Selection: ", {0, 1, 2, 3}):
            case 0: return
            case 1:
                a, b = safe_int("Integer 1: "), safe_int("Integer 2: ")
                gcd = math.gcd(a, b)
                lcm = abs(a * b) // gcd if gcd else 0
                type_print(f"GCD = {gcd} | LCM = {lcm}", delay=0.01)
            case 2:
                n = safe_int("Number to test: ")
                if n < 2: is_prime = False
                else: is_prime = all(n % i != 0 for i in range(2, int(math.isqrt(n)) + 1))
                type_print(f"The number is structurally: {'PRIME' if is_prime else 'COMPOSITE'}", delay=0.01)
            case 3:
                type_print("Enter expression (e.g., 1/2 + 2/3): ", delay=0.01, end="")
                expr = input().strip().split()
                try:
                    f1, op, f2 = Fraction(expr[0]), expr[1], Fraction(expr[2])
                    match op:
                        case "+": res = f1 + f2
                        case "-": res = f1 - f2
                        case "*": res = f1 * f2
                        case "/": res = f1 / f2
                    type_print(f"Resulting Fraction: {res} ({float(res):.6g})", delay=0.01)
                except Exception as e: type_print(f"Formatting parsing error: {e}", delay=0.01)
        pause()

def statistics_menu(history: History) -> None:
    clear_screen()
    type_print("\n--- NUMERICAL STATISTICAL ANALYSIS ---", delay=0.01)
    type_print("Enter numerical sample array separated by spaces: ", delay=0.01, end="")
    try:
        nums = sorted([float(x) for x in input().split()])
        n = len(nums)
        mean = sum(nums) / n
        med = nums[n//2] if n % 2 != 0 else (nums[n//2 - 1] + nums[n//2]) / 2
        var = sum((x - mean)**2 for x in nums) / n
        type_print(f"\nTotal Elements (n): {n}\nArithmetic Mean: {mean:.5g}\nMedian Value: {med:.5g}\nVariance: {var:.5g}\nStandard Deviation: {math.sqrt(var):.5g}", delay=0.01)
    except Exception as e: type_print(f"Statistical Core Error: {e}", delay=0.01)
    pause()

def plot_function() -> None:
    clear_screen()
    type_print("\n--- GRAPH REVOLUTION RENDERING ---", delay=0.01)
    type_print("Enter an equation function y(x) (e.g., sin(x)*x): ", delay=0.01, end="")
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
        plt.title("Kronos Functional Graphic Interface")
        type_print("Launching interactive canvas display...", delay=0.01)
        plt.show()
    except ImportError:
        type_print("Error: Missing 'matplotlib' dependency module. Run: pip install matplotlib", delay=0.01)
    except Exception as e:
        type_print(f"Rendering exception: {e}", delay=0.01)
    pause()

def programmer_mode(history: History) -> None:
    while True:
        clear_screen()
        type_print("\n--- ARCHITECT PROGRAMMER RADIX MODE ---", delay=0.01)
        type_print("1) Radix System Conversion Utility (BIN/OCT/DEC/HEX)\n2) Low-level Bitwise Logical operations\n0) Back", delay=0.005)
        match safe_choice("Selection: ", {0, 1, 2}):
            case 0: return
            case 1:
                base = safe_int("Select source numerical radix system (2, 8, 10, 16): ")
                type_print("Enter data value string: ", delay=0.01, end="")
                val = input().strip()
                try:
                    n = int(val, base)
                    type_print(f"\nDEC: {n}\nBIN: {bin(n)}\nOCT: {oct(n)}\nHEX: {hex(n).upper()}", delay=0.005)
                except Exception as e: type_print(f"Parsing evaluation fault: {e}", delay=0.01)
            case 2:
                type_print("Bitwise operators supported: (&, |, ^, ~, <<, >>)\nEnter operation (e.g., 12 & 7): ", delay=0.01, end="")
                try:
                    res = eval(input().strip(), {"__builtins__": {}}, {})
                    type_print(f"Decimal Output (DEC): {res} | Bitwise Matrix (BIN): {bin(res)}", delay=0.01)
                except Exception as e: type_print(f"Operator Error: {e}", delay=0.01)
        pause()

# MASTER PROGRAM INTEGRATED INTERRUPT LOOP

def main() -> None:
    history = History()
    while True:
        clear_screen()
        banner()
        
        menu = [
            "\n   [ MATHEMATICAL UTILITIES HUB ]",
            "   1. Standard / Scientific Calculator (Native RPN Engine)",
            "   2. Advanced Calculus Tools (Derivatives & Simpson's Integrals)",
            "   3. Linear Algebra Subsystems (Quadratics, System Equations, Vectors)",
            "   4. Number Theory Modules & Real Fraction Arithmetic",
            "\n   [ APPLIED ANALYTICS & INDUSTRIAL SCIENCES ]",
            "   5. Applied Physics Lab (Kinematics, Force, Ohm's Electrical Law)",
            "   6. Geometrical Metrics (Plane Calculations & 3D Volume Systems)",
            "   7. Macro Finance & Venture Investment Metrics (ROI, Yields, Loans)",
            "   8. Array Data Statistics & Empirical Matrix Distribution",
            "   9. Visual Graph Analytical Renderer (Matplotlib Interface)",
            "\n   [ INFRASTRUCTURE IT DEVELOPMENT MODS ]",
            "   10. Low-level Programming Toolkit (Bitwise Shifts, Radix Convert)",
            "   11. Cryptographically Secure Random Password Architect (secrets)",
            "   12. Diagnostics System History Event Logging",
            "   0. Close Active Terminal Session Connection"
        ]
        
        for line in menu:
            type_print(line, delay=0.001)

        match safe_choice("\nSelect active command module terminal code: ", set(range(13))):
            case 0: 
                type_print("\n[TERMINAL TERMINATION] Session successfully safely disconnected. Goodbye, Zuro!", delay=0.01)
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
                type_print("\n--- SECURE PASSKEY ARCHITECT ---", delay=0.01)
                length = safe_int("Determine security passcode length value parameter: ")
                if length > 0:
                    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+"
                    pwd = "".join(secrets.choice(chars) for _ in range(length))
                    type_print(f"\nGenerated Cryptographic Passkey token string: {pwd}", delay=0.01)
                    history.add("Passkey", f"Securely generated string (length {length})")
                pause()
            case 12:
                clear_screen()
                history.show()
                type_print("\nPurge diagnostic system history events cache? (y/n): ", delay=0.01, end="")
                if input().strip().lower() in ['y', 'yes']:
                    history.clear()
                    type_print("System log history cache successfully purged.", delay=0.01)
                pause()

if __name__ == "__main__":
    main()