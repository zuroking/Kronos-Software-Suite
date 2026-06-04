# modules/mod_rpn.py
import operator
from kronos_core import Colors

METADATA = {
    "id": 1,
    "category": "АЛГЕБРА И ГЕОМЕТРИЯ",
    "name": "Калькулятор выражений (Обратная польская запись)"
}

class KronosPlugin:
    def __init__(self, app) -> None:
        self.app = app

    def execute(self) -> None:
        self.app.ui.print_smart(f"{Colors.BOLD}{Colors.CYAN}--- КАЛЬКУЛЯТОР ВЫРАЖЕНИЙ ОПЗ (ПЛАГИН) ---{Colors.RESET}")
        print(" Введите токены через пробел. Пример: '3 4 + 2 *' -> (3+4)*2")
        expr = self.app.ui.get_input("ОПЗ Выражение: ", str).strip()
        
        if not expr:
            self.app.ui.print_error("Ошибка: введена пустая строка.")
            return

        try:
            tokens = expr.split()
            stack = []
            ops = {
                '+': operator.add, 
                '-': operator.sub, 
                '*': operator.mul, 
                '/': operator.truediv, 
                '^': operator.pow
            }
            
            for token in tokens:
                if token in ops:
                    if len(stack) < 2:
                        raise ValueError("недостаточно чисел в стеке для выполнения операции.")
                    b = stack.pop()
                    a = stack.pop()
                    
                    if token == '/' and abs(b) < 1e-15:
                        raise ZeroDivisionError("деление на ноль в ОПЗ-стеке.")
                        
                    try:
                        stack.append(ops[token](a, b))
                    except (OverflowError, ValueError):
                        raise ValueError(f"вычислительное переполнение регистра! Операция [{a} {token} {b}] невозможна.")
                else:
                    try:
                        stack.append(float(token))
                    except ValueError:
                        raise ValueError(f"недопустимый токен '{token}'. Вводите только числа и операторы (+, -, *, /, ^).")
            
            if not stack:
                raise ValueError("стек пуст.")
                
            if len(stack) > 1:
                print(f"\n{Colors.YELLOW}[ВНИМАНИЕ]: Выражение составлено неполно. В стеке остались неиспользованные числа: {stack[:-1]}{Colors.RESET}")
            
            res = stack[-1]
            self.app.ui.print_smart(f"\n{Colors.GREEN}Результат ОПЗ:{Colors.RESET} {res}")
            self.app.history.add("RPN", expr, str(res))
            
        except ZeroDivisionError as zde:
            self.app.ui.print_error(f"Математическая ошибка: {zde}")
        except ValueError as ve:
            self.app.ui.print_error(f"Ошибка парсера ОПЗ: {ve}")
        except Exception as e:
            self.app.ui.print_error(f"Критический сбой калькулятора ОПЗ: {e}")