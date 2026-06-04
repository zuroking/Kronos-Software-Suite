# modules/mod_fin_inflation.py
import math
from kronos_core import Colors

METADATA = {
    "id": 18,
    "category": "ФИНАНСОВАЯ МАТЕМАТИКА",
    "name": "Калькулятор инфляции (Сложные проценты, Капитализация и FV)"
}

class InflationEngine:
    @staticmethod
    def compound_interest_with_deposits(principal: float, annual_rate: float, years: float, 
                                        compounding_periods: int, periodic_deposit: float, 
                                        deposit_frequency: int) -> tuple[float, float]:
        r = annual_rate / 100
        t = years
        
        total_compounding_steps = int(t * compounding_periods)
        rate_per_period = r / compounding_periods
        
        fv_principal = principal * ((1 + rate_per_period) ** total_compounding_steps)
        
        fv_deposits = 0.0
        actual_deposited_funds = 0.0
        
        if periodic_deposit > 0:
            total_deposits = int(t * deposit_frequency)
            deposit_step_in_years = 1.0 / deposit_frequency
            
            for i in range(total_deposits):
                time_remaining = t - (i * deposit_step_in_years)
                if time_remaining > 0:
                    fv_deposits += periodic_deposit * ((1 + rate_per_period) ** (time_remaining * compounding_periods))
                    actual_deposited_funds += periodic_deposit
        
        total_fv = fv_principal + fv_deposits
        total_invested = principal + actual_deposited_funds
        
        return total_fv, total_invested

    @staticmethod
    def calculate_inflation_erosion(amount: float, inflation_rate: float, years: float) -> tuple[float, float]:
        inf_r = inflation_rate / 100
        eroded_value = amount / ((1 + inf_r) ** years)
        loss = amount - eroded_value
        return eroded_value, loss


class KronosPlugin:
    def __init__(self, app) -> None:
        self.app = app

    def execute(self) -> None:
        self.app.ui.print_smart(f"{Colors.BOLD}{Colors.CYAN}--- ФИНАНСОВЫЙ СИМУЛЯТОР СТОИМОСТИ КАПИТАЛА ULTRA V3.0 ---{Colors.RESET}")
        print(" Выберите режим анализа:")
        print("  [1] Калькулятор сложных процентов и накоплений (Депозиты + Капитализация)")
        print("  [2] Калькулятор инфляции (Обесценивание капитала и покупательская способность)")
        
        choice = self.app.ui.get_input("Режим: ", int, lambda x: x in (1, 2))
        
        try:
            if choice == 1:
                print(f"\n{Colors.YELLOW}--- НАСТРОЙКА ИНВЕСТИЦИОННОГО ДЕПОЗИТА ---{Colors.RESET}")
                principal = self.app.ui.get_input("Начальная сумма вложений: ", float, lambda x: x >= 0)
                annual_rate = self.app.ui.get_input("Годовая процентная ставка доходности (%): ", float, lambda x: x >= 0)
                years = self.app.ui.get_input("Срок размещения капитала (лет): ", float, lambda x: x > 0)
                
                print(f"\n{Colors.GRAY}Периодичность капитализации: 1-раз в год, 4-поквартально, 12-ежемесячно, 365-ежедневно{Colors.RESET}")
                comp_periods = self.app.ui.get_input("Частота начисления процентов в год: ", int, lambda x: x in (1, 4, 12, 365))
                
                periodic_dep = self.app.ui.get_input("\nСумма регулярного пополнения (0 если нет): ", float, lambda x: x >= 0)
                dep_freq = 12
                if periodic_dep > 0:
                    dep_freq = self.app.ui.get_input("Частота пополнений в год (1-раз в год, 12-ежемесячно): ", int, lambda x: x in (1, 12))
                
                target_inflation = self.app.ui.get_input("Ожидаемая инфляция для расчёта реальной доходности (%): ", float, lambda x: x >= 0)
                
                fv, invested = InflationEngine.compound_interest_with_deposits(
                    principal, annual_rate, years, comp_periods, periodic_dep, dep_freq
                )
                
                self.app.ui.print_smart(f"\n{Colors.BOLD}{Colors.GREEN}[АНАЛИЗ РОСТА НАКОПЛЕНИЙ]:{Colors.RESET}")
                print(f"  • Всего лично вами вложено средств: {invested:.2f}")
                print(f"  • Итоговая сумма на счету (FV):     {Colors.BRIGHT_GREEN}{fv:.2f}{Colors.RESET}")
                print(f"  • Чистый доход от сложных процентов: {Colors.BRIGHT_CYAN}{fv - invested:.2f}{Colors.RESET}")
                
                real_fv = fv / ((1 + (target_inflation / 100)) ** years)
                print(f"  • Реальная ценность капитала (с поправкой на инфляцию {target_inflation}%): {Colors.YELLOW}{real_fv:.2f}{Colors.RESET}")
                
                self.app.history.add("Финансы", f"Депозит {principal:.0f} на {years} л.", f"FV={fv:.2f}")

            elif choice == 2:
                print(f"\n{Colors.YELLOW}--- АНАЛИЗ ИНФЛЯЦИОННЫХ РИСКОВ ---{Colors.RESET}")
                amount = self.app.ui.get_input("Введите текущую сумму капитала: ", float, lambda x: x > 0)
                inflation_rate = self.app.ui.get_input("Ожидаемый среднегодовой темп инфляции (%): ", float, lambda x: x >= 0)
                years = self.app.ui.get_input("Горизонт прогнозирования (лет): ", float, lambda x: x > 0)
                
                eroded, loss = InflationEngine.calculate_inflation_erosion(amount, inflation_rate, years)
                purchasing_power_index = (eroded / amount) * 100
                
                self.app.ui.print_smart(f"\n{Colors.BOLD}{Colors.RED}[РЕЗУЛЬТАТ ОБЕСЦЕНИВАНИЯ]:{Colors.RESET}")
                print(f"  • Номинальная сумма останется прежней: {amount:.2f}")
                print(f"  • Реальная покупательская способность через {years} лет: {Colors.BRIGHT_RED}{eroded:.2f}{Colors.RESET}")
                print(f"  • Прямые чистые потери от инфляции:     {loss:.2f}")
                print(f"  • Индекс ценности ваших денег:          {Colors.YELLOW}{purchasing_power_index:.2f}%{Colors.RESET}")
                
                if purchasing_power_index < 50:
                    print(f"  • {Colors.BRIGHT_RED}ВНИМАНИЕ: За указанный период деньги обесценятся более чем в два раза! Требуется хеджирование активов.{Colors.RESET}")
                else:
                    print(f"  • {Colors.GREEN}Оценка стабильности: Риски умеренные.{Colors.RESET}")
                    
                self.app.history.add("Финансы", f"Инфляция {amount:.0f} под {inflation_rate}%", f"Реальный остаток={eroded:.2f}")

        except Exception as e:
            self.app.ui.print_error(f"Ошибка процессора временной стоимости денег: {e}")