# modules/mod_bases.py
from kronos_core import Colors

METADATA = {
    "id": 14,
    "category": "ИНСТРУМЕНТЫ",
    "name": "Системы счисления (Вещественный конвертер и Дополнительный код)"
}

class BasesProcessor:
    CHARSET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    @classmethod
    def _int_to_base(cls, n: int, base: int) -> str:
        if n == 0: return "0"
        res = ""
        while n > 0:
            res = cls.CHARSET[n % base] + res
            n //= base
        return res

    @classmethod
    def _frac_to_base(cls, frac: float, base: int, precision: int = 10) -> str:
        res = ""
        while frac > 0 and len(res) < precision:
            frac *= base
            digit = int(frac)
            res += cls.CHARSET[digit]
            frac -= digit
        return res if res else "0"

    @classmethod
    def convert_arbitrary(cls, num_str: str, from_base: int, to_base: int, precision: int = 10) -> str:
        num_str = num_str.upper().strip().replace(",", ".")
        
        is_negative = False
        if num_str.startswith("-"):
            is_negative = True
            num_str = num_str[1:]
            
        if "." in num_str:
            int_part, frac_part = num_str.split(".", 1)
        else:
            int_part, frac_part = num_str, ""
            
        try:
            val_int_10 = int(int_part, from_base) if int_part else 0
        except ValueError:
            raise ValueError(f"Символы целой части не соответствуют базису {from_base}!")
            
        val_frac_10 = 0.0
        if frac_part:
            for idx, char in enumerate(frac_part):
                digit = cls.CHARSET.find(char)
                if digit == -1 or digit >= from_base:
                    raise ValueError(f"Символ '{char}' в дробной части не соответствует базису {from_base}!")
                val_frac_10 += digit / (from_base ** (idx + 1))
                
        res_int = cls._int_to_base(val_int_10, to_base)
        res_frac = cls._frac_to_base(val_frac_10, to_base, precision)
        
        sign = "-" if is_negative else ""
        if frac_part or val_frac_10 > 0:
            return f"{sign}{res_int}.{res_frac}"
        return f"{sign}{res_int}"

    @staticmethod
    def to_twos_complement(number: int, bits: int) -> str:
        if number >= 0:
            bin_str = bin(number)[2:]
            if len(bin_str) > bits - 1:
                raise ValueError(f"Число {number} слишком велико для знакового {bits}-битного регистра!")
            return bin_str.zfill(bits)
        else:
            max_val = 1 << bits
            if abs(number) > (max_val >> 1):
                raise ValueError(f"Отрицательное число {number} выходит за рамки лимита {bits} бит!")
            complement_val = max_val + number
            return bin(complement_val)[2:].zfill(bits)


class KronosPlugin:
    def __init__(self, app) -> None:
        self.app = app

    def execute(self) -> None:
        self.app.ui.print_smart(f"{Colors.BOLD}{Colors.CYAN}--- ВЕЩЕСТВЕННЫЙ ПОЛИМОРФНЫЙ КОНВЕРТЕР БАЗИСОВ ULTRA V3.0 ---{Colors.RESET}")
        print(" Выберите режим анализа данных:")
        print("  [1] Перевод произвольного числа (с плавающей точкой) между системами от 2 до 36")
        print("  [2] Генерация двоичного дополнительного кода (Представление знака в ОЗУ)")
        
        choice = self.app.ui.get_input("Действие: ", int, lambda x: x in (1, 2))
        
        try:
            if choice == 1:
                b1 = self.app.ui.get_input("\nИсходное основание системы (2-36): ", int, lambda x: 2 <= x <= 36)
                b2 = self.app.ui.get_input("Целевое основание системы (2-36):   ", int, lambda x: 2 <= x <= 36)
                num = self.app.ui.get_input("Введите число для конвертации (можно с точкой): ", str)
                
                prec = self.app.ui.get_input("Точность дробной части (кол-во знаков мантиссы, 1-32, Enter для 10): ", 
                                             int, lambda x: 1 <= x <= 32, allow_empty=True)
                if not prec:
                    prec = 10
                
                res = BasesProcessor.convert_arbitrary(num, b1, b2, precision=prec)
                
                self.app.ui.print_smart(f"\n{Colors.BOLD}{Colors.GREEN}[КОНВЕРТАЦИЯ ВЫПОЛНЕНА]:{Colors.RESET}")
                print(f"  • {num} (базис {b1}) = {Colors.BRIGHT_GREEN}{res}{Colors.RESET} (базис {b2})")
                self.app.history.add("СистемыСчисления", f"Перевод {num} (b{b1}) -> b{b2}", res)

            elif choice == 2:
                print(f"\n{Colors.YELLOW}--- ДВОИЧНЫЙ ДОПОЛНИТЕЛЬНЫЙ КОД (ЗНАКОВЫЙ РЕГИСТР) ---{Colors.RESET}")
                num_10 = self.app.ui.get_input("Введите целое десятичное число (можно отрицательное): ", int)
                bits = self.app.ui.get_input("Выберите разрядность регистра процессора (8, 16, 32 бита): ", int, lambda x: x in (8, 16, 32))
                
                comp_bin = BasesProcessor.to_twos_complement(num_10, bits)
                
                self.app.ui.print_smart(f"\n{Colors.BOLD}{Colors.GREEN}[МАШИННОЕ ПРЕДСТАВЛЕНИЕ В ОЗУ]:{Colors.RESET}")
                formatted_bin = " ".join(comp_bin[i:i+4] for i in range(0, len(comp_bin), 4))
                print(f"  • Знаковый {bits}-битный регистр: {Colors.BRIGHT_CYAN}{formatted_bin}{Colors.RESET}")
                self.app.history.add("СистемыСчисления", f"Доп.код числа {num_10} ({bits} бит)", comp_bin)

        except ValueError as ve:
            self.app.ui.print_error(f"Ошибка трансляции базиса: {ve}")
        except Exception as e:
            self.app.ui.print_error(f"Критический сбой процессора систем счисления: {e}")