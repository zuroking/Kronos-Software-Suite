# modules/mod_chemistry.py
import re
from typing import List, Tuple
from kronos_core import Colors

METADATA = {
    "id": 10,
    "category": "ИНЖЕНЕРИЯ И АНАЛИТИКА",
    "name": "Химия (Молярная масса сложных молекул)"
}

class KronosPlugin:
    def __init__(self, app) -> None:
        self.app = app
        self.periodic_table = {
            "H": 1.008, "He": 4.0026, "Li": 6.94, "Be": 9.0122, "B": 10.81, "C": 12.011, "N": 14.007, "O": 15.999,
            "F": 18.998, "Ne": 20.180, "Na": 22.990, "Mg": 24.305, "Al": 26.982, "Si": 28.085, "P": 30.974, "S": 32.06,
            "Cl": 35.45, "Ar": 39.948, "K": 39.098, "Ca": 40.078, "Fe": 55.845, "Cu": 63.546, "Zn": 65.38, "Ag": 107.868,
            "Au": 196.967, "Pt": 195.084, "I": 126.904, "Br": 79.904, "Xe": 131.293, "Hg": 200.592, "Pb": 207.2
        }

    def _parse_formula(self, formula: str) -> List[Tuple[str, int]]:
        sub_form = formula.replace(" ", "")
        stack = [[]]
        i, n = 0, len(sub_form)
        
        while i < n:
            if sub_form[i] == '(':
                stack.append([])
                i += 1
            elif sub_form[i] == ')':
                if len(stack) < 2: 
                    raise ValueError("Нарушен баланс скобок (лишняя закрывающая скобка).")
                top = stack.pop()
                i += 1
                start = i
                while i < n and sub_form[i].isdigit(): i += 1
                count = int(sub_form[start:i]) if start != i else 1
                
                if count > 100000:
                    raise ValueError(f"Аномальный индекс {count}! Превышен лимит безопасности KRONOS (max: 100000).")
                
                for el, c in top: 
                    stack[-1].append((el, c * count))
            else:
                match = re.match(r'^([A-Z][a-z]*)', sub_form[i:])
                if not match: 
                    raise ValueError(f"Неверный синтаксис на элементе '{sub_form[i:]}'. Проверьте знаки.")
                el = match.group(1)
                if el not in self.periodic_table: 
                    raise ValueError(f"Элемент '{el}' отсутствует в базе данных KRONOS.")
                i += len(el)
                
                start = i
                while i < n and sub_form[i].isdigit(): i += 1
                count = int(sub_form[start:i]) if start != i else 1
                
                if count > 100000:
                    raise ValueError(f"Аномальный индекс {count} для элемента {el}! Превышен лимит безопасности KRONOS.")
                    
                stack[-1].append((el, count))
                
        if len(stack) != 1:
            raise ValueError("Нарушен баланс скобок (отсутствует закрывающая скобка).")
            
        return stack[0]

    def execute(self) -> None:
        self.app.ui.print_smart(f"{Colors.BOLD}{Colors.CYAN}--- CHEMICAL MASS-SPECTROMETRIC PROCESSOR ULTRA V3.0 ---{Colors.RESET}")
        print(" Модуль вычисляет идеальную молярную массу соединений и элементный состав.")
        print(f" {Colors.GRAY}Примеры ввода: H2O, H2SO4, Ca(OH)2, Fe2(SO4)3, C6H12O6{Colors.RESET}\n")
        
        formula = self.app.ui.get_input("Введите химическую формулу вещества: ", str).strip()
        
        if not formula:
            self.app.ui.print_error("Ошибка: пустой ввод.")
            return
            
        try:
            parsed_elements = self._parse_formula(formula)
            
            composition = {}
            for el, count in parsed_elements:
                composition[el] = composition.get(el, 0) + count
                
            total_mass = sum(self.periodic_table[el] * count for el, count in composition.items())
            
            self.app.ui.print_smart(f"\n{Colors.BOLD}{Colors.GREEN}[РЕЗУЛЬТАТЫ СПЕКТРАЛЬНОГО АНАЛИЗА]:{Colors.RESET}")
            print(f"  • Сводная молярная масса соединения (M): {Colors.BRIGHT_GREEN}{total_mass:.4f}{Colors.RESET} г/моль")
            
            print(f"\n{Colors.BOLD}{Colors.CYAN}[ПРОЦЕНТНОЕ ДОЛЕВОЕ РАСПРЕДЕЛЕНИЕ МАССЫ]:{Colors.RESET}")
            for el, count in sorted(composition.items()):
                el_mass = self.periodic_table[el] * count
                percentage = (el_mass / total_mass) * 100 if total_mass > 0 else 0.0
                print(f"    - {el:<3} × {count:<4} | Масса в ячейке: {el_mass:<8.3f} г/моль | Доля: {Colors.YELLOW}{percentage:.2f}%{Colors.RESET}")
                
            self.app.history.add("Химия", f"Формула {formula}", f"M={total_mass:.2f}")
            
        except ValueError as ve:
            self.app.ui.print_error(f"Ошибка синтаксического анализа: {ve}")
        except Exception as e:
            self.app.ui.print_error(f"Критический сбой химического процессора: {e}")