# KRONOS CALCULATOR ULTRA V2.5
from __future__ import annotations

import os
import sys
import time
import json
import csv
import math
import cmath
import secrets
import hashlib
import base64
import re
import unittest
from dataclasses import dataclass, asdict
from datetime import datetime
from fractions import Fraction
from typing import List, Tuple, Dict, Any, Callable, TypeVar

T = TypeVar('T')

# TERMINAL ANSI COLOR PALETTE

class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    CYAN = "\033[1;36m"
    GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    RED = "\033[1;31m"
    MAGENTA = "\033[1;35m"
    GRAY = "\033[90m"

# SETTINGS AND DATA PERSISTENCE SYSTEM

class ConfigManager:
    CONFIG_FILE = "kronos_config.json"
    
    def __init__(self) -> None:
        self.settings: Dict[str, Any] = {
            "text_delay": 0.005,
            "plot_theme": "dark_background",
            "history_file": "kronos_history.json",
            "export_dir": "exports"
        }
        self.load_config()

    def load_config(self) -> None:
        if os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, "r", encoding="utf-8") as f:
                    self.settings.update(json.load(f))
            except Exception:
                pass

    def save_config(self) -> None:
        try:
            with open(self.CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"{Colors.RED}Configuration saving error: {e}{Colors.RESET}")


@dataclass
class HistoryItem:
    timestamp: str
    module: str
    action: str
    result: str

    def to_line(self) -> str:
        return f"[{Colors.GRAY}{self.timestamp}{Colors.RESET}] ({Colors.CYAN}{self.module}{Colors.RESET}) {self.action} -> {Colors.GREEN}{self.result}{Colors.RESET}"


class HistoryEngine:
    def __init__(self, filename: str, export_dir: str) -> None:
        self.filename = filename
        self.export_dir = export_dir
        self.items: List[HistoryItem] = []
        self.load_history()

    def add(self, module: str, action: str, result: str) -> None:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        item = HistoryItem(timestamp=now, module=module, action=action, result=result)
        self.items.append(item)
        self.save_history()

    def load_history(self) -> None:
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.items = [HistoryItem(**item) for item in data]
            except Exception:
                self.items = []

    def save_history(self) -> None:
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump([asdict(item) for item in self.items], f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"{Colors.RED}History saving error: {e}{Colors.RESET}")

    def clear(self) -> None:
        self.items.clear()
        if os.path.exists(self.filename):
            try:
                os.remove(self.filename)
            except Exception:
                pass

    def export_txt(self) -> str:
        os.makedirs(self.export_dir, exist_ok=True)
        path = os.path.join(self.export_dir, f"export_{int(time.time())}.txt")
        with open(path, "w", encoding="utf-8") as f:
            for item in self.items:
                clean_line = f"[{item.timestamp}] ({item.module}) {item.action} -> {item.result}\n"
                f.write(clean_line)
        return path

    def export_csv(self) -> str:
        os.makedirs(self.export_dir, exist_ok=True)
        path = os.path.join(self.export_dir, f"export_{int(time.time())}.csv")
        with open(path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "Module", "Action", "Result"])
            for item in self.items:
                writer.writerow([item.timestamp, item.module, item.action, item.result])
        return path

# TERMINAL INTERFACE AND UTILITIES

class TerminalUI:
    def __init__(self, config: ConfigManager) -> None:
        self.config = config

    def print_smart(self, text: str, end: str = "\n") -> None:
        delay = self.config.settings.get("text_delay", 0.005)
        if delay == 0:
            sys.stdout.write(text + end)
            sys.stdout.flush()
            return
        
        i = 0
        n = len(text)
        while i < n:
            if text[i] == "\033":
                j = i
                while j < n and text[j] != "m":
                    j += 1
                sys.stdout.write(text[i:j+1])
                i = j + 1
            else:
                sys.stdout.write(text[i])
                sys.stdout.flush()
                time.sleep(delay)
                i += 1
        sys.stdout.write(end)
        sys.stdout.flush()

    @staticmethod
    def clear() -> None:
        if os.name == "nt":
            os.system("cls")
            os.system("") 
        else:
            os.system("clear")

    def pause(self) -> None:
        self.print_smart(f"\n{Colors.GRAY}Press Enter to continue...{Colors.RESET}", end="")
        input()

    def get_input(self, prompt: str, parser_func: Callable[[str], T], validator: Callable[[T], bool] = lambda x: True, err_msg: str = "Invalid input.") -> T:
        while True:
            self.print_smart(prompt, end="")
            raw = input().strip()
            try:
                cleaned = raw.replace(",", ".") if parser_func in [float, complex] else raw
                value = parser_func(cleaned)  # type: ignore
                if validator(value):
                    return value
                self.print_smart(f"{Colors.RED}Error: {err_msg}{Colors.RESET}")
            except Exception:
                self.print_smart(f"{Colors.RED}Parsing error: {err_msg}{Colors.RESET}")

    def show_banner(self) -> None:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lines = [
            f"{Colors.CYAN}=====================================================================================================",
            f"{Colors.BOLD}{Colors.CYAN}   ██╗  ██╗██████╗  ██████╗ ███╗   ██╗ ██████╗ ███████╗   ██╗   ██╗██╗     ███████╗ ██████╗  █████╗ ",
            "   ██║ ██╔╝██╔══██╗██╔═══██╗████╗  ██║██╔═══██╗██╔════╝   ██║   ██║██║     ╚══██╔══╝██╔══██╗██╔══██╗",
            "   █████╔╝ ██████╔╝██║   ██║██╔██╗ ██║██║   ██║███████╗   ██║   ██║██║        ██║   ██████╔╝███████║",
            "   ██╔═██╗ ██╔══██╗██║   ██║██║╚██╗██║██║   ██║╚════██║   ██║   ██║██║        ██║   ██╔══██╗██╔══██║",
            "   ██║  ██╗██║  ██║╚██████╔╝██║ ╚████║╚██████╔╝███████║   ╚██████╔╝███████╗   ██║   ██║  ██║██║  ██║",
            f"   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚══════╝    ╚═════╝ ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝{Colors.RESET}",
            f"{Colors.CYAN}====================================================================================================={Colors.RESET}"
        ]
        for line in lines:
            print(line)
            time.sleep(0.01)
        self.print_smart(f"         {Colors.BOLD}{Colors.GREEN}Kronos Calculator ULTRA v2.5 by Kronos Russian{Colors.RESET} | {Colors.YELLOW}Mode:{Colors.RESET} Standard")
        self.print_smart(f"         {Colors.MAGENTA}Session time:{Colors.RESET} {now}")
        print(f"{Colors.CYAN}====================================================================================================={Colors.RESET}")

# MATHEMATICAL ENGINE WITH RPN PARSER

class MathEngine:
    OPERATORS = {
        "+": (2, "left", lambda a, b: a + b),
        "-": (2, "left", lambda a, b: a - b),
        "*": (3, "left", lambda a, b: a * b),
        "/": (3, "left", lambda a, b: a / b),
        "//": (3, "left", lambda a, b: float(a.real // b.real)),
        "%": (3, "left", lambda a, b: float(a.real % b.real)),
        "**": (4, "right", lambda a, b: a ** b),
        "u-": (5, "right", lambda a: -a)
    }

    FUNCTIONS = {
        "sin": lambda x: cmath.sin(x),
        "cos": lambda x: cmath.cos(x),
        "tan": lambda x: cmath.tan(x),
        "sqrt": lambda x: cmath.sqrt(x),
        "ln": lambda x: cmath.log(x),
        "log": lambda x: cmath.log10(x),
        "exp": lambda x: cmath.exp(x),
        "abs": lambda x: complex(abs(x))
    }

    CONSTANTS = {
        "pi": complex(math.pi),
        "e": complex(math.e),
        "i": complex(0, 1)
    }

    @classmethod
    def tokenize(cls, expr: str) -> List[Tuple[str, str]]:
        tokens: List[Tuple[str, str]] = []
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
                while i < n and (expr[i].isdigit() or (expr[i] == "." and not saw_dot)):
                    if expr[i] == ".":
                        saw_dot = True
                    i += 1
                if i < n and expr[i] == 'j':
                    tokens.append(("NUM", expr[start:i+1]))
                    i += 1
                else:
                    tokens.append(("NUM", expr[start:i]))
                continue
            if ch.isalpha():
                start = i
                while i < n and expr[i].isalpha():
                    i += 1
                name = expr[start:i]
                if name in cls.FUNCTIONS:
                    tokens.append(("FUNC", name))
                elif name in cls.CONSTANTS:
                    tokens.append(("NUM", name))
                else:
                    tokens.append(("VAR", name))
                continue
            raise ValueError(f"Invalid character: '{ch}'")
        return tokens

    @classmethod
    def to_rpn(cls, tokens: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
        output: List[Tuple[str, str]] = []
        stack: List[Tuple[str, str]] = []
        prev_type: str | None = None
        prev_val: str | None = None

        for tok_type, val in tokens:
            if tok_type in ("NUM", "VAR"):
                output.append((tok_type, val))
            elif tok_type == "FUNC":
                stack.append((tok_type, val))
            elif tok_type == "PAREN" and val == "(":
                stack.append((tok_type, val))
            elif tok_type == "PAREN" and val == ")":
                while stack and stack[-1][1] != "(":
                    output.append(stack.pop())
                if not stack:
                    raise ValueError("Mismatched parentheses.")
                stack.pop()
                if stack and stack[-1][0] == "FUNC":
                    output.append(stack.pop())
            elif tok_type == "OP":
                op = val
                if op == "-" and (prev_type is None or (prev_type == "PAREN" and prev_val == "(") or prev_type == "OP"):
                    op = "u-"
                
                if op == "u-":
                    prec = 5
                    while stack and stack[-1][0] == "OP" and cls.OPERATORS.get(stack[-1][1])[0] > prec:  # type: ignore
                        output.append(stack.pop())
                    stack.append(("OP", "u-"))
                else:
                    prec, assoc, _ = cls.OPERATORS[op]
                    while stack and stack[-1][0] == "OP":
                        top_op = stack[-1][1]
                        top_prec, top_assoc, _ = cls.OPERATORS[top_op]
                        if (assoc == "left" and prec <= top_prec) or (assoc == "right" and prec < top_prec):
                            output.append(stack.pop())
                        else:
                            break
                    stack.append(("OP", op))
            prev_type, prev_val = tok_type, val

        while stack:
            if stack[-1][0] == "PAREN":
                raise ValueError("Mismatched parentheses.")
            output.append(stack.pop())
        return output

    @classmethod
    def evaluate(cls, rpn_tokens: List[Tuple[str, str]], variables: Dict[str, complex] = None) -> complex:
        if variables is None:
            variables = {}
        stack: List[complex] = []

        for tok_type, val in rpn_tokens:
            if tok_type == "NUM":
                if val in cls.CONSTANTS:
                    stack.append(cls.CONSTANTS[val])
                elif val.endswith('j'):
                    stack.append(complex(0, float(val[:-1])))
                else:
                    stack.append(complex(float(val)))
            elif tok_type == "VAR":
                if val in variables:
                    stack.append(variables[val])
                else:
                    raise ValueError(f"Variable '{val}' not found.")
            elif tok_type == "FUNC":
                if not stack:
                    raise ValueError("No arguments for function.")
                arg = stack.pop()
                stack.append(cls.FUNCTIONS[val](arg))
            elif tok_type == "OP":
                if val == "u-":
                    if not stack:
                        raise ValueError("Unary operator error.")
                    stack.append(-stack.pop())
                else:
                    if len(stack) < 2:
                        raise ValueError(f"Not enough operands for '{val}'.")
                    b = stack.pop()
                    a = stack.pop()
                    try:
                        res = cls.OPERATORS[val][2](a, b)  # type: ignore
                        stack.append(res)
                    except ZeroDivisionError:
                        raise ZeroDivisionError("Division by zero.")
        if len(stack) != 1:
            raise ValueError("Expression structure error.")
        return stack[0]

    @classmethod
    def safe_eval(cls, expr: str, variables: Dict[str, complex] = None) -> complex:
        tokens = cls.tokenize(expr)
        rpn = cls.to_rpn(tokens)
        return cls.evaluate(rpn, variables)

# SCIENTIFIC AND ENGINEERING MODULES

class Matrix:
    def __init__(self, data: List[List[float]]) -> None:
        self.data = data
        self.rows = len(data)
        self.cols = len(data[0]) if self.rows > 0 else 0

    def __add__(self, other: Matrix) -> Matrix:
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions do not match.")
        return Matrix([[self.data[i][j] + other.data[i][j] for j in range(self.cols)] for i in range(self.rows)])

    def __sub__(self, other: Matrix) -> Matrix:
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions do not match.")
        return Matrix([[self.data[i][j] - other.data[i][j] for j in range(self.cols)] for i in range(self.rows)])

    def __mul__(self, other: Matrix) -> Matrix:
        if self.cols != other.rows:
            raise ValueError("Incompatible dimensions for multiplication.")
        res = [[0.0] * other.cols for _ in range(self.rows)]
        for i in range(self.rows):
            for j in range(other.cols):
                for k in range(self.cols):
                    res[i][j] += self.data[i][k] * other.data[k][j]
        return Matrix(res)

    def transpose(self) -> Matrix:
        return Matrix([[self.data[i][j] for i in range(self.rows)] for j in range(self.cols)])

    def determinant(self) -> float:
        if self.rows != self.cols:
            raise ValueError("Matrix must be square.")
        n = self.rows
        m_copy = [row[:] for row in self.data]
        det = 1.0
        for i in range(n):
            pivot = i
            for r in range(i + 1, n):
                if abs(m_copy[r][i]) > abs(m_copy[pivot][i]):
                    pivot = r
            if pivot != i:
                m_copy[i], m_copy[pivot] = m_copy[pivot], m_copy[i]
                det *= -1.0
            if abs(m_copy[i][i]) < 1e-12:
                return 0.0
            det *= m_copy[i][i]
            for r in range(i + 1, n):
                factor = m_copy[r][i] / m_copy[i][i]
                for c in range(i, n):
                    m_copy[r][c] -= factor * m_copy[i][c]
        return det

    def inverse(self) -> Matrix:
        if self.rows != self.cols:
            raise ValueError("Matrix must be square.")
        n = self.rows
        aug = [self.data[i] + [1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
        for i in range(n):
            pivot = i
            for r in range(i + 1, n):
                if abs(aug[r][i]) > abs(aug[pivot][i]):
                    pivot = r
            if pivot != i:
                aug[i], aug[pivot] = aug[pivot], aug[i]
            if abs(aug[i][i]) < 1e-12:
                raise ValueError("Matrix is singular.")
            factor = aug[i][i]
            for c in range(2 * n):
                aug[i][c] /= factor
            for r in range(n):
                if r != i:
                    f = aug[r][i]
                    for c in range(i, 2 * n):
                        aug[r][c] -= f * aug[i][c]
        inv_data = [row[n:] for row in aug]
        return Matrix(inv_data)

    def to_string(self) -> str:
        return "\n".join(["\t".join([f"{Colors.GREEN}{cell:.4g}{Colors.RESET}" for cell in row]) for row in self.data])


class AdvancedScience:
    PHYSICAL_CONSTANTS = {
        "Speed of light (c)": "299792458 m/s",
        "Gravitational constant (G)": "6.6743e-11 N·m²/kg²",
        "Planck constant (h)": "6.62607015e-34 J·s",
        "Avogadro's number (Na)": "6.02214076e23 mol⁻¹",
        "Universal gas constant (R)": "8.314462618 J/(mol·K)",
        "Standard gravity (g)": "9.80665 m/s²"
    }

    CHEMICAL_ELEMENTS = {
        "H": 1.008, "He": 4.0026, "Li": 6.94, "Be": 9.0122, "B": 10.81, "C": 12.011,
        "N": 14.007, "O": 15.999, "F": 18.998, "Ne": 20.180, "Na": 22.990, "Mg": 24.305,
        "Al": 26.982, "Si": 28.085, "P": 30.974, "S": 32.06, "Cl": 35.45, "K": 39.098,
        "Ca": 40.078, "Fe": 55.845, "Cu": 63.546, "Zn": 65.38
    }

    @classmethod
    def parse_chemical_formula(cls, formula: str) -> float:
        tokens = re.findall(r'([A-Z][a-z]*|\([^)]+\))(\d*)', formula)
        total_mass = 0.0
        for elem, count in tokens:
            count_val = int(count) if count else 1
            if elem.startswith('('):
                sub_mass = cls.parse_chemical_formula(elem[1:-1])
                total_mass += sub_mass * count_val
            else:
                if elem not in cls.CHEMICAL_ELEMENTS:
                    raise ValueError(f"Element '{elem}' not found in database.")
                total_mass += cls.CHEMICAL_ELEMENTS[elem] * count_val
        return total_mass

    @staticmethod
    def solve_cubic(a: float, b: float, c: float, d: float) -> List[complex]:
        if a == 0:
            raise ValueError("Parameter 'a' cannot be zero.")
        b, c, d = b / a, c / a, d / a
        f = ((3 * c) - (b ** 2)) / 3
        g = ((2 * (b ** 3)) - (9 * b * c) + (27 * d)) / 27
        h = ((g ** 2) / 4) + ((f ** 3) / 27)

        if h > 0:
            r = -(g / 2) + math.sqrt(h)
            s = r ** (1/3) if r >= 0 else -((-r) ** (1/3))
            t = -(g / 2) - math.sqrt(h)
            u = t ** (1/3) if t >= 0 else -((-t) ** (1/3))
            x1 = (s + u) - (b / 3)
            x2 = complex(-(s + u) / 2 - (b / 3), (s - u) * math.sqrt(3) / 2)
            x3 = complex(-(s + u) / 2 - (b / 3), -(s - u) * math.sqrt(3) / 2)
            return [complex(x1), x2, x3]
        elif f == 0 and g == 0 and h == 0:
            return [complex(-(d ** (1/3)))] * 3
        else:
            i = math.sqrt(((g ** 2) / 4) - h)
            j = i ** (1/3)
            k = math.acos(-(g / (2 * i)))
            m = math.cos(k / 3)
            n = math.sqrt(3) * math.sin(k / 3)
            p = -(b / 3)
            x1 = 2 * j * m + p
            x2 = -j * (m + n) + p
            x3 = -j * (m - n) + p
            return [complex(x1), complex(x2), complex(x3)]

    @staticmethod
    def advanced_statistics(data: List[float]) -> Dict[str, Any]:
        from collections import Counter
        n = len(data)
        if n == 0:
            raise ValueError("Empty sample.")
        
        sorted_d = sorted(data)
        mean_val = sum(sorted_d) / n
        
        counts = Counter(sorted_d)
        max_freq = max(counts.values())
        modes = [k for k, v in counts.items() if v == max_freq]
        mode_val = modes[0] if max_freq > 1 else sorted_d[0]
        
        def get_median(lst: List[float]) -> float:
            length = len(lst)
            if length % 2 != 0:
                return lst[length // 2]
            return (lst[length // 2 - 1] + lst[length // 2]) / 2

        q2 = get_median(sorted_d)
        if n % 2 == 0:
            q1 = get_median(sorted_d[:n // 2])
            q3 = get_median(sorted_d[n // 2:])
        else:
            q1 = get_median(sorted_d[:n // 2])
            q3 = get_median(sorted_d[n // 2 + 1:])
            
        return {"mean": mean_val, "mode": mode_val, "q1": q1, "q2": q2, "q3": q3}

# AUTOMATED TESTING SYSTEM

class KronosTestSuite(unittest.TestCase):
    def test_math_parser(self) -> None:
        self.assertAlmostEqual(MathEngine.safe_eval("2 + 2 * 2").real, 6.0)
        self.assertAlmostEqual(MathEngine.safe_eval("sin(pi / 2)").real, 1.0)
        self.assertAlmostEqual(MathEngine.safe_eval("2 ** 3").real, 8.0)

    def test_matrix_operations(self) -> None:
        m1 = Matrix([[1, 2], [3, 4]])
        m2 = Matrix([[5, 6], [7, 8]])
        res = m1 + m2
        self.assertEqual(res.data, [[6, 8], [10, 12]])
        self.assertAlmostEqual(m1.determinant(), -2.0)

# APPLICATION ASSEMBLY AND MANAGEMENT POINT

class KronosApp:
    def __init__(self) -> None:
        self.config = ConfigManager()
        self.ui = TerminalUI(self.config)
        self.history = HistoryEngine(
            self.config.settings.get("history_file", "kronos_history.json"),
            self.config.settings.get("export_dir", "exports")
        )

    def run(self) -> None:
        while True:
            TerminalUI.clear()
            self.ui.show_banner()
            print(f"   {Colors.BOLD}{Colors.YELLOW}─[ MATHEMATICS ]─{Colors.RESET}")
            print(f"   {Colors.CYAN}[1]{Colors.RESET} Expression Calculator (RPN, complex numbers)")
            print(f"   {Colors.CYAN}[2]{Colors.RESET} Linear Algebra (Matrices)")
            print(f"   {Colors.CYAN}[3]{Colors.RESET} Algebraic Equations (Quadratic/Cubic)")
            print(f"   {Colors.CYAN}[4]{Colors.RESET} Calculus (Numerical Differentiation/Integration)")
            print(f"\n   {Colors.BOLD}{Colors.YELLOW}─[ ANALYTICS ]─{Colors.RESET}")
            print(f"   {Colors.CYAN}[5]{Colors.RESET} Physics (Constants and Kinematics)")
            print(f"   {Colors.CYAN}[6]{Colors.RESET} Chemistry (Molar Mass)")
            print(f"   {Colors.CYAN}[7]{Colors.RESET} Statistical Sample Analysis")
            print(f"   {Colors.CYAN}[8]{Colors.RESET} Plotting (Matplotlib)")
            print(f"\n   {Colors.BOLD}{Colors.YELLOW}─[ TOOLS ]─{Colors.RESET}")
            print(f"   {Colors.CYAN}[9]{Colors.RESET} Cryptography (Hashing)")
            print(f"   {Colors.CYAN}[10]{Colors.RESET} Number System Converter")
            print(f"   {Colors.CYAN}[11]{Colors.RESET} Calculation Log and Export")
            print(f"   {Colors.CYAN}[12]{Colors.RESET} Run Tests")
            print(f"\n   {Colors.BOLD}{Colors.RED}[0]{Colors.RESET} Exit")
            print(f"{Colors.CYAN}======================================================================{Colors.RESET}")
            
            choice = self.ui.get_input(f"{Colors.BOLD}{Colors.CYAN}» Select an option: {Colors.RESET}", int, lambda x: 0 <= x <= 12, "Invalid input.")
            if choice == 0:
                self.ui.print_smart(f"\n{Colors.BOLD}{Colors.MAGENTA}Session closed.{Colors.RESET}")
                break
            self.route_menu(choice)

    def route_menu(self, choice: int) -> None:
        TerminalUI.clear()
        try:
            match choice:
                case 1: self.mod_calculator()
                case 2: self.mod_matrix()
                case 3: self.mod_equations()
                case 4: self.mod_calculus()
                case 5: self.mod_physics()
                case 6: self.mod_chemistry()
                case 7: self.mod_statistics()
                case 8: self.mod_plotting()
                case 9: self.mod_cryptography()
                case 10: self.mod_conversion()
                case 11: self.mod_history_center()
                case 12: self.mod_run_tests()
        except Exception as e:
            self.ui.print_smart(f"\n{Colors.RED}Module execution error: {e}{Colors.RESET}")
        self.ui.pause()

    def mod_calculator(self) -> None:
        self.ui.print_smart(f"{Colors.BOLD}{Colors.CYAN}--- CALCULATOR ---{Colors.RESET}")
        self.ui.print_smart(f"{Colors.GRAY}Functions: sin, cos, tan, sqrt, ln, log, exp, abs. Constants: pi, e, i{Colors.RESET}")
        expr = self.ui.get_input(f"{Colors.YELLOW}Enter expression (or '0' to exit): {Colors.RESET}", str)
        if expr == '0':
            return
        res = MathEngine.safe_eval(expr)
        out = f"{res.real:.10g}" if abs(res.imag) < 1e-12 else f"{res.real:.6g} + {res.imag:.6g}j"
        self.ui.print_smart(f"{Colors.BOLD}{Colors.GREEN}Result: {out}{Colors.RESET}")
        self.history.add("Calculator", expr, out)

    def mod_matrix(self) -> None:
        self.ui.print_smart(f"{Colors.BOLD}{Colors.CYAN}--- MATRICES ---{Colors.RESET}")
        print(f"[{Colors.CYAN}1{Colors.RESET}] Addition A + B\n[{Colors.CYAN}2{Colors.RESET}] Determinant and Inversion")
        sub_choice = self.ui.get_input(f"{Colors.YELLOW}Select action: {Colors.RESET}", int, lambda x: x in [1, 2])
        
        if sub_choice == 2:
            n = self.ui.get_input(f"Matrix dimension N: ", int, lambda x: x > 0)
            data = []
            for i in range(n):
                row = self.ui.get_input(f"Row {i+1} ({n} numbers separated by space): ", str)
                data.append([float(x) for x in row.split()])
            mat = Matrix(data)
            det = mat.determinant()
            self.ui.print_smart(f"\n{Colors.BOLD}{Colors.GREEN}Determinant: {det:.6g}{Colors.RESET}")
            if det != 0:
                self.ui.print_smart(f"{Colors.YELLOW}Inverse matrix:{Colors.RESET}\n" + mat.inverse().to_string())
                self.history.add("Matrices", "Determinant and Inversion", f"Det: {det:.4g}")
            else:
                self.ui.print_smart(f"{Colors.RED}Inverse matrix does not exist (det=0).{Colors.RESET}")

        elif sub_choice == 1:
            r = self.ui.get_input("Rows: ", int)
            c = self.ui.get_input("Columns: ", int)
            self.ui.print_smart(f"\n{Colors.YELLOW}Matrix A:{Colors.RESET}")
            data_a = [[float(x) for x in self.ui.get_input(f"Row {i+1}: ", str).split()] for i in range(r)]
            self.ui.print_smart(f"\n{Colors.YELLOW}Matrix B:{Colors.RESET}")
            data_b = [[float(x) for x in self.ui.get_input(f"Row {i+1}: ", str).split()] for i in range(r)]
            m_a, m_b = Matrix(data_a), Matrix(data_b)
            self.ui.print_smart(f"\n{Colors.BOLD}{Colors.GREEN}A + B:{Colors.RESET}\n" + (m_a + m_b).to_string())

    def mod_equations(self) -> None:
        self.ui.print_smart(f"{Colors.BOLD}{Colors.CYAN}--- EQUATIONS ---{Colors.RESET}")
        print(f"[{Colors.CYAN}1{Colors.RESET}] Quadratic (ax² + bx + c = 0)\n[{Colors.CYAN}2{Colors.RESET}] Cubic (ax³ + bx² + cx + d = 0)")
        type_eq = self.ui.get_input(f"{Colors.YELLOW}Choice: {Colors.RESET}", int, lambda x: x in [1, 2])
        
        if type_eq == 1:
            a = self.ui.get_input("Coefficient a: ", float)
            b = self.ui.get_input("Coefficient b: ", float)
            c = self.ui.get_input("Coefficient c: ", float)
            d = b**2 - 4*a*c
            x1 = (-b + cmath.sqrt(d)) / (2*a)
            x2 = (-b - cmath.sqrt(d)) / (2*a)
            self.ui.print_smart(f"\n{Colors.BOLD}{Colors.GREEN}Discriminant D = {d}{Colors.RESET}")
            self.ui.print_smart(f"{Colors.GREEN}x1 = {x1}{Colors.RESET}\n{Colors.GREEN}x2 = {x2}{Colors.RESET}")
        else:
            a = self.ui.get_input("Coefficient a: ", float)
            b = self.ui.get_input("Coefficient b: ", float)
            c = self.ui.get_input("Coefficient c: ", float)
            d = self.ui.get_input("Coefficient d: ", float)
            roots = AdvancedScience.solve_cubic(a, b, c, d)
            print(f"\n{Colors.BOLD}{Colors.GREEN}Roots of the equation:{Colors.RESET}")
            for idx, r in enumerate(roots):
                self.ui.print_smart(f"  {Colors.GREEN}x{idx+1} = {r}{Colors.RESET}")

    def mod_calculus(self) -> None:
        self.ui.print_smart(f"{Colors.BOLD}{Colors.CYAN}--- CALCULUS ---{Colors.RESET}")
        print(f"[{Colors.CYAN}1{Colors.RESET}] Derivative f'(x) at point\n[{Colors.CYAN}2{Colors.RESET}] Integral (Simpson's Rule)")
        sub = self.ui.get_input(f"{Colors.YELLOW}Choice: {Colors.RESET}", int, lambda x: x in [1, 2])
        expr = self.ui.get_input("Function f(x) (e.g., sin(x)*x): ", str)
        
        if sub == 1:
            x_val = self.ui.get_input("Point x: ", float)
            h = 1e-6
            f_plus = MathEngine.safe_eval(expr, {"x": complex(x_val + h)}).real
            f_minus = MathEngine.safe_eval(expr, {"x": complex(x_val - h)}).real
            df = (f_plus - f_minus) / (2 * h)
            self.ui.print_smart(f"{Colors.BOLD}{Colors.GREEN}f'({x_val}) ≈ {df:.7g}{Colors.RESET}")
        else:
            a = self.ui.get_input("Limit a: ", float)
            b = self.ui.get_input("Limit b: ", float)
            n = 10000
            h = (b - a) / n
            s = MathEngine.safe_eval(expr, {"x": complex(a)}).real + MathEngine.safe_eval(expr, {"x": complex(b)}).real
            for i in range(1, n, 2):
                s += 4 * MathEngine.safe_eval(expr, {"x": complex(a + i * h)}).real
            for i in range(2, n - 1, 2):
                s += 2 * MathEngine.safe_eval(expr, {"x": complex(a + i * h)}).real
            res = s * h / 3
            self.ui.print_smart(f"{Colors.BOLD}{Colors.GREEN}Integral ≈ {res:.7g}{Colors.RESET}")

    def mod_physics(self) -> None:
        self.ui.print_smart(f"{Colors.BOLD}{Colors.CYAN}--- PHYSICS ---{Colors.RESET}")
        for k, v in AdvancedScience.PHYSICAL_CONSTANTS.items():
            print(f"  {Colors.YELLOW}{k}:{Colors.RESET} {v}")
        print(f"\n{Colors.BOLD}{Colors.CYAN}[Kinematics]{Colors.RESET}")
        v0 = self.ui.get_input("Initial velocity v0 (m/s): ", float)
        t = self.ui.get_input("Time t (s): ", float)
        a = self.ui.get_input("Acceleration a (m/s²): ", float)
        s = v0 * t + 0.5 * a * (t**2)
        self.ui.print_smart(f"{Colors.BOLD}{Colors.GREEN}S = {s:.6g} m.{Colors.RESET}")

    def mod_chemistry(self) -> None:
        self.ui.print_smart(f"{Colors.BOLD}{Colors.CYAN}--- CHEMISTRY ---{Colors.RESET}")
        formula = self.ui.get_input("Compound formula (e.g., H2O): ", str)
        molar_mass = AdvancedScience.parse_chemical_formula(formula)
        self.ui.print_smart(f"{Colors.BOLD}{Colors.GREEN}M({formula}) = {molar_mass:.4f} g/mol{Colors.RESET}")
        
        mass = self.ui.get_input("Mass (g) to calculate moles (0 to skip): ", float)
        if mass > 0:
            moles = mass / molar_mass
            self.ui.print_smart(f"{Colors.BOLD}{Colors.GREEN}n = {moles:.4f} mol{Colors.RESET}")

    def mod_statistics(self) -> None:
        self.ui.print_smart(f"{Colors.BOLD}{Colors.CYAN}--- STATISTICS ---{Colors.RESET}")
        raw = self.ui.get_input("Sample (numbers separated by space): ", str)
        data = [float(x) for x in raw.split()]
        stats = AdvancedScience.advanced_statistics(data)
        print(f"\n{Colors.BOLD}{Colors.GREEN}Results:{Colors.RESET}")
        print(f"  {Colors.YELLOW}Mean:{Colors.RESET} {stats['mean']:.4g}")
        print(f"  {Colors.YELLOW}Mode:{Colors.RESET} {stats['mode']:.4g}")
        print(f"  {Colors.YELLOW}Q1:{Colors.RESET} {stats['q1']:.4g}")
        print(f"  {Colors.YELLOW}Median (Q2):{Colors.RESET} {stats['q2']:.4g}")
        print(f"  {Colors.YELLOW}Q3:{Colors.RESET} {stats['q3']:.4g}")

    def mod_plotting(self) -> None:
        self.ui.print_smart(f"{Colors.BOLD}{Colors.CYAN}--- PLOTTING ---{Colors.RESET}")
        try:
            import matplotlib.pyplot as plt
            import numpy as np
        except ImportError:
            self.ui.print_smart(f"{Colors.RED}Dependencies not found. Install matplotlib and numpy.{Colors.RESET}")
            return

        print(f"[{Colors.CYAN}1{Colors.RESET}] Cartesian plot\n[{Colors.CYAN}2{Colors.RESET}] Polar plot")
        mode = self.ui.get_input(f"{Colors.YELLOW}Choice: {Colors.RESET}", int, lambda x: x in [1, 2])
        plt.style.use(self.config.settings.get("plot_theme", "dark_background"))
        
        if mode == 1:
            exprs = self.ui.get_input("Functions separated by ';' (e.g.: sin(x); cos(x)): ", str)
            funcs = [e.strip() for e in exprs.split(";")]
            x = np.linspace(-10, 10, 400)
            plt.figure(figsize=(10, 6))
            for f in funcs:
                y = [MathEngine.safe_eval(f, {"x": complex(val)}).real for val in x]
                plt.plot(x, y, label=f"y = {f}")
            plt.axhline(0, color='white', linewidth=0.8)
            plt.axvline(0, color='white', linewidth=0.8)
            plt.grid(True, color='gray', linestyle='--', alpha=0.5)
            plt.legend()
            plt.show()
        else:
            f = self.ui.get_input("Polar function r(theta): ", str)
            theta = np.linspace(0, 2 * np.pi, 500)
            r = [MathEngine.safe_eval(f, {"theta": complex(t)}).real for t in theta]
            plt.figure(figsize=(6, 6))
            plt.subplot(111, projection='polar')
            plt.plot(theta, r, color='#00ffcc', linewidth=2)
            plt.title(f"r = {f}")
            plt.show()

    def mod_cryptography(self) -> None:
        self.ui.print_smart(f"{Colors.BOLD}{Colors.CYAN}--- CRYPTOGRAPHY ---{Colors.RESET}")
        text = self.ui.get_input("String to process: ", str)
        s256 = hashlib.sha256(text.encode()).hexdigest()
        s512 = hashlib.sha512(text.encode()).hexdigest()
        b64 = base64.b64encode(text.encode()).decode()
        print(f"\n{Colors.BOLD}{Colors.GREEN}Results:{Colors.RESET}")
        print(f"  {Colors.YELLOW}SHA256:{Colors.RESET} {s256}")
        print(f"  {Colors.YELLOW}SHA512:{Colors.RESET} {s512}")
        print(f"  {Colors.YELLOW}Base64:{Colors.RESET} {b64}")

    def mod_conversion(self) -> None:
        self.ui.print_smart(f"{Colors.BOLD}{Colors.CYAN}--- NUMBER SYSTEM CONVERTER ---{Colors.RESET}")
        num = self.ui.get_input("Integer (Base 10): ", int)
        print(f"\n{Colors.BOLD}{Colors.GREEN}Representation:{Colors.RESET}")
        print(f"  {Colors.YELLOW}BIN:{Colors.RESET} {bin(num)}")
        print(f"  {Colors.YELLOW}OCT:{Colors.RESET} {oct(num)}")
        print(f"  {Colors.YELLOW}HEX:{Colors.RESET} {hex(num).upper()}")

    def mod_history_center(self) -> None:
        self.ui.print_smart(f"{Colors.BOLD}{Colors.CYAN}--- LOG AND EXPORT ---{Colors.RESET}")
        if not self.history.items:
            self.ui.print_smart(f"{Colors.GRAY}History is empty.{Colors.RESET}")
            return
        for item in self.history.items:
            print(item.to_line())
        print(f"\n[{Colors.CYAN}1{Colors.RESET}] Export to TXT\n[{Colors.CYAN}2{Colors.RESET}] Export to CSV\n[{Colors.CYAN}3{Colors.RESET}] Clear history")
        act = self.ui.get_input(f"{Colors.YELLOW}Choice: {Colors.RESET}", int, lambda x: x in [1, 2, 3])
        if act == 1:
            p = self.history.export_txt()
            self.ui.print_smart(f"{Colors.GREEN}Exported to TXT: {p}{Colors.RESET}")
        elif act == 2:
            p = self.history.export_csv()
            self.ui.print_smart(f"{Colors.GREEN}Exported to CSV: {p}{Colors.RESET}")
        elif act == 3:
            self.history.clear()
            self.ui.print_smart(f"{Colors.RED}History cleared.{Colors.RESET}")

    def mod_run_tests(self) -> None:
        self.ui.print_smart(f"{Colors.BOLD}{Colors.CYAN}Running core unit tests...{Colors.RESET}\n")
        suite = unittest.TestLoader().loadTestsFromTestCase(KronosTestSuite)
        unittest.TextTestRunner(verbosity=2).run(suite)

# PROGRAM ENTRY POINT

if __name__ == "__main__":
    app = KronosApp()
    app.run()