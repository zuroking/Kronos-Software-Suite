# modules/mod_equations.py
import math
import cmath
from kronos_core import Colors

METADATA = {
    "id": 4,
    "category": "АЛГЕБРА И ГЕОМЕТРИЯ",
    "name": "Решатель уравнений (Линейные, Квадратные и Кубические по Кардано)"
}

class EquationsEngine:
    @staticmethod
    def solve_linear(a: float, b: float) -> list:
        if a == 0:
            if b == 0: return [float('inf')]  
            return []  
        return [round(-b / a, 12)]

    @staticmethod
    def solve_quadratic(a: float, b: float, c: float) -> list:
        if a == 0:
            return EquationsEngine.solve_linear(b, c)
            
        d = b**2 - 4*a*c
        if d > 0:
            r1 = (-b + math.sqrt(d)) / (2*a)
            r2 = (-b - math.sqrt(d)) / (2*a)
            return [round(r1, 12), round(r2, 12)]
        elif d == 0:
            return [round(-b / (2*a), 12)]
        else:
            root1 = (-b + cmath.sqrt(d)) / (2*a)
            root2 = (-b - cmath.sqrt(d)) / (2*a)
            return [complex(round(root1.real, 12), round(root1.imag, 12)), 
                    complex(round(root2.real, 12), round(root2.imag, 12))]

    @staticmethod
    def solve_cubic_cardano(a: float, b: float, c: float, d: float) -> list:
        if a == 0:
            return EquationsEngine.solve_quadratic(b, c, d)

        p = (3*a*c - b**2) / (3 * a**2)
        q = (2*b**3 - 9*a*b*c + 27*a**2*d) / (27 * a**3)
        
        disp = (q / 2)**2 + (p / 3)**3
        shift = -b / (3 * a)

        if disp > 0:
            u = (-q / 2 + math.sqrt(disp))
            v = (-q / 2 - math.sqrt(disp))
            
            u = math.copysign(abs(u)**(1/3), u)
            v = math.copysign(abs(v)**(1/3), v)
            
            r1 = u + v + shift
            r2 = complex(-(u + v) / 2 + shift, (u - v) * math.sqrt(3) / 2)
            r3 = complex(-(u + v) / 2 + shift, -(u - v) * math.sqrt(3) / 2)
            
            return [round(r1, 12), 
                    complex(round(r2.real, 12), round(r2.imag, 12)), 
                    complex(round(r3.real, 12), round(r3.imag, 12))]

        elif disp == 0:
            if p == 0 and q == 0:
                return [round(shift, 12)]
            
            r1 = 3 * q / p + shift
            r2 = -3 * q / (2 * p) + shift
            return [round(r1, 12), round(r2, 12), round(r2, 12)]

        else:
            r = math.sqrt(-(p / 3)**3)
            phi = math.acos(max(-1.0, min(1.0, -q / (2 * r))))
            
            r1 = 2 * math.pow(r, 1/3) * math.cos(phi / 3) + shift
            r2 = 2 * math.pow(r, 1/3) * math.cos((phi + 2 * math.pi) / 3) + shift
            r3 = 2 * math.pow(r, 1/3) * math.cos((phi + 4 * math.pi) / 3) + shift
            
            return [round(r1, 12), round(r2, 12), round(r3, 12)]


class KronosPlugin:
    def __init__(self, app) -> None:
        self.app = app

    def execute(self) -> None:
        self.app.ui.print_smart(f"{Colors.BOLD}{Colors.CYAN}--- ВЫЧИСЛИТЕЛЬНЫЙ АНАЛИЗАТОР УРАВНЕНИЙ ULTRA V3.0 ---{Colors.RESET}")
        print(" Поддерживаемые типы уравнений:")
        print("  • Линейные: ax + b = 0")
        print("  • Квадратные: ax^2 + bx + c = 0")
        print("  • Кубические: ax^3 + bx^2 + cx + d = 0")
        
        print(f"\n{Colors.YELLOW}Введите коэффициенты системы (0 для отсутствующих):{Colors.RESET}")
        a = self.app.ui.get_input(" Коэффициент a: ", float)
        b = self.app.ui.get_input(" Коэффициент b: ", float)
        c = self.app.ui.get_input(" Коэффициент c: ", float)
        d = self.app.ui.get_input(" Коэффициент d (для кубических): ", float)
        
        try:
            status_msg = ""
            if a == 0 and b == 0 and c == 0 and d == 0:
                roots = [float('inf')]
            elif a == 0 and b == 0:
                roots = EquationsEngine.solve_linear(c, d)
            elif a == 0:
                status_msg = f"{Colors.YELLOW}[ИНФО]: Степень понижена до квадратной.{Colors.RESET}"
                roots = EquationsEngine.solve_quadratic(b, c, d)
            else:
                roots = EquationsEngine.solve_cubic_cardano(a, b, c, d)
                
            self.app.ui.print_smart(f"\n{Colors.BOLD}{Colors.GREEN}[АНАЛИЗ КОРНЕЙ УРАВНЕНИЯ ЗАВЕРШЕН]:{Colors.RESET}")
            if status_msg:
                print(f"  {status_msg}")
                
            if not roots:
                print(f"  • {Colors.RED}Уравнение не имеет математических решений.{Colors.RESET}")
            elif len(roots) == 1 and roots[0] == float('inf'):
                print(f"  • {Colors.YELLOW}Уравнение имеет бесконечное множество решений.{Colors.RESET}")
            else:
                for idx, r in enumerate(roots):
                    if isinstance(r, complex):
                        sign = "+" if r.imag >= 0 else "-"
                        print(f"  • корень x{idx+1} = {Colors.BRIGHT_MAGENTA}{r.real:.6g} {sign} {abs(r.imag):.6g}i{Colors.RESET} (Комплексный корень)")
                    else:
                        print(f"  • корень x{idx+1} = {Colors.BRIGHT_GREEN}{r:.6g}{Colors.RESET}")
                        
            eq_type = "Кубическое" if a != 0 else ("Квадратное" if b != 0 else "Линейное")
            self.app.history.add("Уравнения", f"Речено {eq_type} уравнение", f"Корней: {len(roots)}")

        except Exception as e:
            self.app.ui.print_error(f"Критический сбой процессора уравнений: {e}")