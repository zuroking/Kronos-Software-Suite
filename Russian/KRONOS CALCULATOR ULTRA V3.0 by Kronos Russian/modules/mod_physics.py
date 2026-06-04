# modules/mod_physics.py
import math
import cmath
from typing import Optional
from kronos_core import Colors

METADATA = {
    "id": 9,
    "category": "ИНЖЕНЕРИЯ И АНАЛИТИКА",
    "name": "Физика (Кинематика, Динамика Ньютона и RLC-цепи)"
}

class PhysicsEngine:
    @staticmethod
    def solve_kinematics(v0: Optional[float], v: Optional[float], a: Optional[float], t: Optional[float], s: Optional[float]) -> dict[str, float]:
        known = {k: v for k, v in {"v0": v0, "v": v, "a": a, "t": t, "s": s}.items() if v is not None}
        
        if len(known) < 3:
            raise ValueError("Для решения кинематики необходимо ввести как минимум 3 известных параметра!")

        if "t" in known and known["t"] < 0:
            raise ValueError("Время движения не может быть отрицательным!")

        iterations = 0
        while len(known) < 5 and iterations < 5:
            iterations += 1
            if "v0" in known and "a" in known and "t" in known and "v" not in known:
                known["v"] = known["v0"] + known["a"] * known["t"]
            if "v" in known and "a" in known and "t" in known and "v0" not in known:
                known["v0"] = known["v"] - known["a"] * known["t"]
            if "v" in known and "v0" in known and "t" in known and "a" not in known:
                if known["t"] != 0:
                    known["a"] = (known["v"] - known["v0"]) / known["t"]
            if "v" in known and "v0" in known and "a" in known and "t" not in known:
                if known["a"] != 0:
                    val = (known["v"] - known["v0"]) / known["a"]
                    if val < 0: raise ValueError("Парадоксальные условия: расчетное время отрицательное!")
                    known["t"] = val

            if "v0" in known and "a" in known and "t" in known and "s" not in known:
                known["s"] = known["v0"] * known["t"] + 0.5 * known["a"] * (known["t"] ** 2)
            if "v" in known and "v0" in known and "a" in known and "s" not in known:
                if known["a"] != 0:
                    known["s"] = (known["v"] ** 2 - known["v0"] ** 2) / (2 * known["a"])
            if "s" in known and "t" in known and "v0" in known and "a" not in known:
                if known["t"] != 0:
                    known["a"] = 2 * (known["s"] - known["v0"] * known["t"]) / (known["t"] ** 2)
            if "s" in known and "t" in known and "a" in known and "v0" not in known:
                if known["t"] != 0:
                    known["v0"] = (known["s"] - 0.5 * known["a"] * (known["t"] ** 2)) / known["t"]
            if "v" in known and "v0" in known and "s" in known and "a" not in known:
                if known["s"] != 0:
                    known["a"] = (known["v"] ** 2 - known["v0"] ** 2) / (2 * known["s"])

        if all(k in known for k in ["v", "v0", "a", "t"]):
            v_calc = known["v0"] + known["a"] * known["t"]
            if not math.isclose(known["v"], v_calc, abs_tol=1e-4):
                raise ValueError(f"Физическое противоречие! Скорость v={known['v']} не совпадает с расчетной {v_calc:.4g}")

        if all(k in known for k in ["s", "v0", "a", "t"]):
            s_calc = known["v0"] * known["t"] + 0.5 * known["a"] * (known["t"] ** 2)
            if not math.isclose(known["s"], s_calc, abs_tol=1e-4):
                raise ValueError(f"Физическое противоречие! Путь s={known['s']} не совпадает с расчетным {s_calc:.4g}")

        return known

    @staticmethod
    def calculate_ac_impedance(R: float, L: float, C: float, f: float) -> tuple[complex, float, float]:
        omega = 2 * math.pi * f
        XL = omega * L if L > 0 else 0.0
        XC = 1 / (omega * C) if C > 0 else 0.0
        
        Z = complex(R, XL - XC)
        phase_rad = cmath.phase(Z)
        return Z, abs(Z), math.degrees(phase_rad)


class KronosPlugin:
    def __init__(self, app) -> None:
        self.app = app

    def execute(self) -> None:
        self.app.ui.print_smart(f"{Colors.BOLD}{Colors.CYAN}--- ФИЗИЧЕСКИЙ ВЫЧИСЛИТЕЛЬНЫЙ КОМПЛЕКС ULTRA V3.0 ---{Colors.RESET}")
        print(" Выберите физический модуль:")
        print("  [1] Кинематический Солвер (Анализ равноускоренного движения)")
        print("  [2] Динамика, Энергия и Мощность (Законы Ньютона)")
        print("  [3] Электротехника (Расчет комплексного импеданса RLC-цепей AC)")
        
        choice = self.app.ui.get_input("Действие: ", int, lambda x: 1 <= x <= 3)
        
        try:
            if choice == 1:
                print(f"\n{Colors.YELLOW}Введите известные параметры (нажмите Enter для пропуска):{Colors.RESET}")
                v0 = self.app.ui.get_input("  Начальная скорость v0 (м/с): ", float, allow_empty=True)
                v  = self.app.ui.get_input("  Конечная скорость v   (м/с): ", float, allow_empty=True)
                a  = self.app.ui.get_input("  Ускорение a           (м/с²): ", float, allow_empty=True)
                t  = self.app.ui.get_input("  Время движения t        (с): ", float, allow_empty=True)
                s  = self.app.ui.get_input("  Расстояние (путь) s     (м): ", float, allow_empty=True)
                
                res = PhysicsEngine.solve_kinematics(v0, v, a, t, s)
                self.app.ui.print_smart(f"\n{Colors.BOLD}{Colors.GREEN}[КИНЕМАТИЧЕСКИЙ ПРОФИЛЬ ДВИЖЕНИЯ]:{Colors.RESET}")
                for k, val in res.items():
                    print(f"  • {k} = {Colors.BRIGHT_GREEN}{val:.6g}{Colors.RESET}")
                self.app.history.add("Физика", "Кинематика", f"Решено параметров: {len(res)}")

            elif choice == 2:
                print(f"\n{Colors.YELLOW}--- ДИНАМИКА И ЭНЕРГЕТИКА ---{Colors.RESET}")
                m = self.app.ui.get_input("Введите массу тела m (кг): ", float, lambda x: x > 0)
                v = self.app.ui.get_input("Введите скорость тела v (м/с): ", float)
                h = self.app.ui.get_input("Введите высоту над поверхностью h (м): ", float)
                f_net = self.app.ui.get_input("Введите результирующую силу F (Ньютоны), если известна (или 0): ", float)
                
                p = m * v
                e_k = 0.5 * m * (v ** 2)
                e_p = m * 9.80665 * h
                
                self.app.ui.print_smart(f"\n{Colors.BOLD}{Colors.GREEN}[ДИНАМИЧЕСКИЙ И ЭНЕРГЕТИЧЕСКИЙ АНАЛИЗ]:{Colors.RESET}")
                print(f"  • Импульс тела (p): {p:.4g} кг·м/с")
                print(f"  • Кинетическая энергия (E_k): {Colors.BRIGHT_GREEN}{e_k:.6g}{Colors.RESET} Дж")
                print(f"  • Потенциальная энергия (E_p): {Colors.BRIGHT_GREEN}{e_p:.6g}{Colors.RESET} Дж")
                print(f"  • Полная механическая энергия (E): {e_k + e_p:.6g} Дж")
                if f_net != 0:
                    print(f"  • Ускорение тела под действием силы (a = F/m): {f_net / m:.4g} м/с²")
                self.app.history.add("Физика", "Динамика", f"Ek={e_k:.2f} J")

            elif choice == 3:
                print(f"\n{Colors.YELLOW}--- РАСЧЕТ ЦЕПЕЙ ПЕРЕМЕННОГО ТОКА (RLC) ---{Colors.RESET}")
                R = self.app.ui.get_input("Активное сопротивление R (Ом): ", float, lambda x: x >= 0)
                L = self.app.ui.get_input("Индуктивность L (Гн): ", float, lambda x: x >= 0)
                C = self.app.ui.get_input("Емкость C (Ф): ", float, lambda x: x >= 0)
                f = self.app.ui.get_input("Частота переменного тока f (Гц): ", float, lambda x: x > 0)
                v_rms = self.app.ui.get_input("Действующее напряжение V_rms (В): ", float, lambda x: x > 0)
                
                Z, z_mod, phase_deg = PhysicsEngine.calculate_ac_impedance(R, L, C, f)
                
                if z_mod == 0:
                    raise ValueError("Полное сопротивление равно нулю (Резонансное короткое замыкание)!")
                
                i_rms = v_rms / z_mod
                
                self.app.ui.print_smart(f"\n{Colors.BOLD}{Colors.GREEN}[ХАРАКТЕРИСТИКИ ЦЕПИ ПЕРЕМЕННОГО ТОКА]:{Colors.RESET}")
                sign = "+" if Z.imag >= 0 else "-"
                print(f"  • Комплексный Импеданс Z:  {Colors.WHITE}{Z.real:.4g} {sign} {abs(Z.imag):.4g}j{Colors.RESET} Ом")
                print(f"  • Полное сопротивление |Z|: {Colors.BRIGHT_GREEN}{z_mod:.4g}{Colors.RESET} Ом")
                print(f"  • Действующий ток I_rms:    {Colors.BRIGHT_CYAN}{i_rms:.4g}{Colors.RESET} А")
                print(f"  • Сдвиг фаз (угол φ):       {Colors.YELLOW}{phase_deg:.2f}°{Colors.RESET}")
                
                if abs(Z.imag) < 1e-6: character = "Чисто активный (Резонанс напряжений)"
                elif Z.imag > 0: character = "Активно-индуктивный"
                else: character = "Активно-емкостный"
                print(f"  • Характер нагрузки цепи:  {Colors.MAGENTA}{character}{Colors.RESET}")
                
                self.app.history.add("Физика", "RLC Импеданс", f"|Z|={z_mod:.2f} Ohm, I={i_rms:.2f} A")

        except Exception as e:
            self.app.ui.print_error(f"Физический сбой расчетов: {e}")