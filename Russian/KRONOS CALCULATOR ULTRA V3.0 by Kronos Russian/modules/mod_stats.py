# modules/mod_stats.py
import math
from collections import Counter
from kronos_core import Colors

METADATA = {
    "id": 11,
    "category": "ИНЖЕНЕРИЯ И АНАЛИТИКА",
    "name": "Статистический анализ массивов данных (Дескриптивное Ядро)"
}

class StatisticsProcessor:
    @staticmethod
    def calculate_modes(data: list[float]) -> list[float]:
        if not data: return []
        counts = Counter(data)
        max_count = max(counts.values())
        if max_count == 1 and len(data) > 1:
            return []
        return [k for k, v in counts.items() if v == max_count]

    @staticmethod
    def analyze_array(data: list[float]) -> dict:
        n = len(data)
        if n < 2:
            raise ValueError("Для полноценного статистического анализа выборки требуется минимум 2 числа!")

        sorted_data = sorted(data)
        
        mean = sum(data) / n
        mid = n // 2
        if n % 2 != 0:
            median = sorted_data[mid]
        else:
            median = (sorted_data[mid - 1] + sorted_data[mid]) / 2.0
            
        modes = StatisticsProcessor.calculate_modes(data)
        
        v_min, v_max = sorted_data[0], sorted_data[-1]
        v_range = v_max - v_min
        
        variance = sum((x - mean) ** 2 for x in data) / (n - 1)
        stdev = math.sqrt(variance)
        cv = (stdev / mean * 100) if mean != 0 else 0.0
        
        q1_idx = int(n * 0.25)
        q3_idx = int(n * 0.75)
        q1 = sorted_data[q1_idx]
        q3 = sorted_data[q3_idx]
        iqr = q3 - q1
        
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outliers = [x for x in data if x < lower_bound or x > upper_bound]

        return {
            "n": n, "mean": mean, "median": median, "modes": modes,
            "min": v_min, "max": v_max, "range": v_range,
            "variance": variance, "stdev": stdev, "cv": cv,
            "q1": q1, "q3": q3, "iqr": iqr, "outliers": outliers
        }


class KronosPlugin:
    def __init__(self, app) -> None:
        self.app = app

    def execute(self) -> None:
        self.app.ui.print_smart(f"{Colors.BOLD}{Colors.CYAN}--- СТАТИСТИЧЕСКИЙ АНАЛИТИЧЕСКИЙ КОМПЛЕКС ULTRA V3.0 ---{Colors.RESET}")
        print("Введите числовой массив данных (можно использовать пробелы, запятые и смешанный текст):")
        
        try:
            raw_input = self.app.ui.get_input("  Данные: ", str)
            normalized_input = raw_input.replace(",", ".")
            
            data = []
            ignored_tokens = []
            
            for token in normalized_input.split():
                try:
                    data.append(float(token))
                except ValueError:
                    ignored_tokens.append(token)
            
            if ignored_tokens:
                print(f"{Colors.YELLOW}  [ПРЕДУПРЕЖДЕНИЕ] Игнорирован нечисловой мусор: {ignored_tokens}{Colors.RESET}")
                
            res = StatisticsProcessor.analyze_array(data)
            
            self.app.ui.print_smart(f"\n{Colors.BOLD}{Colors.GREEN}[МЕТРИКИ ЦЕНТРАЛЬНОЙ ТЕНДЕНЦИИ]:{Colors.RESET}")
            print(f"  • Размер выборки (N):         {res['n']}")
            print(f"  • Среднее арифметическое (X): {Colors.BRIGHT_GREEN}{res['mean']:.4f}{Colors.RESET}")
            print(f"  • Медиана (Median):           {Colors.BRIGHT_GREEN}{res['median']:.4f}{Colors.RESET}")
            
            if res['modes']:
                print(f"  • Мода (Mode):                {Colors.BRIGHT_GREEN}{res['modes']}{Colors.RESET}")
            else:
                print(f"  • Мода (Mode):                Отсутствует (все значения уникальны)")

            self.app.ui.print_smart(f"\n{Colors.BOLD}{Colors.YELLOW}[АНАЛИЗ ВАРИАЦИИ И РАЗБРОСА]:{Colors.RESET}")
            print(f"  • Размах выборки (Range):     {res['range']:.4f} (от {res['min']} до {res['max']})")
            print(f"  • Исправленная Дисперсия:     {res['variance']:.6f}")
            print(f"  • Стандартное отклонение (σ): {Colors.BRIGHT_CYAN}{res['stdev']:.4f}{Colors.RESET}")
            print(f"  • Коэффициент вариации (V):   {res['cv']:.2f}%")
            
            if res['cv'] < 33: homogeneity = "Однородная выборка"
            else: homogeneity = "Неоднородная выборка (высокий разброс)"
            print(f"  • Структурная оценка:         {Colors.WHITE}{homogeneity}{Colors.RESET}")

            self.app.ui.print_smart(f"\n{Colors.BOLD}{Colors.MAGENTA}[ИНТЕРКВАРТИЛЬНЫЙ АНАЛИЗ (IQR)]:{Colors.RESET}")
            print(f"  • 25-й перцентиль (Q1):       {res['q1']:.4f}")
            print(f"  • 75-й перцентиль (Q3):       {res['q3']:.4f}")
            print(f"  • Межквартильный размах (IQR):{res['iqr']:.4f}")

            print(f"\n{Colors.BOLD}{Colors.RED}[ФИЛЬТРАЦИЯ СТАТИСТИЧЕСКИХ ВЫБРОСОВ]:{Colors.RESET}")
            if res['outliers']:
                print(f"  • Обнаружены аномальные выбросы ({len(res['outliers'])} шт.): {Colors.BRIGHT_RED}{res['outliers']}{Colors.RESET}")
            else:
                print(f"  • {Colors.GREEN}Критических аномалий и выбросов не обнаружено.{Colors.RESET}")

            self.app.history.add("Статистика", f"Анализ выборки N={res['n']}", f"Mean={res['mean']:.2f}, СКО={res['stdev']:.2f}")

        except Exception as e:
            self.app.ui.print_error(f"Ошибка статистического процессора: {e}")