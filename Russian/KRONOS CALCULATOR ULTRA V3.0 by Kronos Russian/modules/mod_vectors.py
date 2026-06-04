# modules/mod_vectors.py
import math
from kronos_core import Colors

METADATA = {
    "id": 2,
    "category": "АЛГЕБРА И ГЕОМЕТРИЯ",
    "name": "Векторная алгебра (N-мерный Анализатор Пространства)"
}

class VectorMath:
    @staticmethod
    def dot_product(v1: list[float], v2: list[float]) -> float:
        return sum(a * b for a, b in zip(v1, v2))

    @staticmethod
    def length(v: list[float]) -> float:
        return math.sqrt(sum(a ** 2 for a in v))

    @staticmethod
    def angle(v1: list[float], v2: list[float]) -> tuple[float, float]:
        dot = VectorMath.dot_product(v1, v2)
        len1 = VectorMath.length(v1)
        len2 = VectorMath.length(v2)
        if len1 == 0 or len2 == 0:
            return 0.0, 0.0
        cos_alpha = max(-1.0, min(1.0, dot / (len1 * len2)))
        rad = math.acos(cos_alpha)
        return rad, math.degrees(rad)

    @staticmethod
    def cross_product(v1: list[float], v2: list[float]) -> list[float]:
        a = v1 + [0.0] * (3 - len(v1)) if len(v1) < 3 else v1[:3]
        b = v2 + [0.0] * (3 - len(v2)) if len(v2) < 3 else v2[:3]
        
        return [
            a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0]
        ]


class KronosPlugin:
    def __init__(self, app) -> None:
        self.app = app

    def execute(self) -> None:
        self.app.ui.print_smart(f"{Colors.BOLD}{Colors.CYAN}--- N-МЕРНЫЙ ВЕКТОРНЫЙ АНАЛИЗАТОР ПРОСТРАНСТВА ULTRA V3.0 ---{Colors.RESET}")
        dim = self.app.ui.get_input("Выберите размерность векторов (2-N): ", int, lambda x: x >= 2)
        
        print(f"\n{Colors.GRAY}Введите координаты векторов через пробел (размерность: {dim}):{Colors.RESET}")
        while True:
            raw_v1 = self.app.ui.get_input("  Вектор A: ", str)
            v1 = [float(x) for x in raw_v1.split()]
            if len(v1) != dim:
                self.app.ui.print_error(f"Ошибка: вектор должен содержать ровно {dim} координат!")
                continue
            break

        while True:
            raw_v2 = self.app.ui.get_input("  Вектор B: ", str)
            v2 = [float(x) for x in raw_v2.split()]
            if len(v2) != dim:
                self.app.ui.print_error(f"Ошибка: вектор должен содержать ровно {dim} координат!")
                continue
            break

        try:
            len_a = VectorMath.length(v1)
            len_b = VectorMath.length(v2)
            dot = VectorMath.dot_product(v1, v2)
            rad, deg = VectorMath.angle(v1, v2)
            
            self.app.ui.print_smart(f"\n{Colors.BOLD}{Colors.GREEN}[РЕЗУЛЬТАТЫ ГЕОМЕТРИЧЕСКОГО АНАЛИЗА ЗАПРОСА]:{Colors.RESET}")
            print(f"  • Модуль (длина) вектора A:  {len_a:.4f}")
            print(f"  • Модуль (длина) вектора B:  {len_b:.4f}")
            print(f"  • Скалярное произведение A·B: {Colors.BRIGHT_GREEN}{dot:.4f}{Colors.RESET}")
            print(f"  • Угол между векторами:       {Colors.YELLOW}{deg:.2f}°{Colors.RESET} ({rad:.4f} рад)")
            
            if dim <= 3:
                cross_prod = VectorMath.cross_product(v1, v2)
                area = VectorMath.length(cross_prod)
                
                self.app.ui.print_smart(f"\n{Colors.BOLD}{Colors.CYAN}[ПРОСТРАНСТВЕННЫЕ ХАРАКТЕРИСТИКИ (3D-ФОЛБЕК)]:{Colors.RESET}")
                print(f"  • Векторное произведение A × B: {Colors.BRIGHT_MAGENTA}{cross_prod}{Colors.RESET}")
                print(f"  • Площадь построенного параллелограмма S: {Colors.YELLOW}{area:.4f}{Colors.RESET}")
                
                if dim == 3:
                    raw_v3 = self.app.ui.get_input("\nЖелаете рассчитать смешанное произведение? Введите вектор C (или Enter для пропуска): ", str, allow_empty=True)
                    if raw_v3:
                        v3 = [float(x) for x in raw_v3.split()]
                        if len(v3) != 3:
                            self.app.ui.print_error("Вектор C обязан быть трехмерным!")
                            return
                        
                        triple_prod = VectorMath.dot_product(cross_prod, v3)
                        vol_para = abs(triple_prod)
                        print(f"\n  • Смешанное произведение (A × B) · C: {Colors.BRIGHT_GREEN}{triple_prod:.6g}{Colors.RESET}")
                        print(f"  • Объем параллелепипеда на векторах A, B, C: {Colors.YELLOW}{vol_para:.6g}{Colors.RESET}")
                        print(f"  • Объем пирамиды (тетраэдра): {Colors.YELLOW}{vol_para / 6:.6g}{Colors.RESET}")
                        
                        if abs(triple_prod) < 1e-11:
                            print(f"  • {Colors.BRIGHT_RED}Векторы КОМПЛАНАРНЫ (лежат в одной плоскости). Базис не образуют.{Colors.RESET}")
                        else:
                            print(f"  • {Colors.BRIGHT_GREEN}Векторы линейно независимы. Образуют правый/левый базис в 3D.{Colors.RESET}")
                            
            self.app.history.add("Векторы", f"Анализ {dim}D векторов", f"A·B={dot:.2f}")

        except Exception as e:
            self.app.ui.print_error(f"Критический сбой векторного процессора: {e}")