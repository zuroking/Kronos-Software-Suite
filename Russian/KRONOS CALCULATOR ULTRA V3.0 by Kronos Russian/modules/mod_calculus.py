# modules/mod_calculus.py
import math

METADATA = {
    "id": 5,
    "category": "АЛГЕБРА И ГЕОМЕТРИЯ",
    "name": "Высший математический анализ (Численный интеграл Симпсона и Производные)"
}

class BuiltinSafeParser:
    def __init__(self):
        self.allowed_names = {
            "abs": abs, "round": round, "max": max, "min": min,
            "sin": math.sin, "cos": math.cos, "tan": math.tan,
            "asin": math.asin, "acos": math.acos, "atan": math.atan,
            "sinh": math.sinh, "cosh": math.cosh, "tanh": math.tanh,
            "sqrt": math.sqrt, "log": math.log, "log10": math.log10,
            "exp": math.exp, "pi": math.pi, "e": math.e
        }

    def eval_expr(self, expr: str, variables: dict) -> float:
        clean_expr = expr.replace("^", "**").replace(" ", "")
        return float(eval(clean_expr, {"__builtins__": None}, self.allowed_names | variables))


class CalculusEngine:
    @staticmethod
    def simpson_integral(app, expr: str, a: float, b: float, n: int = 1000) -> float:
        if n % 2 != 0:
            n += 1
            
        parser = app.parser if hasattr(app, 'parser') and app.parser else BuiltinSafeParser()
        
        try:
            f_a = parser.eval_expr(expr, {"x": a})
            f_b = parser.eval_expr(expr, {"x": b})
            f_mid = parser.eval_expr(expr, {"x": (a + b) / 2})
            if math.isnan(f_a) or math.isnan(f_b) or math.isnan(f_mid) or math.isinf(f_a) or math.isinf(f_b) or math.isinf(f_mid):
                raise ValueError("асимптотический разрыв функции.")
        except (ZeroDivisionError, ValueError, OverflowError):
            raise ValueError("Обнаружена точка разрыва функции внутри ОДЗ отрезка! Интегрирование методом Симпсона невозможно.")

        h = (b - a) / n
        total_sum = parser.eval_expr(expr, {"x": a}) + parser.eval_expr(expr, {"x": b})
        
        for i in range(1, n):
            x = a + i * h
            try:
                f_x = parser.eval_expr(expr, {"x": x})
                if math.isnan(f_x) or math.isinf(f_x):
                    raise ValueError
                if i % 2 == 0:
                    total_sum += 2 * f_x
                else:
                    total_sum += 4 * f_x
            except (ZeroDivisionError, ValueError, OverflowError):
                raise ValueError(f"Критический разрыв функции в промежуточной точке x = {x:.4f}!")

        return (h / 3) * total_sum

    @staticmethod
    def numerical_derivative(app, expr: str, x0: float, h: float = 1e-5) -> float:
        parser = app.parser if hasattr(app, 'parser') and app.parser else BuiltinSafeParser()
        try:
            f_plus = parser.eval_expr(expr, {"x": x0 + h})
            f_minus = parser.eval_expr(expr, {"x": x0 - h})
            return (f_plus - f_minus) / (2 * h)
        except (ZeroDivisionError, ValueError, OverflowError):
            raise ValueError(f"Функция не дифференцируема в точке x = {x0} (выход за границы ОДЗ).")


class KronosPlugin:
    def __init__(self, app) -> None:
        self.app = app

    def execute(self) -> None:
        from kronos_core import Colors
        self.app.ui.print_smart(f"{Colors.BOLD}{Colors.CYAN}--- ВЫЧИСЛИТЕЛЬНЫЙ МОДУЛЬ МАТЕМАТИЧЕСКОГО АНАЛИЗА ULTRA V3.0 ---{Colors.RESET}")
        print(" Выберите операцию:")
        print("  [1] Численное интегрирование f(x) на отрезке [a; b] (Метод Симпсона)")
        print("  [2] Расчет мгновенной производной f'(x) в точке")
        
        choice = self.app.ui.get_input("Действие: ", int, lambda x: x in (1, 2))
        
        try:
            if choice == 1:
                expr = self.app.ui.get_input("\nВведите интегрируемую функцию f(x) (например: x**2 + sin(x)): ", str)
                a = self.app.ui.get_input("Введите нижний предел интегрирования (a): ", float)
                b = self.app.ui.get_input("Введите верхний предел интегрирования (b): ", float)
                
                if a > b:
                    print(f"  {Colors.YELLOW}[ИНФО]: Смена пределов интегрирования (a > b). Знак результата изменится.{Colors.RESET}")
                    a, b = b, a
                    res = -CalculusEngine.simpson_integral(self.app, expr, a, b)
                else:
                    res = CalculusEngine.simpson_integral(self.app, expr, a, b)
                
                self.app.ui.print_smart(f"\n{Colors.BOLD}{Colors.GREEN}[ВЫЧИСЛЕНИЕ ЧИСЛЕННОГО ИНТЕГРАЛА ЗАВЕРШЕНО]:{Colors.RESET}")
                print(f"  • Значение площади под кривой ∫ f(x) dx = {Colors.BRIGHT_GREEN}{res:.8g}{Colors.RESET}")
                self.app.history.add("Матанализ", f"Интеграл {expr}", f"Res={res:.4f}")
                
            elif choice == 2:
                expr = self.app.ui.get_input("\nВведите функцию f(x) для дифференцирования (например: x**3 - 2*x): ", str)
                x_val = self.app.ui.get_input("Введите точку исследования x: ", float)
                
                res = CalculusEngine.numerical_derivative(self.app, expr, x_val)
                
                self.app.ui.print_smart(f"\n{Colors.BOLD}{Colors.GREEN}[РАСЧЕТ МГНОВЕННОЙ СКОРОСТИ ИЗМЕНЕНИЯ]:{Colors.RESET}")
                print(f"  • Значение тангенса угла наклона f'({x_val}) = {Colors.BRIGHT_CYAN}{res:.6g}{Colors.RESET}")
                self.app.history.add("Матанализ", f"Производная {expr} в x={x_val}", f"Res={res:.4f}")

        except ValueError as ve:
            self.app.ui.print_error(f"Математическое ограничение: {ve}")
        except Exception as e:
            self.app.ui.print_error(f"Критический сбой процессора матанализа: {e}")