# modules/mod_plotting.py
import math
from kronos_core import Colors

METADATA = {
    "id": 12,
    "category": "ИНЖЕНЕРИЯ И АНАЛИТИКА",
    "name": "ASCII Графический визуализатор математических функций"
}

class AsciiPlotter:
    @staticmethod
    def safe_eval(expr: str, x_val: float) -> float:
        allowed_words = {
            "x": x_val,
            "sin": math.sin, "cos": math.cos, "tan": math.tan,
            "sqrt": math.sqrt, "log": math.log, "exp": math.exp,
            "pi": math.pi, "e": math.e, "abs": abs
        }
        return float(eval(expr.replace(" ", ""), {"__builtins__": None}, allowed_words))

    @staticmethod
    def generate_chart(expr: str, width: int = 60, height: int = 20) -> list[str]:
        canvas = [[" " for _ in range(width)] for _ in range(height)]
        
        x_min, x_max = -10.0, 10.0
        y_vals = []
        x_vals = []
        
        for c in range(width):
            x = x_min + (c / (width - 1)) * (x_max - x_min)
            try:
                y = AsciiPlotter.safe_eval(expr, x)
                if math.isnan(y) or math.isinf(y):
                    continue
                y_vals.append(y)
                x_vals.append((c, y))
            except (ZeroDivisionError, ValueError, OverflowError):
                continue
                
        if not y_vals:
            return [" График не может быть построен: функция не определена на отрезке [-10; 10] "]
            
        y_min, y_max = min(y_vals), max(y_vals)
        if abs(y_max - y_min) < 1e-5:
            y_min -= 1.0
            y_max += 1.0
            
        if y_min <= 0.0 <= y_max:
            r_zero = int((y_max - 0.0) / (y_max - y_min) * (height - 1))
            if 0 <= r_zero < height:
                for c in range(width):
                    canvas[r_zero][c] = "─"
                    
        if x_min <= 0.0 <= x_max:
            c_zero = int((0.0 - x_min) / (x_max - x_min) * (width - 1))
            if 0 <= c_zero < width:
                for r in range(height):
                    canvas[r][c_zero] = "┼" if canvas[r][c_zero] == "─" else "│"
                        
        for c, y in x_vals:
            r = int((y_max - y) / (y_max - y_min) * (height - 1))
            if 0 <= r < height:
                canvas[r][c] = "●"
                    
        return ["".join(row) for row in canvas]


class KronosPlugin:
    def __init__(self, app) -> None:
        self.app = app

    def execute(self) -> None:
        self.app.ui.print_smart(f"{Colors.BOLD}{Colors.CYAN}--- ТЕРМИНАЛЬНЫЙ ASCII ГРАФИЧЕСКИЙ СТЕНД ULTRA V3.0 ---{Colors.RESET}")
        expr = self.app.ui.get_input("Введите математическую функцию f(x) (например: sin(x) или x**2 - 3): ", str)
        
        try:
            chart_lines = AsciiPlotter.generate_chart(expr)
            
            self.app.ui.print_smart(f"\n{Colors.BOLD}{Colors.GREEN}[СИСТЕМА СИМУЛЯЦИИ КООРДИНАТНЫХ ОСЕЙ]:{Colors.RESET}")
            print(Colors.BRIGHT_CYAN + "  ┌" + "─" * 60 + "┐" + Colors.RESET)
            for line in chart_lines:
                print(f"  {Colors.BRIGHT_CYAN}│{Colors.RESET}{Colors.YELLOW}{line}{Colors.RESET}{Colors.BRIGHT_CYAN}│{Colors.RESET}")
            print(Colors.BRIGHT_CYAN + "  └" + "─" * 60 + "┘" + Colors.RESET)
            print(f"  {Colors.GRAY}Масштаб сетки: X ∈ [-10; 10]. Ось Y адаптируется автоматически.{Colors.RESET}")
            
            self.app.history.add("Графика", f"Построен график {expr}", "Успешно")
            
        except Exception as e:
            self.app.ui.print_error(f"Критический сбой рендерера графиков: {e}")