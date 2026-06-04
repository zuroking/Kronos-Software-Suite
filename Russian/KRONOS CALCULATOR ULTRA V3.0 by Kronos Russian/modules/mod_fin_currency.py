# modules/mod_fin_currency.py
from kronos_core import Colors

METADATA = {
    "id": 20,
    "category": "ФИНАНСОВАЯ МАТЕМАТИКА",
    "name": "Валютный процессор (Кросс-курсы и Треугольный арбитраж)"
}

class CurrencyEngine:
    EXCHANGE_BOOK = {
        "usd": (1.0000, 1.0000),      
        "eur": (0.9150, 0.9220),      
        "gbp": (0.7810, 0.7880),      
        "chf": (0.8920, 0.8990),      
        "jpy": (155.2000, 156.4000),  
        "cny": (7.2400, 7.2800),      
        "rub": (89.8000, 91.5000),    
        "kzt": (448.0000, 454.0000),  
        "aed": (3.6710, 3.6730)       
    }

    @classmethod
    def convert_cash(cls, amount: float, from_val: str, to_val: str, trading_fee_pct: float = 0.0) -> tuple[float, float]:
        if from_val == to_val:
            return amount, 0.0
            
        bid_from, ask_from = cls.EXCHANGE_BOOK[from_val]
        bid_to, ask_to = cls.EXCHANGE_BOOK[to_val]
        
        if from_val == "usd":
            amount_in_usd = amount
        else:
            amount_in_usd = amount / ask_from 
            
        if to_val == "usd":
            final_amount = amount_in_usd
        else:
            final_amount = amount_in_usd * bid_to

        if trading_fee_pct > 0:
            final_amount *= (1.0 - (trading_fee_pct / 100))

        mid_from = (bid_from + ask_from) / 2
        mid_to = (bid_to + ask_to) / 2
        ideal_res = (amount / mid_from) * mid_to
        spread_loss = max(0.0, ideal_res - final_amount)

        return final_amount, spread_loss

    @classmethod
    def check_triangular_arbitrage(cls, fee_pct: float) -> list[tuple[str, str, str, float]]:
        currencies = list(cls.EXCHANGE_BOOK.keys())
        opportunities = []
        
        for v1 in currencies:
            for v2 in currencies:
                for v3 in currencies:
                    if v1 != v2 and v2 != v3 and v1 != v3:
                        start_amt = 100.0
                        amt_v2, _ = cls.convert_cash(start_amt, v1, v2, fee_pct)
                        amt_v3, _ = cls.convert_cash(amt_v2, v2, v3, fee_pct)
                        end_amt, _ = cls.convert_cash(amt_v3, v3, v1, fee_pct)
                        
                        if end_amt > start_amt:
                            profit_pct = (end_amt - start_amt) / start_amt * 100
                            opportunities.append((v1, v2, v3, profit_pct))
                            
        opportunities.sort(key=lambda x: x[3], reverse=True)
        return opportunities


class KronosPlugin:
    def __init__(self, app) -> None:
        self.app = app

    def execute(self) -> None:
        self.app.ui.print_smart(f"{Colors.BOLD}{Colors.CYAN}--- ВАЛЮТНЫЙ ДИЛИНГОВЫЙ ПРОЦЕССОР ULTRA V3.0 ---{Colors.RESET}")
        print(" Выберите режим валютных операций:")
        print("  [1] Обмен валюты (Конвертация с учетом банковского спреда Bid/Ask)")
        print("  [2] Сканирование рынка на Треугольный Арбитраж (Поиск неэффективности курсов)")
        
        choice = self.app.ui.get_input("Действие: ", int, lambda x: x in (1, 2))
        
        try:
            if choice == 1:
                print(f"\n{Colors.YELLOW}Доступные международные тикеры:{Colors.RESET}")
                print(f"  {Colors.GRAY}" + ", ".join([k.upper() for k in CurrencyEngine.EXCHANGE_BOOK.keys()]) + f"{Colors.RESET}")
                
                v_from = self.app.ui.get_input("\nИсходная валюта (продать): ", str).lower()
                v_to = self.app.ui.get_input("Целевая валюта (купить):   ", str).lower()
                amount = self.app.ui.get_input("Объем обмениваемых средств: ", float, lambda x: x > 0)
                
                if v_from not in CurrencyEngine.EXCHANGE_BOOK or v_to not in CurrencyEngine.EXCHANGE_BOOK:
                    self.app.ui.print_error("Указанный валютный тикер отсутствует в спецификации ядра!")
                    return
                    
                res, loss = CurrencyEngine.convert_cash(amount, v_from, v_to, trading_fee_pct=0.0)
                
                self.app.ui.print_smart(f"\n{Colors.BOLD}{Colors.GREEN}[ОПЕРАЦИЯ ОБМЕНА ВЫПОЛНЕНА]:{Colors.RESET}")
                print(f"  • Вы отдаете: {amount:.2f} {v_from.upper()}")
                print(f"  • Вы получаете на руки: {Colors.BRIGHT_GREEN}{res:.2f}{Colors.RESET} {v_to.upper()}")
                print(f"  • Тотальные потери на спреде: {Colors.BRIGHT_RED}{loss:.2f}{Colors.RESET} {v_to.upper()}")
                
                self.app.history.add("Валюта", f"Обмен {amount} {v_from}->{v_to}", f"Получено={res:.2f}")

            elif choice == 2:
                fee_pct = self.app.ui.get_input("\nВведите торговую комиссию брокера/биржи (%, например 0.1): ", float, lambda x: 0 <= x < 5)
                
                self.app.ui.print_smart(f"\n{Colors.GRAY}Запуск сканирования кросс-матрицы котировок...{Colors.RESET}")
                arb_windows = CurrencyEngine.check_triangular_arbitrage(fee_pct)
                
                self.app.ui.print_smart(f"\n{Colors.BOLD}{Colors.YELLOW}[РЕЗУЛЬТАТЫ СКАНИРОВАНИЯ РЫНКА]:{Colors.RESET}")
                if not arb_windows:
                    print(f"  • {Colors.GREEN}Локальный валютный рынок стабилен. Арбитражных окон с учетом комиссий {fee_pct}% не обнаружено.{Colors.RESET}")
                else:
                    print(f"  • {Colors.BRIGHT_RED}ОБНАРУЖЕНЫ РЕАЛЬНЫЕ АРБИТРАЖНЫЕ ОКНА ДЛЯ СПЕКУЛЯЦИЙ!{Colors.RESET}")
                    for v1, v2, v3, profit in arb_windows[:10]:
                        print(f"    [!] Цепочка: {v1.upper()} -> {v2.upper()} -> {v3.upper()} -> {v1.upper()} | Чистая прибыль: +{Colors.BRIGHT_GREEN}{profit:.3f}%{Colors.RESET}")
                
                self.app.history.add("Валюта", "Сканирование арбитража", f"Найдено окон: {len(arb_windows)}")

        except Exception as e:
            self.app.ui.print_error(f"Критическая ошибка валютного процессора: {e}")