# modules/mod_depreciation.py
from kronos_core import Colors

METADATA = {
    "id": 19,
    "category": "ФИНАНСОВАЯ МАТЕМАТИКА",
    "name": "Амортизация активов (Профессиональные методы износа и Учет нагрузки)"
}

class DepreciationEngine:
    @staticmethod
    def straight_line(cost: float, salvage: float, years: int) -> list[tuple[int, float, float]]:
        annual_dep = (cost - salvage) / years
        schedule = []
        current_value = cost
        for y in range(1, years + 1):
            current_value -= annual_dep
            schedule.append((y, annual_dep, max(salvage, current_value)))
        return schedule

    @staticmethod
    def declining_balance(cost: float, salvage: float, years: int, factor: float = 2.0) -> list[tuple[int, float, float]]:
        rate = (1.0 / years) * factor
        schedule = []
        current_value = cost
        
        for y in range(1, years + 1):
            if current_value <= salvage:
                dep_amount = 0.0
            else:
                dep_amount = current_value * rate
                if current_value - dep_amount < salvage:
                    dep_amount = current_value - salvage
            
            current_value -= dep_amount
            schedule.append((y, dep_amount, max(salvage, current_value)))
        return schedule

    @staticmethod
    def sum_of_years_digits(cost: float, salvage: float, years: int) -> list[tuple[int, float, float]]:
        syd = (years * (years + 1)) // 2
        depreciable_base = cost - salvage
        schedule = []
        current_value = cost
        for y in range(1, years + 1):
            remaining_life = years - y + 1
            dep_amount = depreciable_base * (remaining_life / syd)
            current_value -= dep_amount
            schedule.append((y, dep_amount, max(salvage, current_value)))
        return schedule


class KronosPlugin:
    def __init__(self, app) -> None:
        self.app = app

    def _print_table(self, schedule: list[tuple[int, float, float]]) -> None:
        print(f"  {Colors.GRAY}{'Год':<6}{'Списание за период':<22}{'Остаточная стоимость (Book Value)':<25}{Colors.RESET}")
        print("  " + "─" * 58)
        for y, dep, val in schedule:
            print(f"   {y:<5} {Colors.BRIGHT_CYAN}{dep:<21.2f}{Colors.RESET} {Colors.BRIGHT_GREEN}{val:<24.2f}{Colors.RESET}")

    def execute(self) -> None:
        self.app.ui.print_smart(f"{Colors.BOLD}{Colors.CYAN}--- ИНЖЕНЕРНО-ЭКОНОМИЧЕСКИЙ АМОРТИЗАЦИОННЫЙ СТЕНД ULTRA V3.0 ---{Colors.RESET}")
        print(" Модуль осуществляет аудит износа основных средств и долгосрочных активов.")
        
        try:
            cost = self.app.ui.get_input("\nПервоначальная балансовая стоимость актива (Cost): ", float, lambda x: x > 0)
            salvage = self.app.ui.get_input("Ликвидационная стоимость (Salvage Value в конце срока): ", float, lambda x: x >= 0)
            
            if salvage >= cost:
                self.app.ui.print_error("Ликвидационная стоимость не может быть больше или равна первоначальной!")
                return

            print(f"\n{Colors.YELLOW}Доступные методы учета износа:{Colors.RESET}")
            print("  [1] Линейный метод (Straight-Line) — классическое равномерное списание")
            print("  [2] Метод уменьшаемого остатка (Declining Balance) — ускоренное списание")
            print("  [3] Метод суммы чисел лет (SYD) — кумулятивное ускоренное списание")
            print("  [4] Производственный метод (Units of Production) — списание по фактической нагрузке")
            
            method = self.app.ui.get_input("\nВыберите метод: ", int, lambda x: 1 <= x <= 4)
            tax_rate = self.app.ui.get_input("Ставка налога на прибыль компании (%, например 20): ", float, lambda x: 0 <= x < 100) / 100

            schedule = []
            total_depreciated = 0.0

            if method in (1, 2, 3):
                years = self.app.ui.get_input("Срок полезного использования актива (лет): ", int, lambda x: x > 0)
                
                if method == 1:
                    schedule = DepreciationEngine.straight_line(cost, salvage, years)
                elif method == 2:
                    factor = self.app.ui.get_input("Коэффициент ускорения износа (обычно 2.0 - двойной баланс): ", float, lambda x: x > 0)
                    schedule = DepreciationEngine.declining_balance(cost, salvage, years, factor)
                elif method == 3:
                    schedule = DepreciationEngine.sum_of_years_digits(cost, salvage, years)
                
                self.app.ui.print_smart(f"\n{Colors.BOLD}{Colors.GREEN}[АМОРТИЗАЦИОННАЯ ВЕДОМОСТЬ]:{Colors.RESET}")
                self._print_table(schedule)
                total_depreciated = sum(item[1] for item in schedule)

            elif method == 4:
                print(f"\n{Colors.YELLOW}--- РАСЧЕТ ПО ФАКТИЧЕСКОМУ РЕСУРСУ НАГРУЗКИ ---{Colors.RESET}")
                total_capacity = self.app.ui.get_input("Максимальный жизненный ресурс актива: ", float, lambda x: x > 0)
                current_units = self.app.ui.get_input("Фактическая выработка (нагрузка) за текущий отчетный период: ", float, lambda x: x >= 0)
                
                if current_units > total_capacity:
                    self.app.ui.print_error("Текущая выработка не может превышать общий жизненный ресурс!")
                    return
                
                rate_per_unit = (cost - salvage) / total_capacity
                period_dep = current_units * rate_per_unit
                book_value = max(salvage, cost - period_dep)
                period_dep = cost - book_value
                
                self.app.ui.print_smart(f"\n{Colors.BOLD}{Colors.GREEN}[АНАЛИЗ ФАКТИЧЕСКОГО ИЗНОСА]:{Colors.RESET}")
                print(f"  • Норма списания на единицу выработки: {rate_per_unit:.5f}")
                print(f"  • Амортизационные отчисления за период: {Colors.BRIGHT_CYAN}{period_dep:.2f}{Colors.RESET}")
                print(f"  • Остаточная стоимость актива (Book Value): {Colors.BRIGHT_GREEN}{book_value:.2f}{Colors.RESET}")
                total_depreciated = period_dep

            tax_shield = total_depreciated * tax_rate
            if tax_shield > 0:
                self.app.ui.print_smart(f"\n{Colors.BOLD}{Colors.MAGENTA}[НАЛОГОВОЙ АУДИТ KRONOS]:{Colors.RESET}")
                print(f"  • Сформированный Налоговый Щит (Tax Shield): {Colors.YELLOW}{tax_shield:.2f}{Colors.RESET}")
                print(f"    {Colors.GRAY}(Эта сумма легально уменьшит налогооблагаемую базу вашей организации за расчетный период){Colors.RESET}")

            self.app.history.add("Финансы", f"Амортизация актива ({cost:.0f})", f"Списано={total_depreciated:.2f}")

        except Exception as e:
            self.app.ui.print_error(f"Ошибка амортизационного процессора: {e}")