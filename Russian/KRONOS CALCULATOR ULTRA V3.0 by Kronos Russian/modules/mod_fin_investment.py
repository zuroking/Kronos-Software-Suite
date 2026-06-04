# modules/mod_fin_investment.py
from kronos_core import Colors

METADATA = {
    "id": 17,
    "category": "ФИНАНСОВАЯ МАТЕМАТИКА",
    "name": "Инвестиционный анализ (NPV, Дисконтированная окупаемость и Стресс-тест)"
}

class InvestmentEngine:
    @staticmethod
    def calculate_metrics(initial_investment: float, rate: float, cash_flows: list[float]) -> dict:
        npv = -initial_investment
        present_values = []
        total_nominal_return = sum(cash_flows)
        
        for idx, cf in enumerate(cash_flows):
            pv = cf / ((1 + rate) ** (idx + 1))
            present_values.append(pv)
            npv += pv

        sum_pv = npv + initial_investment
        pi = sum_pv / initial_investment if initial_investment > 0 else 0.0

        roi = ((total_nominal_return - initial_investment) / initial_investment) * 100

        cumulative_pv = -initial_investment
        dpbp = None
        
        for idx, pv in enumerate(present_values):
            next_cumulative = cumulative_pv + pv
            if cumulative_pv < 0 and next_cumulative >= 0:
                fraction = abs(cumulative_pv) / pv if pv > 0 else 0.0
                dpbp = idx + fraction
                break
            cumulative_pv = next_cumulative

        return {
            "npv": npv,
            "pi": pi,
            "roi": roi,
            "dpbp": dpbp,
            "total_nominal": total_nominal_return
        }


class KronosPlugin:
    def __init__(self, app) -> None:
        self.app = app

    def execute(self) -> None:
        self.app.ui.print_smart(f"{Colors.BOLD}{Colors.CYAN}--- ИНВЕСТИЦИОННЫЙ АНАЛИТИЧЕСКИЙ КОМПЛЕКС ULTRA V3.0 ---{Colors.RESET}")
        print(" Модуль проводит глубокую экспертизу коммерческой эффективности стартапов и активов.")
        
        try:
            initial_investment = self.app.ui.get_input("\nВведите сумму начальных вложений (капитальные затраты): ", float, lambda x: x > 0)
            rate_pct = self.app.ui.get_input("Ставка дисконтирования / барьерная ставка расчетов (%): ", float, lambda x: x >= 0)
            years = self.app.ui.get_input("Горизонт планирования проекта (сколько лет): ", int, lambda x: x > 0)
            
            rate = rate_pct / 100
            cash_flows = []
            
            print(f"\n{Colors.YELLOW}Введите прогнозируемый чистый денежный поток (Cash Flow) по годам:{Colors.RESET}")
            for y in range(1, years + 1):
                cf = self.app.ui.get_input(f"  Конец года {y} (доход/прибыль): ", float)
                cash_flows.append(cf)
                
            res = InvestmentEngine.calculate_metrics(initial_investment, rate, cash_flows)
            
            self.app.ui.print_smart(f"\n{Colors.BOLD}{Colors.GREEN}[ЭФФЕКТИВНОСТЬ БИЗНЕС-МОДЕЛИ]:{Colors.RESET}")
            print(f"  • Номинальная валовая прибыль:       {res['total_nominal']:.2f}")
            print(f"  • Рентабельность инвестиций (ROI):   {Colors.BRIGHT_GREEN}{res['roi']:.2f}%{Colors.RESET}")
            
            npv_color = Colors.BRIGHT_GREEN if res['npv'] >= 0 else Colors.BRIGHT_RED
            print(f"  • Чистый приведенный доход (NPV):   {npv_color}{res['npv']:.2f}{Colors.RESET}")
            
            pi_color = Colors.BRIGHT_GREEN if res['pi'] >= 1.0 else Colors.BRIGHT_RED
            print(f"  • Индекс доходности капитала (PI):   {pi_color}{res['pi']:.3f}{Colors.RESET} " + 
                  f"{Colors.GRAY}(каждый вложенный символ валюты вернет {res['pi']:.2f}){Colors.RESET}")

            if res['dpbp'] is not None:
                total_months = round(res['dpbp'] * 12)
                years_part = total_months // 12
                months_part = total_months % 12
                print(f"  • Дисконтированная окупаемость (DPBP): {Colors.BRIGHT_CYAN}{years_part} л. и {months_part} мес.{Colors.RESET}")
            else:
                print(f"  • Дисконтированная окупаемость (DPBP): {Colors.BRIGHT_RED}Не окупается{Colors.RESET} в пределах заданного горизонта.")

            self.app.ui.print_smart(f"\n{Colors.BOLD}{Colors.MAGENTA}[КРИЗИСНЫЙ СТРЕСС-ТЕСТ СИСТЕМЫ KRONOS]:{Colors.RESET}")
            print(f"  {Colors.GRAY}Моделирование падения входящих доходов на 20% (рыночный спад)...{Colors.RESET}")
            
            stressed_flows = [cf * 0.8 for cf in cash_flows]
            stress_res = InvestmentEngine.calculate_metrics(initial_investment, rate, stressed_flows)
            
            print(f"  • NPV в условиях кризиса:           {Colors.BRIGHT_GREEN if stress_res['npv'] >= 0 else Colors.BRIGHT_RED}{stress_res['npv']:.2f}{Colors.RESET}")
            
            self.app.ui.print_smart(f"\n{Colors.BOLD}{Colors.YELLOW}[ИТОГОВОЕ ЭКСПЕРТНОЕ ЗАКЛЮЧЕНИЕ]:{Colors.RESET}")
            if res['npv'] >= 0 and stress_res['npv'] >= 0:
                print(f"  {Colors.BRIGHT_GREEN}● ВЫСОКАЯ НАДЕЖНОСТЬ{Colors.RESET}. Проект прибыльный и сохраняет устойчивость даже при падении доходов.")
            elif res['npv'] >= 0 and stress_res['npv'] < 0:
                print(f"  {Colors.YELLOW}● УМЕРЕННЫЙ РИСК{Colors.RESET}. Проект прибыльный в штатном режиме, но уязвим к падению рынка. Требует резервных фондов.")
            else:
                print(f"  {Colors.BRIGHT_RED}● ОТКЛОНИТЬ ПРОЕКТ{Colors.RESET}. Бизнес-модель экономически неэффективна и генерирует убытки.")

            self.app.history.add("Финансы", f"Инвест-анализ (Инв: {initial_investment:.0f})", f"NPV={res['npv']:.2f}")

        except Exception as e:
            self.app.ui.print_error(f"Ошибка инвестиционного процессора: {e}")