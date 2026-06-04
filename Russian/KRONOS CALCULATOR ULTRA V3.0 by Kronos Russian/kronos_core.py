# KRONOS CALCULATOR ULTRA V3.0 - CORE ENGINE
from __future__ import annotations

import os
import sys
import time
import csv
import threading
import queue
import importlib
import pkgutil
import math
import ast
import re
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Any, Callable, TypeVar, Optional

T = TypeVar("T")

class SafeMathParser:
    def __init__(self) -> None:
        self.allowed_names = {
            "abs": abs, "round": round, "max": max, "min": min,
            "sin": math.sin, "cos": math.cos, "tan": math.tan,
            "asin": math.asin, "acos": math.acos, "atan": math.atan,
            "sinh": math.sinh, "cosh": math.cosh, "tanh": math.tanh,
            "sqrt": math.sqrt, "log": math.log, "log10": math.log10,
            "exp": math.exp, "pi": math.pi, "e": math.e
        }

    def eval_expr(self, expr: str, variables: dict) -> float:
        clean_expr = expr.replace("^", "**")
        clean_expr = re.sub(r'(\d+)([a-zA-Z(])', r'\1*\2', clean_expr)
        try:
            tree = ast.parse(clean_expr, mode='eval')
            if not self._check_node(tree.body):
                raise ValueError("Обнаружены недопустимые или опасные операторы.")
            compiled = compile(tree, '<string>', 'eval')
            context = {**self.allowed_names, **variables}
            return float(eval(compiled, {"__builtins__": None}, context))
        except Exception as e:
            raise ValueError(f"Синтаксическая ошибка разбора формулы: {e}")

    def _check_node(self, node: ast.AST) -> bool:
        if isinstance(node, ast.Expression): 
            return self._check_node(node.body)
        if isinstance(node, (ast.Constant, ast.Name)): 
            return True
        if hasattr(ast, 'Num') and isinstance(node, ast.Num):
            return True
        if isinstance(node, ast.UnaryOp): 
            return self._check_node(node.operand)
        if isinstance(node, ast.BinOp): 
            return self._check_node(node.left) and self._check_node(node.right)
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in self.allowed_names:
                return all(self._check_node(arg) for arg in node.args)
            return False
        return False

class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    GRAY = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"

@dataclass
class HistoryItem:
    timestamp: str
    module_name: str
    expression: str
    result: str

    def to_line(self) -> str:
        return f"[{self.timestamp}] {Colors.CYAN}{self.module_name}{Colors.RESET} ➔ {Colors.GRAY}{self.expression}{Colors.RESET} = {Colors.GREEN}{self.result}{Colors.RESET}"

class HistoryEngine:
    def __init__(self, filename: str = "kronos_history.csv") -> None:
        self.filename = filename
        self.items: List[HistoryItem] = []
        self._queue: queue.Queue[HistoryItem] = queue.Queue()
        self._is_running = True
        self._load_from_file()
        self._worker_thread = threading.Thread(target=self._io_loop, daemon=True)
        self._worker_thread.start()

    def _load_from_file(self) -> None:
        if not os.path.exists(self.filename): return
        try:
            with open(self.filename, mode="r", encoding="utf-8") as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) == 4: self.items.append(HistoryItem(*row))
        except Exception: pass

    def _io_loop(self) -> None:
        while self._is_running or not self._queue.empty():
            try:
                item = self._queue.get(timeout=0.2)
                with open(self.filename, mode="a", encoding="utf-8", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([item.timestamp, item.module_name, item.expression, item.result])
                self._queue.task_done()
            except queue.Empty: continue
            except Exception: pass

    def add(self, module_name: str, expression: str, result: str) -> None:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        item = HistoryItem(now, module_name, str(expression), str(result))
        self.items.append(item)
        self._queue.put(item)

    def clear(self) -> None:
        self.items.clear()
        try:
            if os.path.exists(self.filename): os.remove(self.filename)
        except Exception: pass

    def stop(self) -> None:
        self._is_running = False
        self._worker_thread.join(timeout=1.0)

class UserInterface:
    @staticmethod
    def clear_screen() -> None:
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def pause() -> None:
        input(f"\n{Colors.GRAY}Нажмите Enter для возврата в главное меню...{Colors.RESET}")

    @staticmethod
    def print_smart(text: str) -> None:
        print(text)

    @staticmethod
    def print_error(msg: str) -> None:
        print(f"{Colors.BOLD}{Colors.RED}[КРИТИЧЕСКАЯ ОШИБКА]: {msg}{Colors.RESET}")

    @staticmethod
    def get_input(prompt: str, type_func: Callable[[str], T], validator: Optional[Callable[[T], bool]] = None, allow_empty: bool = False) -> T:
        while True:
            try:
                raw = input(prompt).strip()
                if not raw and allow_empty: return ""  # type: ignore
                val = type_func(raw)
                if validator and not validator(val): raise ValueError()
                return val
            except Exception:
                print(f"  {Colors.RED}❌ Некорректный ввод. Ожидался {type_func.__name__}. Повторите попытку.{Colors.RESET}")

class AppEngine:
    def _print_gradient_logo(self, start_color: tuple, end_color: tuple):
        logo = [
            "  ╔══════════════════════════════════════════════════════╗",
            "   ██╗ ██╗██████╗  ██████╗ ███╗   ██╗ ██████╗ ███████╗",
            "   ██║ ██╔╝██╔══██╗██╔═══██╗████╗  ██║██╔═══██╗██╔════╝",
            "   █████╔╝ ██████╔╝██║   ██║██╔██╗ ██║██║   ██║███████╗",
            "   ██╔═██╗ ██╔══██╗██║   ██║██║╚██╗██║██║   ██║╚════██║",
            "   ██║  ██╗██║  ██║╚██████╔╝██║ ╚████║╚██████╔╝███████║",
            "   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚══════╝",
            "                                                       ",
            "             ██╗   ██╗██╗  ████████╗██████╗  █████╗    ",
            "             ██║   ██║██║  ╚══██╔══╝██╔══██╗██╔══██╗   ",
            "             ██║   ██║██║     ██║   ██████╔╝███████║   ",
            "             ██║   ██║██║     ██║   ██╔══██╗██╔══██║   ",
            "             ╚██████╔╝███████╗██║   ██║  ██║██║  ██║   ",
            "              ╚═════╝ ╚══════╝╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝   ",
            "                                                       ",
            "                        ██╗   ██╗██████╗               ",
            "                        ██║   ██║╚════██╗              ",
            "                        ██║   ██║ █████╔╝              ",
            "                        ╚██╗ ██╔╝ ╚═══██╗              ",
            "                        ╚████╔╝ ██████╔╝               ",
            "                         ╚═══╝  ╚═════╝                ",
            "  ╚══════════════════════════════════════════════════════╝"
        ]
        
        for line in logo:
            colored_line = ""
            n = len(line)
            for i, char in enumerate(line):
                if n > 1:
                    r = int(start_color[0] + (end_color[0] - start_color[0]) * (i / (n - 1)))
                    g = int(start_color[1] + (end_color[1] - start_color[1]) * (i / (n - 1)))
                    b = int(start_color[2] + (end_color[2] - start_color[2]) * (i / (n - 1)))
                else:
                    r, g, b = start_color
                colored_line += f"\033[38;2;{r};{g};{b}m{char}"
            print(colored_line + "\033[0m")
            
    def __init__(self) -> None:
        self.ui = UserInterface()
        self.history = HistoryEngine()
        self.parser = SafeMathParser()
        self.plugins: Dict[int, Dict[str, Any]] = {}
        self.theme = "Cyberpunk"
        self._load_plugins()

    def _load_plugins(self) -> None:
        modules_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "modules")
        if not os.path.exists(modules_dir): return
        if modules_dir not in sys.path: sys.path.insert(0, modules_dir)

        for _, module_name, is_pkg in pkgutil.iter_modules([modules_dir]):
            if is_pkg: continue
            try:
                module = importlib.import_module(module_name)
                if hasattr(module, "METADATA") and hasattr(module, "KronosPlugin"):
                    meta = module.METADATA
                    self.plugins[meta["id"]] = {"metadata": meta, "class": module.KronosPlugin}
            except Exception as e:
                self.ui.print_error(f"Не удалось загрузить модуль {module_name}: {e}")

    def run(self) -> None:
        def rgb(r: int, g: int, b: int, text: str) -> str:
            return f"\033[38;2;{r};{g};{b}m{text}\033[0m"

        while True:
            self.ui.clear_screen()
            
            if self.theme == "Cyberpunk":
                grad_start = (255, 0, 128)
                grad_end = (0, 240, 255)
                ht = (255, 0, 128)   
                it = (0, 255, 255)   
                st = (240, 240, 240) 
                ec = (255, 255, 0)   
                
                cat_colors = {
                    "АЛГЕБРА И ГЕОМЕТРИЯ": (255, 100, 0),     
                    "ИНЖЕНЕРИЯ И АНАЛИТИКА": (0, 255, 128),   
                    "ФИНАНСОВАЯ МАТЕМАТИКА": (255, 0, 255),   
                    "ИНСТРУМЕНТЫ": (200, 160, 255),           
                    "СИСТЕМА": (255, 50, 100)                 
                }
            else:
                grad_start = (0, 255, 128)
                grad_end = (0, 100, 40)
                ht, it, st, ec = (0, 255, 128), (128, 255, 0), (200, 250, 200), (255, 64, 64)
                cat_colors = {
                    "АЛГЕБРА И ГЕОМЕТРИЯ": ht, "ИНЖЕНЕРИЯ И АНАЛИТИКА": ht,
                    "ФИНАНСОВАЯ МАТЕМАТИКА": ht, "ИНСТРУМЕНТЫ": ht, "СИСТЕМА": ht
                }

            self._print_gradient_logo(grad_start, grad_end)
            print("   " + f"\033[1m{rgb(*ht, '      EDITION: ULTRA V3.0  ⚡  BY KRONOS RUSSIAN')}\033[0m")
            print("   " + rgb(*ht, "═ " * 29))

            for cat in ["АЛГЕБРА И ГЕОМЕТРИЯ", "ИНЖЕНЕРИЯ И АНАЛИТИКА", "ФИНАНСОВАЯ МАТЕМАТИКА", "ИНСТРУМЕНТЫ"]:
                has_items_in_cat = any(p["metadata"]["category"] == cat for p in self.plugins.values())
                if not has_items_in_cat: continue
                
                current_cat_color = cat_colors.get(cat, ht)
                print(f"\n   \033[1m{rgb(*current_cat_color, f'[{cat}]')}\033[0m")
                for p_id, p_info in sorted(self.plugins.items()):
                    if p_info["metadata"]["category"] == cat:
                        print(f"     {rgb(*it, f'[{p_id:02d}]')} {rgb(*st, p_info['metadata']['name'])}")

            print(f"\n   \033[1m{rgb(*cat_colors['СИСТЕМА'], '[СИСТЕМНЫЕ СЕРВИСЫ]')}\033[0m")
            print(f"     {rgb(*it, '[98]')} {rgb(*st, 'Просмотр асинхронных логов вычислений')}")
            print(f"     {rgb(*it, '[99]')} {rgb(*st, 'Очистить историю логов')}")
            print(f"     {rgb(*ec, '[00]')} {rgb(*ec, 'Выход из terminal KRONOS')}")
            print("   " + rgb(*ht, "═ " * 29))

            choice = self.ui.get_input(f"\033[1m{rgb(*ht, ' » Выберите пункт: ')}\033[0m", int)
            
            if choice == 0:
                self.ui.print_smart(f"\n\033[1m{rgb(255, 0, 128, ' [!] Вычислительное ядро KRONOS ULTRA деактивировано. До встречи!')}\033[0m\n")
                self.history.stop()
                break
            elif choice == 98:
                self.ui.clear_screen()
                print(f"{Colors.BOLD}{Colors.CYAN}--- ТЕРМИНАЛЬНЫЙ ЛОГ ВЫЧИСЛЕНИЙ KRONOS ---{Colors.RESET}\n")
                if not self.history.items:
                    print(f"  {Colors.GRAY}История вычислений пуста.{Colors.RESET}")
                else:
                    for item in self.history.items[-15:]: print(f"  {item.to_line()}")
                self.ui.pause()
            elif choice == 99:
                self.history.clear()
                self.ui.print_smart(f"\n  {Colors.GREEN}✔ Файловые хранилища логов очищены.{Colors.RESET}")
                self.ui.pause()
            elif choice in self.plugins:
                self.ui.clear_screen()
                try:
                    plugin_instance = self.plugins[choice]["class"](self)
                    plugin_instance.execute()
                    self.ui.pause() 
                except Exception as e:
                    self.ui.print_error(f"Ошибка выполнения плагина №{choice}: {e}")
                    self.ui.pause()
            else:
                print(f"  {Colors.RED}❌ Ошибка: Указанный идентификатор отсутствует в пуле ядра.{Colors.RESET}")
                time.sleep(1.2)

if __name__ == "__main__":
    app = AppEngine()
    app.run()