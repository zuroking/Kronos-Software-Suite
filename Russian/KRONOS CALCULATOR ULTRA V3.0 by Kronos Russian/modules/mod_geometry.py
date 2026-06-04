# modules/mod_geometry.py
import math
from kronos_core import Colors

METADATA = {
    "id": 6,
    "category": "АЛГЕБРА И ГЕОМЕТРИЯ",
    "name": "Геометрия (Convex Hull, Полигоны и Анализ Треугольников)"
}

class GeometryProcessor:
    @staticmethod
    def analyze_triangle(a: float, b: float, c: float) -> dict:
        if a + b <= c or a + c <= b or b + c <= a:
            raise ValueError("Треугольник с такими сторонами не существует!")
            
        p = (a + b + c) / 2
        area = math.sqrt(p * (p - a) * (p - b) * (p - c))
        r_in = area / p
        r_out = (a * b * c) / (4 * area) if area > 0 else 0.0
        
        cos_alpha = max(-1.0, min(1.0, (b**2 + c**2 - a**2) / (2 * b * c)))
        cos_beta = max(-1.0, min(1.0, (a**2 + c**2 - b**2) / (2 * a * c)))
        
        alpha = math.degrees(math.acos(cos_alpha))
        beta = math.degrees(math.acos(cos_beta))
        gamma = 180.0 - alpha - beta
        
        max_angle = max(alpha, beta, gamma)
        if abs(max_angle - 90.0) < 1e-7: character = "Прямоугольный"
        elif max_angle > 90.0: character = "Тупоугольный"
        else: character = "Остроугольный"
        
        return {
            "area": area, "perimeter": a + b + c,
            "r_in": r_in, "r_out": r_out,
            "angles": (alpha, beta, gamma), "type": character
        }

    @staticmethod
    def convex_hull(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
        pts = sorted(list(set(points)))
        if len(pts) <= 1: return pts

        def cross(o, a, b):
            return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

        lower = []
        for p in pts:
            while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0: lower.pop()
            lower.append(p)

        upper = []
        for p in reversed(pts):
            while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0: upper.pop()
            upper.append(p)

        return lower[:-1] + upper[:-1]

    @staticmethod
    def polygon_area_perimeter(points: list[tuple[float, float]]) -> tuple[float, float]:
        n = len(points)
        area = 0.0
        perimeter = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += points[i][0] * points[j][1]
            area -= points[j][0] * points[i][1]
            perimeter += math.hypot(points[i][0] - points[j][0], points[i][1] - points[j][1])
        return abs(area) / 2.0, perimeter


class KronosPlugin:
    def __init__(self, app) -> None:
        self.app = app

    def execute(self) -> None:
        self.app.ui.print_smart(f"{Colors.BOLD}{Colors.CYAN}--- ГЕОМЕТРИЧЕСКИЙ АНАЛИТИЧЕСКИЙ СТЕНД ULTRA V3.0 ---{Colors.RESET}")
        print(" Выберите режим работы:")
        print("  [1] Комплексный анализ треугольника по 3-м сторонам")
        print("  [2] Построение Выпуклой Оболочки (Convex Hull) множества точек")
        print("  [3] Оценка площади и периметра многоугольника (Формула Гаусса)")
        
        choice = self.app.ui.get_input("\nДействие: ", int, lambda x: 1 <= x <= 3)
        
        try:
            if choice == 1:
                print(f"\n{Colors.YELLOW}--- АНАЛИЗ ТРЕУГОЛЬНИКА ---{Colors.RESET}")
                a = self.app.ui.get_input("Сторона a: ", float, lambda x: x > 0)
                b = self.app.ui.get_input("Сторона b: ", float, lambda x: x > 0)
                c = self.app.ui.get_input("Сторона c: ", float, lambda x: x > 0)
                
                res = GeometryProcessor.analyze_triangle(a, b, c)
                
                self.app.ui.print_smart(f"\n{Colors.BOLD}{Colors.GREEN}[РЕЗУЛЬТАТЫ МЕТРИЧЕСКОГО АНАЛИЗА]:{Colors.RESET}")
                print(f"  • Периметр треугольника:  {res['perimeter']:.4f}")
                print(f"  • Площадь по Герону (S):  {Colors.BRIGHT_GREEN}{res['area']:.4f}{Colors.RESET}")
                print(f"  • Тип геометрии углов:    {Colors.YELLOW}{res['type']}{Colors.RESET}")
                print(f"  • Радиус вписанной окр.:  {res['r_in']:.4f}")
                print(f"  • Радиус описанной окр.: {res['r_out']:.4f}")
                
                print(f"\n{Colors.BOLD}{Colors.CYAN}[ВНУТРЕННИЕ УГЛЫ]:{Colors.RESET}")
                print(f"  • Угол α (противолежащий a): {res['angles'][0]:.2f}°")
                print(f"  • Угол β (противолежащий b): {res['angles'][1]:.2f}°")
                print(f"  • Угол γ (противолежащий c): {res['angles'][2]:.2f}°")
                
                self.app.history.add("Геометрия", f"Треугольник {a}-{b}-{c}", res['type'])

            elif choice == 2:
                print(f"\n{Colors.YELLOW}--- ВЫПУКЛАЯ ОБОЛОЧКА (CONVEX HULL) ---{Colors.RESET}")
                print(f"{Colors.GRAY}Вводите координаты точек (X Y) через пробел. Пустая строка — завершить ввод.{Colors.RESET}")
                pts = []
                while True:
                    inp = self.app.ui.get_input(f"  Точка {len(pts)+1}: ", str, allow_empty=True)
                    if not inp: break
                    try:
                        coords = tuple(map(float, inp.split()))
                        if len(coords) != 2:
                            self.app.ui.print_error("Ошибка: нужно ввести ровно 2 координаты (X и Y).")
                            continue
                        pts.append(coords)
                    except ValueError:
                        self.app.ui.print_error("Некорректный формат чисел.")
                
                if len(pts) < 3:
                    self.app.ui.print_error("Для построения оболочки нужно минимум 3 уникальные точки!")
                    return
                    
                hull = GeometryProcessor.convex_hull(pts)
                self.app.ui.print_smart(f"\n{Colors.BOLD}{Colors.GREEN}[ВЕРШИНЫ ОБОЛОЧКИ (ПО КОНТУРУ)]:{Colors.RESET}")
                for p in hull:
                    print(f"  • Точка: ({p[0]}, {p[1]})")
                self.app.history.add("Геометрия", f"Convex Hull {len(pts)} точек", f"Вершин={len(hull)}")

            elif choice == 3:
                print(f"\n{Colors.YELLOW}--- АНАЛИЗ МНОГОУГОЛЬНИКА ---{Colors.RESET}")
                print(f"{Colors.GRAY}Вводите координаты вершин последовательно по контуру (X Y). Пустая строка - расчет.{Colors.RESET}")
                pts = []
                while True:
                    inp = self.app.ui.get_input(f"  Вершина {len(pts)+1}: ", str, allow_empty=True)
                    if not inp: break
                    try:
                        coords = tuple(map(float, inp.split()))
                        if len(coords) != 2:
                            self.app.ui.print_error("Нужно 2 числа!")
                            continue
                        pts.append(coords)
                    except ValueError:
                        self.app.ui.print_error("Некорректный формат чисел.")
                
                if len(pts) < 3:
                    self.app.ui.print_error("Многоугольник должен иметь минимум 3 вершины!")
                    return
                    
                area, perim = GeometryProcessor.polygon_area_perimeter(pts)
                self.app.ui.print_smart(f"\n{Colors.BOLD}{Colors.GREEN}[РЕЗУЛЬТАТЫ РАСЧЕТА ПОЛИГОНА]:{Colors.RESET}")
                print(f"  • Периметр контура: {perim:.4f}")
                print(f"  • Площадь (S): {Colors.BRIGHT_GREEN}{area:.4f}{Colors.RESET} кв. ед.")
                self.app.history.add("Геометрия", f"Полигон {len(pts)} вершин", f"S={area:.2f}")

        except Exception as e:
            self.app.ui.print_error(f"Критический сбой геометрического процессора: {e}")