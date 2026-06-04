# modules/mod_number_theory.py
import math
import secrets
from kronos_core import Colors

METADATA = {
    "id": 7,
    "category": "АЛГЕБРА И ГЕОМЕТРИЯ",
    "name": "Теория чисел (Миллер-Рабин, Факторизация Ферма и Алгоритм Безу)"
}

class NumberTheoryProcessor:
    @staticmethod
    def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = NumberTheoryProcessor.extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

    @staticmethod
    def modular_inverse(a: int, m: int) -> int:
        gcd, x, _ = NumberTheoryProcessor.extended_gcd(a, m)
        if gcd != 1:
            raise ValueError(f"Числа {a} и {m} не взаимно просты! Модульное обратное не существует.")
        return (x % m + m) % m

    @staticmethod
    def is_prime_miller_rabin(n: int, r_rounds: int = 8) -> bool:
        if n < 2: return False
        if n in (2, 3): return True
        if n % 2 == 0: return False

        s = 0
        d = n - 1
        while d % 2 == 0:
            s += 1
            d //= 2

        for _ in range(r_rounds):
            a = secrets.randbelow(n - 3) + 2
            x = pow(a, d, n)
            if x == 1 or x == n - 1:
                continue
            for _ in range(s - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        return True

    @staticmethod
    def factorize_fermat(n: int) -> list[int]:
        if n <= 1: return [] 
        if n % 2 == 0:
            return [2] + NumberTheoryProcessor.factorize_fermat(n // 2)
        if NumberTheoryProcessor.is_prime_miller_rabin(n):
            return [n]

        x = math.isqrt(n) + 1
        y2 = x*x - n
        
        max_iterations = 1000000 
        curr_iter = 0
        
        while curr_iter < max_iterations:
            y = math.isqrt(y2)
            if y*y == y2:
                p = x - y
                q = x + y
                return NumberTheoryProcessor.factorize_fermat(p) + NumberTheoryProcessor.factorize_fermat(q)
            x += 1
            y2 = x*x - n
            curr_iter += 1
            
        return NumberTheoryProcessor._fallback_trial_division(n)

    @staticmethod
    def _fallback_trial_division(n: int) -> list[int]:
        factors = []
        d = 3
        while d * d <= n:
            while n % d == 0:
                factors.append(d)
                n //= d
            d += 2
        if n > 1:
            factors.append(n)
        return factors

    @staticmethod
    def phi_euler(n: int) -> int:
        result = n
        p = 2
        while p * p <= n:
            if n % p == 0:
                while n % p == 0:
                    n //= p
                result -= result // p
            p += 1
        if n > 1:
            result -= result // n
        return result


class KronosPlugin:
    def __init__(self, app) -> None:
        self.app = app

    def execute(self) -> None:
        self.app.ui.print_smart(f"{Colors.BOLD}{Colors.CYAN}--- КИБЕРНЕТИЧЕСКИЙ КOМПЛЕКС ТЕОРИИ ЧИСЕЛ ULTRA V3.0 ---{Colors.RESET}")
        print(" Выберите математическую операцию:")
        print("  [1] Криптостойкий тест на простоту (Миллер-Рабин для больших чисел)")
        print("  [2] Каноническая факторизация числа (Метод Ферма)")
        print("  [3] Диофантовы уравнения и соотношение Безу (НОД, НОК, Линейные коэффициенты)")
        print("  [4] Вычисление Функции Эйлера и модульного обратного (Инженерия RSA)")
        
        choice = self.app.ui.get_input("Модуль: ", int, lambda x: 1 <= x <= 4)
        
        try:
            if choice == 1:
                n = self.app.ui.get_input("\nВведите целое число для проверки: ", int)
                self.app.ui.print_smart(f"\n{Colors.BOLD}{Colors.GREEN}[АНАЛИЗ ЧИСЛА]:{Colors.RESET}")
                
                if n < 2:
                    print(f"  • Число {n} является: {Colors.YELLOW}НЕ ОПРЕДЕЛЕННЫМ{Colors.RESET} (в теории простых чисел рассматриваются N > 1)")
                else:
                    is_prime = NumberTheoryProcessor.is_prime_miller_rabin(n)
                    status = f"{Colors.BRIGHT_GREEN}ПРОСТОЕ{Colors.RESET}" if is_prime else f"{Colors.BRIGHT_RED}СОСТАВНОЕ{Colors.RESET}"
                    print(f"  • Число {n} является: {status}")
                self.app.history.add("ТеорияЧисел", f"Тест простоты {n}", "Завершено")

            elif choice == 2:
                n = self.app.ui.get_input("\nВведите число для разложения на множители: ", int, lambda x: x > 1)
                self.app.ui.print_smart(f"\n{Colors.GRAY}Запуск квантового движка факторизации Ферма...{Colors.RESET}")
                factors = sorted(NumberTheoryProcessor.factorize_fermat(n))
                
                self.app.ui.print_smart(f"\n{Colors.BOLD}{Colors.GREEN}[КАНОНИЧЕСКОЕ РАЗЛОЖЕНИЕ]:{Colors.RESET}")
                print(f"  • Перечень простых множителей: {Colors.BRIGHT_CYAN}{factors}{Colors.RESET}")
                
                unique_factors = sorted(list(set(factors)))
                form_str = " * ".join(f"{p}^" + f"{factors.count(p)}" for p in unique_factors)
                print(f"  • Математический вид: {Colors.YELLOW}{form_str}{Colors.RESET}")
                self.app.history.add("ТеорияЧисел", f"Факторизация {n}", str(factors))

            elif choice == 3:
                a = self.app.ui.get_input("\nВведите число a = ", int)
                b = self.app.ui.get_input("Введите число b = ", int)
                
                gcd, x, y = NumberTheoryProcessor.extended_gcd(a, b)
                lcm = abs(a * b) // gcd if gcd != 0 else 0
                
                self.app.ui.print_smart(f"\n{Colors.BOLD}{Colors.GREEN}[РАСШИРЕННЫЕ МЕТРИКИ ЕВКЛИДА]:{Colors.RESET}")
                print(f"  • НОД({a}, {b}) = {Colors.BRIGHT_GREEN}{gcd}{Colors.RESET}")
                print(f"  • НОК({a}, {b}) = {Colors.BRIGHT_GREEN}{lcm}{Colors.RESET}")
                print(f"  • Линейное соотношение Безу: {Colors.YELLOW}{a}*({x}) + {b}*({y}) = {gcd}{Colors.RESET}")
                self.app.history.add("ТеорияЧисел", f"Евклид {a} и {b}", f"НОД={gcd}")

            elif choice == 4:
                n = self.app.ui.get_input("\nВведите базовое число N = ", int, lambda x: x > 0)
                phi = NumberTheoryProcessor.phi_euler(n)
                self.app.ui.print_smart(f"\n{Colors.BOLD}{Colors.GREEN}[ИНЖЕНЕРНЫЙ АНАЛИЗ]:{Colors.RESET}")
                print(f"  • Функция Эйлера φ({n}) = {Colors.BRIGHT_CYAN}{phi}{Colors.RESET} (чисел, взаимно простых с {n})")
                
                ask_inv = self.app.ui.get_input("\nХотите найти модульное обратное число (вычислить приватную экспоненту)? (1-Да, 0-Нет): ", int, lambda x: x in (0, 1))
                if ask_inv == 1:
                    a = self.app.ui.get_input("Введите число a (взаимно простое с N): ", int)
                    inv = NumberTheoryProcessor.modular_inverse(a, n)
                    print(f"  • Модульное обратное ({a}^-1 mod {n}) = {Colors.BRIGHT_GREEN}{inv}{Colors.RESET}")
                    print(f"    Проверка: ({a} * {inv}) mod {n} = {(a * inv) % n}")
                self.app.history.add("ТеорияЧисел", f"Анализ RSA для {n}", f"phi={phi}")

        except Exception as e:
            self.app.ui.print_error(f"Теоретико-числовой сбой: {e}")