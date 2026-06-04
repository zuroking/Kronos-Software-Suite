# modules/mod_converter.py
from kronos_core import Colors

METADATA = {
    "id": 8,
    "category": "ПРИКЛАДНЫЕ РАСЧЕТЫ",
    "name": "Метрологический конвертер величин (Физические константы и СИ)"
}

class MetrologyEngine:
    DATA = {
        1: { 
            "m": 1.0, "km": 1000.0, "cm": 0.01, "mm": 0.001,
            "mile": 1609.344, "yard": 0.9144, "inch": 0.0254
        },
        2: { 
            "g": 1.0, "kg": 1000.0, "mg": 0.001, "ton": 1000000.0,
            "lb": 453.59237, "oz": 28.3495231
        },
        3: { 
            "ms": 1.0, "kmh": 1 / 3.6, "mph": 0.44704, "knot": 0.514444
        },
        4: { 
            "pa": 1.0, "kpa": 1000.0, "atm": 101325.0, "bar": 100000.0, "mmhg": 133.3224
        }
    }

    @staticmethod
    def convert_standard(category: int, value: float, from_unit: str, to_unit: str) -> float:
        cat_dict = MetrologyEngine.DATA.get(category)
        if not cat_dict or from_unit not in cat_dict or to_unit not in cat_dict:
            raise KeyError("Обнаружена неизвестная физическая единица измерения!")
        
        value_in_base = value * cat_dict[from_unit]
        return value_in_base / cat_dict[to_unit]

    @staticmethod
    def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
        if from_unit == "k" and value < 0:
            raise ValueError(f"Температура {value} K ниже абсолютного нуля (0 K) невозможна!")
        if from_unit == "c" and value < -273.15:
            raise ValueError(f"Температура {value}°C ниже абсолютного нуля (-273.15°C) невозможна!")
        if from_unit == "f" and value < -459.67:
            raise ValueError(f"Температура {value}°F ниже абсолютного нуля (-459.67°F) невозможна!")

        if from_unit == "c":
            temp_c = value
        elif from_unit == "k":
            temp_c = value - 273.15
        elif from_unit == "f":
            temp_c = (value - 32) * 5 / 9
        else:
            raise KeyError("Обнаружена неизвестная физическая единица измерения!")

        if to_unit == "c":
            return temp_c
        elif to_unit == "k":
            return temp_c + 273.15
        elif to_unit == "f":
            return (temp_c * 9 / 5) + 32
        else:
            raise KeyError("Обнаружена неизвестная физическая единица измерения!")


class KronosPlugin:
    def __init__(self, app) -> None:
        self.app = app

    def execute(self) -> None:
        self.app.ui.print_smart(f"{Colors.BOLD}{Colors.CYAN}--- МЕТРОЛОГИЧЕСКИЙ КОНВЕРТЕР ВЕЛИЧИН ULTRA V3.0 ---{Colors.RESET}")
        print(" Выберите физическую размерность:")
        print("  [1] Длина       (m, km, cm, mm, mile, yard, inch)")
        print("  [2] Масса       (kg, g, mg, ton, lb, oz)")
        print("  [3] Скорость    (ms, kmh, mph, knot)")
        print("  [4] Давление    (pa, kpa, atm, bar, mmhg)")
        print("  [5] Температура (c, k, f)")
        
        category = self.app.ui.get_input("Категория: ", int, lambda x: 1 <= x <= 5)
        
        print(f"\n{Colors.GRAY}Вводите сокращения строго маленькими буквами, как указано в меню!{Colors.RESET}")
        from_unit = self.app.ui.get_input("Исходная единица измерения: ", str).strip().lower()
        to_unit = self.app.ui.get_input("Целевая единица измерения:  ", str).strip().lower()
        value = self.app.ui.get_input("Введите конвертируемое значение: ", float)
        
        try:
            if category == 5:
                res = MetrologyEngine.convert_temperature(value, from_unit, to_unit)
            else:
                res = MetrologyEngine.convert_standard(category, value, from_unit, to_unit)
                
            self.app.ui.print_smart(f"\n{Colors.BOLD}{Colors.GREEN}[МЕТРОЛОГИЧЕСКИЙ ПЕРЕСЧЕТ ЗАВЕРШЕН]:{Colors.RESET}")
            print(f"  • {value:.6g} [{from_unit.upper()}] = {Colors.BRIGHT_GREEN}{res:.6g}{Colors.RESET} [{to_unit.upper()}]")
            
            self.app.history.add("Метрология", f"Конвертация {from_unit}->{to_unit}", f"Val={res:.2f}")
            
        except KeyError as ke:
            self.app.ui.print_error(f"Ошибка физического пересчета: {ke.args[0]}")
        except ValueError as ve:
            self.app.ui.print_error(f"Критическое нарушение законов физики: {ve}")
        except Exception as e:
            self.app.ui.print_error(f"Сбой ядра конвертера: {e}")