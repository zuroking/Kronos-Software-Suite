# modules/mod_fin_credit.py
from kronos_core import Colors

METADATA = {
    "id": 15,
    "category": "ФИНАНСОВАЯ МАТЕМАТИКА",
    "name": "Кредитный калькулятор (Оптимизация досрочных выплат и DTI)"
}

class CreditEngine:
    @staticmethod
    def simulate_annuity_with_overpayment(principal: float, rate_year: float, months: int, extra_monthly: float) -> dict:
        if rate_year < 1e-5:
            base_payment = principal / months
            r = 0.0
        else:
            r = (rate_year / 100) / 12
            try:
                base_payment = principal * (r * (1 + r)**months) / ((1 + r)**months - 1)
            except ZeroDivisionError:
                base_payment = principal / months
                r = 0.0
        
        remaining_balance = principal
        total_interest = 0.0
        actual_months = 0
        total_actual_paid = 0.0
        
        while remaining_balance > 0 and actual_months < 1200: 
            actual_months += 1
            interest_for_month = remaining_balance * r
            
            current_base_payment = min(base_payment, remaining_balance + interest_for_month)
            principal_cut = current_base_payment - interest_for_month
            
            if remaining_balance <= (principal_cut + extra_monthly):
                total_interest += interest_for_month
                total_actual_paid += (remaining_balance + interest_for_month)
                remaining_balance = 0
                break
            else:
                total_interest += interest_for_month
                total_actual_paid += (current_base_payment + extra_monthly)
                remaining_balance -= (principal_cut + extra_monthly)

        if r == 0.0:
            base_interest = 0.0
        else:
            base_interest = (base_payment * months) - principal
            
        saved_interest = max(0.0, base_interest - total_interest)
        saved_months = max(0, months - actual_months)
        
        return {
            "base_payment": base_payment,
            "actual_months": actual_months,
            "total_interest": total_interest,
            "total_paid": total_actual_paid,
            "saved_interest": saved_interest,
            "saved_months": saved_months
        }


class KronosPlugin:
    def __init__(self, app) -> None:
        self.app = app

    def execute(self) -> None:
        self.app.ui.print_smart(f"{Colors.BOLD}{Colors.CYAN}--- КРЕДИТНО-АНАЛИТИЧЕСКИЙ КОМПЛЕКС ULTRA V3.0 ---{Colors.RESET}")
        print(" Модуль осуществляет продвинутый расчет аннуитета, рисков и досрочных выплат.")
        
        try:
            principal = self.app.ui.get_input("\nВведите сумму кредита (тело долга): ", float, lambda x: x > 0)
            rate_year = self.app.ui.get_input("Годовая процентная ставка банка (%): ", float, lambda x: x > 0)
            months = self.app.ui.get_input("Срок кредитования (в месяцах): ", int, lambda x: x > 0)
            extra_monthly = self.app.ui.get_input("Сумма ежемесячного досрочного погашения (если нет, введите 0): ", float, lambda x: x >= 0)
            income = self.app.ui.get_input("Ваш чистый ежемесячный доход (для оценки рисков дефолта): ", float, lambda x: x > 0)

            res = CreditEngine.simulate_annuity_with_overpayment(principal, rate_year, months, extra_monthly)
            dti = (res["base_payment"] / income) * 100

            self.app.ui.print_smart(f"\n{Colors.BOLD}{Colors.GREEN}[БАЗОВЫЙ МАТЕМАТИЧЕСКИЙ РАСЧЕТ]:{Colors.RESET}")
            print(f"  • Обязательный ежемесячный платеж: {Colors.BRIGHT_GREEN}{res['base_payment']:.2f}{Colors.RESET}")
            print(f"  • Общая сумма начисленных процентов: {res['total_interest']:.2f}")
            print(f"  • Итоговая стоимость кредита (выплаты): {res['total_paid']:.2f}")

            if extra_monthly > 0:
                self.app.ui.print_smart(f"\n{Colors.BOLD}{Colors.YELLOW}[АНАЛИЗ ОПТИМИЗАЦИИ ДОСРОЧНЫХ ВЫПЛАТ]:{Colors.RESET}")
                print(f"  • Реальный срок погашения сократится до: {Colors.BRIGHT_CYAN}{res['actual_months']}{Colors.RESET} мес. (вместо {months} мес.)")
                print(f"  • Вы сэкономите времени:                {Colors.BRIGHT_GREEN}{res['saved_months']}{Colors.RESET} мес. (это {res['saved_months']/12:.1f} лет)")
                print(f"  • ЧИСТАЯ ЭКОНОМИЯ НА ПРОЦЕНТАХ БАНКА:    {Colors.BRIGHT_GREEN}{res['saved_interest']:.2f}{Colors.RESET}")

            self.app.ui.print_smart(f"\n{Colors.BOLD}{Colors.MAGENTA}[ОЦЕНКА ФИНАНСОВОЙ УСТОЙЧИВОСТИ И РИСКОВ]:{Colors.RESET}")
            print(f"  • Коэффициент долговой нагрузки (DTI): {dti:.2f}%")
            
            if dti <= 30:
                verdict = f"{Colors.BRIGHT_GREEN}БЕЗОПАСНЫЙ УРОВЕНЬ{Colors.RESET}. Кредит не оказывает критического давления на budget."
            elif dti <= 50:
                verdict = f"{Colors.YELLOW}УМЕРЕННЫЙ РИСК{Colors.RESET}. Рекомендуется оптимизировать расходы и не брать новые займы."
            else:
                verdict = f"{Colors.BRIGHT_RED}КРИТИЧЕСКАЯ НАГРУЗКА (РИСК ДЕФОЛТА!){Colors.RESET}. Более половины дохода уходит банку. Высокая вероятность кризиса бюджета."
            
            print(f"  • Вердикт KRONOS: {verdict}")
            self.app.history.add("Финансы", f"Кредит {principal:.0f} под {rate_year}%", f"DTI={dti:.1f}%")

        except Exception as e:
            self.app.ui.print_error(f"Ошибка финансово-кредитного процессора: {e}")