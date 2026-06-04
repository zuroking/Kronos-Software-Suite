# modules/mod_fin_bonds.py
from kronos_core import Colors

METADATA = {
    "id": 21,
    "category": "ФИНАНСОВАЯ МАТЕМАТИКА",
    "name": "Рынок капитала (Справедливая стоимость облигаций и модель Гордона)"
}

class BondsBourseEngine:
    @staticmethod
    def calculate_bond_intrinsic_value(nominal: float, coupon_rate_year: float, years: int, market_rate_year: float) -> tuple[float, float, float]:
        cr = coupon_rate_year / 100
        mr = market_rate_year / 100
        coupon_payment = nominal * cr
        
        intrinsic_value = 0.0
        for t in range(1, years + 1):
            intrinsic_value += coupon_payment / ((1 + mr) ** t)
        intrinsic_value += nominal / ((1 + mr) ** years)
        
        current_yield = (coupon_payment / nominal) * 100 if nominal > 0 else 0.0
        return intrinsic_value, coupon_payment, current_yield

    @staticmethod
    def calculate_precise_ytm(nominal: float, market_price: float, coupon_payment: float, years: int) -> float:
        if market_price <= 0 or nominal <= 0 or years <= 0:
            return 0.0
            
        numerator = coupon_payment + (nominal - market_price) / years
        denominator = (nominal + 2 * market_price) / 3
        
        if denominator == 0:
            return 0.0
        return (numerator / denominator) * 100

    @staticmethod
    def gordon_growth_model(next_dividend: float, required_return_pct: float, growth_rate_pct: float) -> float:
        k = required_return_pct / 100
        g = growth_rate_pct / 100
        if k <= g:
            raise ValueError("Парадокс Гордона: Требуемая доходность инвестора (k) должна быть строго БОЛЬШЕ темпа роста дивидендов (g)!")
        return next_dividend / (k - g)


class KronosPlugin:
    def __init__(self, app) -> None:
        self.app = app

    def execute(self) -> None:
        self.app.ui.print_smart(f"{Colors.BOLD}{Colors.CYAN}--- АНАЛИТИЧЕСКИЙ КОМПЛЕКС РЫНКА КАПИТАЛА ULTRA V3.0 ---{Colors.RESET}")
        print(" Выберите класс исследуемых ценных бумаг:")
        print("  [1] Анализ облигаций (Оценка стоимости, купонов и доходности YTM)")
        print("  [2] Анализ акций (Фундаментальная оценка по модели Гордона)")
        
        choice = self.app.ui.get_input("Инструмент: ", int, lambda x: x in (1, 2))
        
        try:
            if choice == 1:
                print(f"\n{Colors.YELLOW}--- ПАРАМЕТРЫ ОБЛИГАЦИИ ---{Colors.RESET}")
                nominal = self.app.ui.get_input("Номинальная стоимость облигации: ", float, lambda x: x > 0)
                coupon_rate = self.app.ui.get_input("Годовая купонная ставка (%): ", float, lambda x: x >= 0)
                years = self.app.ui.get_input("Срок до погашения (число лет): ", int, lambda x: x > 0)
                market_rate = self.app.ui.get_input("Требуемая инвестором рыночная доходность (%): ", float, lambda x: x > 0)
                
                val, coupon, cy = BondsBourseEngine.calculate_bond_intrinsic_value(nominal, coupon_rate, years, market_rate)
                
                self.app.ui.print_smart(f"\n{Colors.BOLD}{Colors.GREEN}[АНАЛИЗ ДОЛГОВОЙ ЦЕННОЙ БУМАГИ]:{Colors.RESET}")
                print(f"  • Сумма ежегодного купонного дохода: {coupon:.2f}")
                print(f"  • Текущая купонная доходность (CY):   {cy:.2f}%")
                print(f"  • ТЕОРЕТИЧЕСКАЯ СПРАВЕДЛИВАЯ СТОИМОСТЬ: {Colors.BRIGHT_GREEN}{val:.2f}{Colors.RESET}")
                
                if val > nominal: 
                    print(f"  • Статус: Облигация должна торговаться с {Colors.GREEN}ПРЕМИЕЙ{Colors.RESET} выше номинала.")
                elif val < nominal: 
                    print(f"  • Статус: Облигация должна торговаться с {Colors.RED}ДИСКОНТОМ{Colors.RESET} ниже номинала.")
                else: 
                    print("  • Статус: Цена соответствует номиналу.")

                ask_market = self.app.ui.get_input("\nЖелаете рассчитать YTM? Введите текущую рыночную цену облигации (или 0 для пропуска): ", float, lambda x: x >= 0)
                if ask_market > 0:
                    ytm = BondsBourseEngine.calculate_precise_ytm(nominal, ask_market, coupon, years)
                    print(f"  • Полная доходность к погашению (профессиональный YTM) ≈ {Colors.BRIGHT_CYAN}{ytm:.2f}%{Colors.RESET}")

                self.app.history.add("Финансы", f"Облигация (Ном: {nominal:.0f})", f"Цена={val:.2f}")

            elif choice == 2:
                print(f"\n{Colors.YELLOW}--- ФУНДАМЕНТАЛЬНЫЙ АНАЛИЗ АКЦИЙ (GORDON MODEL) ---{Colors.RESET}")
                d1 = self.app.ui.get_input("Прогнозируемый дивиденд на акцию в следующем году (D1): ", float, lambda x: x >= 0)
                k_pct = self.app.ui.get_input("Ожидаемая инвестором ставка доходности / стоимость капитала (%): ", float, lambda x: x > 0)
                g_pct = self.app.ui.get_input("Ожидаемый ежегодный темп роста дивидендов компании (%): ", float, lambda x: x >= 0)
                current_price = self.app.ui.get_input("Текущая реальная рыночная цена акции на бирже: ", float, lambda x: x > 0)

                try:
                    intrinsic_stock_value = BondsBourseEngine.gordon_growth_model(d1, k_pct, g_pct)
                except ValueError as ve:
                    self.app.ui.print_error(str(ve))
                    print(f"  {Colors.BRIGHT_RED}● МАТЕМАТИЧЕСКИЙ ТУПИК:{Colors.RESET} При g >= k стоимость компании уходит в бесконечность.")
                    print(f"    Модель Гордона неприменима для компаний, чей темп роста выше стоимости капитала.")
                    return
                
                self.app.ui.print_smart(f"\n{Colors.BOLD}{Colors.GREEN}[РЕЗУЛЬТАТЫ ОЦЕНКИ СТОИМОСТИ ДОЛИ]:{Colors.RESET}")
                print(f"  • Внутренняя фундаментальная цена акции: {Colors.BRIGHT_GREEN}{intrinsic_stock_value:.2f}{Colors.RESET}")
                print(f"  • Текущая биржевая котировка актива:    {current_price:.2f}")
                
                self.app.ui.print_smart(f"\n{Colors.BOLD}{Colors.YELLOW}[ВЕРДИКТ СИСТЕМЫ KRONOS]:{Colors.RESET}")
                if intrinsic_stock_value > current_price:
                    undervalued_pct = ((intrinsic_stock_value - current_price) / current_price) * 100
                    print(f"  {Colors.BRIGHT_GREEN}● РЕКОМЕНДАЦИЯ: ПОКУПАТЬ (BUY){Colors.RESET}")
                    print(f"    Акция НЕДООЦЕНЕНА рынком на {Colors.BRIGHT_GREEN}{undervalued_pct:.1f}%{Colors.RESET}. Её потенциал роста высок.")
                else:
                    overvalued_pct = ((current_price - intrinsic_stock_value) / intrinsic_stock_value) * 100
                    print(f"  {Colors.BRIGHT_RED}● РЕКОМЕНДАЦИЯ: ПРОДАВАТЬ/ИГНОРИРОВАТЬ (SELL){Colors.RESET}")
                    print(f"    Акция ПЕРЕОЦЕНЕНА рынком на {Colors.BRIGHT_RED}{overvalued_pct:.1f}%{Colors.RESET}. Фундаментальных факторов для роста нет.")
                    
                self.app.history.add("Финансы", f"Акция модель Гордона", f"Справедливая={intrinsic_stock_value:.2f}")

        except Exception as e:
            self.app.ui.print_error(f"Ошибка процессора рынка капитала: {e}")