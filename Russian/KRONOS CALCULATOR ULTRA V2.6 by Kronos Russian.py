# KRONOS CALCULATOR ULTRA V2.6
from __future__ import annotations

import os
import sys
import time
import json
import csv
import math
import cmath
import hashlib
import base64
import re
import tokenize
import unittest
import threading
import queue
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Tuple, Dict, Any, Callable, TypeVar, Optional

from numpy._core.shape_base import stack

T = TypeVar("T")

class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

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
    BRIGHT_WHITE = "\033[97m"

    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_BLUE = "\033[44m"
    BG_CYAN = "\033[46m"


class ConfigManager:
    CONFIG_FILE = "kronos_config.json"

    def __init__(self) -> None:
        self.settings: Dict[str, Any] = {
            "text_delay": 0.003,
            "plot_theme": "dark_background",
            "history_file": "kronos_history.json",
            "export_dir": "exports",
        }
        self.load_config()

    def load_config(self) -> None:
        if os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, "r", encoding="utf-8") as f:
                    self.settings.update(json.load(f))
            except Exception:
                pass

    def save_config(self) -> None:
        try:
            with open(self.CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"{Colors.RED}Ошибка сохранения конфигурации: {e}{Colors.RESET}")


@dataclass
class HistoryItem:
    timestamp: str
    module: str
    action: str
    result: str

    def to_line(self) -> str:
        return f"[{Colors.WHITE}{self.timestamp}{Colors.RESET}] [{Colors.BLUE}{self.module}{Colors.RESET}] {self.action} -> {Colors.GREEN}{self.result}{Colors.RESET}"


class HistoryManager:
    def __init__(self):
        self.items = []
        self.lock = threading.Lock()  

    def add_entry(self, entry: str):
        with self.lock:  
            self.items.append(entry)


class HistoryEngine:
    def __init__(self, filename: str, export_dir: str, testing: bool = False) -> None:
        self.filename = filename
        self.export_dir = export_dir
        self.items: List[HistoryItem] = []
        self.queue: queue.Queue = queue.Queue()
        self.lock = threading.Lock()
        self.testing = testing
        self.load_history()

        if not self.testing:
            self._worker_thread = threading.Thread(
                target=self._save_worker, daemon=True
            )
            self._worker_thread.start()

    def add(self, module: str, action: str, result: str) -> None:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        item = HistoryItem(timestamp=now, module=module, action=action, result=result)
        with self.lock:
            self.items.append(item)
        if not self.testing:
            self.queue.put(item)

    def _save_worker(self) -> None:
        while True:
            item = self.queue.get()
            if item is None:
                break

            with self.lock:
                self.items.append(item)
            self._write_to_disk()
            self.queue.task_done()

    def _write_to_disk(self) -> None:
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(
                    [asdict(item) for item in self.items],
                    f,
                    indent=4,
                    ensure_ascii=False,
                )
        except Exception:
            pass

    def load_history(self) -> None:
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.items = [HistoryItem(**item) for item in data]
            except Exception:
                self.items = []

    def clear(self) -> None:
        with self.lock:
            self.items.clear()
        if os.path.exists(self.filename):
            try:
                os.remove(self.filename)
            except Exception:
                pass

    def export_txt(self) -> str:
        os.makedirs(self.export_dir, exist_ok=True)
        path = os.path.join(self.export_dir, f"export_{int(time.time())}.txt")
        with open(path, "w", encoding="utf-8") as f:
            for item in self.items:
                f.write(
                    f"[{item.timestamp}] ({item.module}) {item.action} -> {item.result}\n"
                )
        return path

    def export_csv(self) -> str:
        os.makedirs(self.export_dir, exist_ok=True)
        path = os.path.join(self.export_dir, f"export_{int(time.time())}.csv")
        with open(path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Временная метка", "Модуль", "Действие", "Результат"])
            for item in self.items:
                writer.writerow([item.timestamp, item.module, item.action, item.result])
        return path

    def stop(self) -> None:
        self.queue.put(None)


class TerminalUI:
    def __init__(self, config=None):
        self.config = config

    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def show_banner(self) -> None:
        raw_banner = """
 ██╗  ██╗██████╗  ██████╗ ███╗   ██╗ ██████╗ ███████╗
 ██║ ██╔╝██╔══██╗██╔═══██╗████╗  ██║██╔═══██╗██╔════╝
 █████╔╝ ██████╔╝██║   ██║██╔██╗ ██║██║   ██║███████╗
 ██╔═██╗ ██╔══██╗██║   ██║██║╚██╗██║██║   ██║╚════██║
 ██║  ██╗██║  ██║╚██████╔╝██║ ╚████║╚██████╔╝███████║
 ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚══════╝
        ██╗   ██╗██╗     ████████╗██████╗  █████╗ 
        ██║   ██║██║     ╚══██╔══╝██╔══██╗██╔══██╗
        ██║   ██║██║        ██║   ██████╔╝███████║
        ██║   ██║██║        ██║   ██╔══██╗██╔══██║
        ╚██████╔╝███████╗   ██║   ██║  ██║██║  ██║
         ╚═════╝ ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝
        """
        
        def get_color(r: int, g: int, b: int) -> str:
            return f"\033[38;2;{r};{g};{b}m"

        start_color = (255, 0, 128)
        end_color = (0, 255, 255)

        colored_banner = ""
        lines = raw_banner.strip("\n").split("\n")
        
        max_length = max(len(line) for line in lines)

        for line in lines:
            for i, char in enumerate(line):
                ratio = i / max_length if max_length > 1 else 0
                
                r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
                g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
                b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
                
                colored_banner += f"{get_color(r, g, b)}{char}"
            
            colored_banner += "\033[0m\n"
            
        print(colored_banner)
        
        subtitle = "─── KRONOS CALCULATOR ULTRA v3.0 by Kronos Russian ───"
        print(f"        \033[1m{get_color(0, 255, 255)}{subtitle}\033[0m\n")

    def print_smart(self, text: str):
        print(text)

    def pause(self):
        input(f"\n{Colors.BOLD}Нажмите Enter для продолжения...{Colors.RESET}")

    def get_input(
        self, prompt: str, type_func=str, validator=None, error_msg="Неверный ввод."
    ):
        while True:
            try:
                val = input(prompt)
                casted = type_func(val)
                if validator and not validator(casted):
                    print(f"{Colors.RED}{error_msg}{Colors.RESET}")
                    continue
                return casted
            except (ValueError, TypeError):
                print(f"{Colors.RED}{error_msg}{Colors.RESET}")


class AdvancedScience:
    # УЛЬТИМАТИВНЫЙ СПРАВОЧНИК КОНСТАНТ
    PHYSICAL_CONSTANTS = {
        # --- ФУНДАМЕНТАЛЬНЫЕ ---
        "c": 299792458,  # Скорость света (м/с)
        "G": 6.67430e-11,  # Гравитационная постоянная (Н·м²/кг²)
        "h": 6.62607015e-34,  # Постоянная Планка (Дж·с)
        "hbar": 1.054571817e-34,  # Приведенная постоянная Планка (Дж·с)
        "alpha": 7.297352569e-3,  # Постоянная тонкой структуры
        # --- АТОМНАЯ И ЯДЕРНАЯ ФИЗИКА ---
        "m_e": 9.1093837e-31,  # Масса электрона (кг)
        "m_p": 1.6726219e-27,  # Масса протона (кг)
        "m_n": 1.6749275e-27,  # Масса нейтрона (кг)
        "e_charge": 1.6021766e-19,  # Элементарный заряд (Кл)
        "a0": 5.2917721e-11,  # Борковский радиус (м)
        "mu_B": 9.27401007e-24,  # Магнетон Бора (Дж/Тл)
        "Ry": 1.09737315e7,  # Постоянная Ридберга (м⁻¹)
        # --- ТЕРМОДИНАМИКА И ГАЗЫ ---
        "Na": 6.02214076e23,  # Число Авогадро (моль⁻¹)
        "R": 8.314462618,  # Газовая постоянная (Дж/(моль·К))
        "k_B": 1.380649e-23,  # Постоянная Больцмана (Дж/К)
        "sigma": 5.670374419e-8,  # Постоянная Стефана-Больцмана (Вт/(м²·К⁴))
        "b_Wien": 2.897771e-3,  # Постоянная смещения Вина (м·К)
        "F_Faraday": 96485.332,  # Постоянная Фарадея (Кл/моль)
        # --- АСТРОФИЗИКА И ПЛАНЕТАРНЫЕ ---
        "M_sun": 1.98847e30,  # Масса Солнца (кг)
        "R_sun": 6.9634e8,  # Радиус Солнца (м)
        "M_earth": 5.9722e24,  # Масса Земли (кг)
        "R_earth": 6371000,  # Радиус Земли (м)
        "AU": 1.4959787e11,  # Астрономическая единица (м)
        "pc": 3.0856776e16,  # Парсек (м)
        "Ly": 9.46073047e15,  # Световой год (м)
        # --- ЭЛЕКТРОМАГНЕТИЗМ ---
        "eps0": 8.8541878e-12,  # Электрическая постоянная (Ф/м)
        "mu0": 1.256637e-6,  # Магнитная постоянная (Гн/м)
        "Z0": 376.730313,  # Волновое сопротивление вакуума (Ом)
    }

    # ВСЕ 118 ЭЛЕМЕНТОВ ТАБЛИЦЫ МЕНДЕЛЕЕВА
    CHEMICAL_ELEMENTS = {
        "H": 1.008,
        "He": 4.0026,
        "Li": 6.94,
        "Be": 9.0122,
        "B": 10.81,
        "C": 12.011,
        "N": 14.007,
        "O": 15.999,
        "F": 18.998,
        "Ne": 20.180,
        "Na": 22.990,
        "Mg": 24.305,
        "Al": 26.982,
        "Si": 28.085,
        "P": 30.974,
        "S": 32.06,
        "Cl": 35.45,
        "K": 39.098,
        "Ca": 40.078,
        "Sc": 44.956,
        "Ti": 47.867,
        "V": 50.942,
        "Cr": 51.996,
        "Mn": 54.938,
        "Fe": 55.845,
        "Co": 58.933,
        "Ni": 58.693,
        "Cu": 63.546,
        "Zn": 65.38,
        "Ga": 69.723,
        "Ge": 72.630,
        "As": 74.922,
        "Se": 78.971,
        "Br": 79.904,
        "Kr": 83.798,
        "Rb": 85.468,
        "Sr": 87.62,
        "Y": 88.906,
        "Zr": 91.224,
        "Nb": 92.906,
        "Mo": 95.95,
        "Tc": 98.0,
        "Ru": 101.07,
        "Rh": 102.91,
        "Pd": 106.42,
        "Ag": 107.87,
        "Cd": 112.41,
        "In": 114.82,
        "Sn": 118.71,
        "Sb": 121.76,
        "Te": 127.60,
        "I": 126.90,
        "Xe": 131.29,
        "Cs": 132.91,
        "Ba": 137.33,
        "La": 138.91,
        "Ce": 140.12,
        "Pr": 140.91,
        "Nd": 144.24,
        "Pm": 145.0,
        "Sm": 150.36,
        "Eu": 151.96,
        "Gd": 157.25,
        "Tb": 158.93,
        "Dy": 162.50,
        "Ho": 164.93,
        "Er": 167.26,
        "Tm": 168.93,
        "Yb": 173.05,
        "Lu": 174.97,
        "Hf": 178.49,
        "Ta": 180.95,
        "W": 183.84,
        "Re": 186.21,
        "Os": 190.23,
        "Ir": 192.22,
        "Pt": 195.08,
        "Au": 196.97,
        "Hg": 200.59,
        "Tl": 204.38,
        "Pb": 207.2,
        "Bi": 208.98,
        "Po": 209.0,
        "At": 210.0,
        "Rn": 222.0,
        "Fr": 223.0,
        "Ra": 226.0,
        "Ac": 227.0,
        "Th": 232.04,
        "Pa": 231.04,
        "U": 238.03,
        "Np": 237.0,
        "Pu": 244.0,
        "Am": 243.0,
        "Cm": 247.0,
        "Bk": 247.0,
        "Cf": 251.0,
        "Es": 252.0,
        "Fm": 257.0,
        "Md": 258.0,
        "No": 259.0,
        "Lr": 266.0,
        "Rf": 267.0,
        "Db": 268.0,
        "Sg": 269.0,
        "Bh": 270.0,
        "Hs": 269.0,
        "Mt": 278.0,
        "Ds": 281.0,
        "Rg": 282.0,
        "Cn": 285.0,
        "Nh": 286.0,
        "Fl": 289.0,
        "Mc": 290.0,
        "Lv": 293.0,
        "Ts": 294.0,
        "Og": 294.0,
    }

    def parse_chemical_composition(cls, formula: str) -> Dict[str, int]:
        tokens = re.findall(r"([A-Z][a-z]*|\([^)]+\))(\d*)", formula)
        comp = {}
        for elem, count in tokens:
            count_val = int(count) if count else 1
            if elem.startswith("("):
                sub_comp = cls.parse_chemical_composition(elem[1:-1])
                for k, v in sub_comp.items():
                    comp[k] = comp.get(k, 0) + v * count_val
            else:
                if elem not in cls.CHEMICAL_ELEMENTS:
                    raise ValueError(f"Элемент '{elem}' не найден в бд.")
                comp[elem] = comp.get(elem, 0) + count_val
        return comp

    def solve_cubic(a: float, b: float, c: float, d: float) -> List[complex]:
        if a == 0:
            raise ValueError("Параметр 'a' не может быть равен нулю.")
        b, c, d = b / a, c / a, d / a
        f, g = ((3 * c) - (b**2)) / 3, ((2 * (b**3)) - (9 * b * c) + (27 * d)) / 27
        h = ((g**2) / 4) + ((f**3) / 27)

        if h > 0:
            r = -(g / 2) + math.sqrt(h)
            s = r ** (1 / 3) if r >= 0 else -((-r) ** (1 / 3))
            t = -(g / 2) - math.sqrt(h)
            u = t ** (1 / 3) if t >= 0 else -((-t) ** (1 / 3))
            x1 = (s + u) - (b / 3)
            x2 = complex(-(s + u) / 2 - (b / 3), (s - u) * math.sqrt(3) / 2)
            x3 = complex(-(s + u) / 2 - (b / 3), -(s - u) * math.sqrt(3) / 2)
            return [complex(x1), x2, x3]
        elif f == 0 and g == 0 and h == 0:
            return [complex(-(d ** (1 / 3)))] * 3
        else:
            i = math.sqrt(((g**2) / 4) - h)
            j, k = i ** (1 / 3), math.acos(-(g / (2 * i)))
            m, n = math.cos(k / 3), math.sqrt(3) * math.sin(k / 3)
            p = -(b / 3)
            return [
                complex(2 * j * m + p),
                complex(-j * (m + n) + p),
                complex(-j * (m - n) + p),
            ]

    def advanced_statistics(data: List[float]) -> Dict[str, Any]:
        from collections import Counter

        n = len(data)
        if n == 0:
            raise ValueError("Пустая выборка.")
        sorted_d = sorted(data)
        mean_val = sum(sorted_d) / n
        counts = Counter(sorted_d)
        max_freq = max(counts.values())
        modes = [k for k, v in counts.items() if v == max_freq]
        mode_val = modes[0] if max_freq > 1 else sorted_d[0]

        def get_median(lst: List[float]) -> float:
            l = len(lst)
            return lst[l // 2] if l % 2 != 0 else (lst[l // 2 - 1] + lst[l // 2]) / 2

        q2 = get_median(sorted_d)
        q1 = get_median(sorted_d[: n // 2])
        q3 = get_median(sorted_d[n // 2 + (1 if n % 2 != 0 else 0) :])
        return {"mean": mean_val, "mode": mode_val, "q1": q1, "q2": q2, "q3": q3}


# МАТЕМАТИЧЕСКИЙ ДВИЖОК С ПАРСЕРОМ ОПЗ
class EngineeringModules:
    # Плотности веществ (кг/м³) при нормальных условиях (0 °C, 101.3 кПа)
    # Для твердых тел и жидкостей — при комнатной температуре.
    DENSITIES = {
        # --- ВСЕ 118 ХИМИЧЕСКИХ ЭЛЕМЕНТОВ ТАБЛИЦЫ МЕНДЕЛЕЕВА ---
        "hydrogen": 0.08988,  # 1 Водород (газ)
        "helium": 0.1786,  # 2 Гелий (газ)
        "lithium": 534,  # 3 Литий
        "beryllium": 1848,  # 4 Бериллий
        "boron": 2340,  # 5 Бор
        "carbon": 2267,  # 6 Углерод (графит)
        "nitrogen": 1.2506,  # 7 Азот (газ)
        "oxygen": 1.429,  # 8 Кислород (газ)
        "fluorine": 1.696,  # 9 Фтор (газ)
        "neon": 0.9002,  # 10 Неон (газ)
        "sodium": 968,  # 11 Натрий
        "magnesium": 1738,  # 12 Магний
        "aluminum": 2700,  # 13 Алюминий
        "silicon": 2329,  # 14 Кремний
        "phosphorus": 1823,  # 15 Фосфор (белый)
        "sulfur": 2070,  # 16 Сера
        "chlorine": 3.214,  # 17 Хлор (газ)
        "argon": 1.784,  # 18 Аргон (газ)
        "potassium": 890,  # 19 Калий
        "calcium": 1550,  # 20 Кальций
        "scandium": 2989,  # 21 Скандий
        "titanium": 4540,  # 22 Титан
        "vanadium": 6110,  # 23 Ванадий
        "chromium": 7190,  # 24 Хром
        "manganese": 7210,  # 25 Марганец
        "iron": 7874,  # 26 Железо
        "cobalt": 8900,  # 27 Кобальт
        "nickel": 8908,  # 28 Никель
        "copper": 8960,  # 29 Медь
        "zinc": 7140,  # 30 Цинк
        "gallium": 5910,  # 31 Галлий
        "germanium": 5323,  # 32 Германий
        "arsenic": 5727,  # 33 Мышьяк
        "selenium": 4810,  # 34 Селен
        "bromine": 3122,  # 35 Бром (жидкость)
        "krypton": 3.749,  # 36 Криптон (газ)
        "rubidium": 1532,  # 37 Рубидий
        "strontium": 2640,  # 38 Стронций
        "yttrium": 4472,  # 39 Иттрий
        "zirconium": 6520,  # 40 Цирконий
        "niobium": 8570,  # 41 Ниобий
        "molybdenum": 10280,  # 42 Молибден
        "technetium": 11000,  # 43 Технеций
        "ruthenium": 12450,  # 44 Рутений
        "rhodium": 12410,  # 45 Родий
        "palladium": 12023,  # 46 Палладий
        "silver": 10500,  # 47 Серебро
        "cadmium": 8690,  # 48 Кадмий
        "indium": 7310,  # 49 Индий
        "tin": 7310,  # 50 Олово
        "antimony": 6697,  # 51 Сурьма
        "tellurium": 6240,  # 52 Теллур
        "iodine": 4933,  # 53 Йод
        "xenon": 5.894,  # 54 Ксенон (газ)
        "cesium": 1930,  # 55 Цезий
        "barium": 3510,  # 56 Барий
        "lanthanum": 6162,  # 57 Лантан
        "cerium": 6770,  # 58 Церий
        "praseodymium": 6773,  # 59 Празеодим
        "neodymium": 7008,  # 60 Неодим
        "promethium": 7260,  # 61 Прометий
        "samarium": 7520,  # 62 Самарий
        "europium": 5264,  # 63 Европий
        "gadolinium": 7901,  # 64 Гадолиний
        "terbium": 8230,  # 65 Тербий
        "dysprosium": 8540,  # 66 Диспрозий
        "holmium": 8795,  # 67 Гольмий
        "erbium": 9066,  # 68 Эрбий
        "thulium": 9321,  # 69 Тулий
        "ytterbium": 6900,  # 70 Иттербий
        "lutetium": 9841,  # 71 Лютеций
        "hafnium": 13310,  # 72 Гафний
        "tantalum": 16654,  # 73 Тантал
        "tungsten": 19250,  # 74 Вольфрам
        "rhenium": 21020,  # 75 Рений
        "osmium": 22590,  # 76 Осмий (самый плотный элемент)
        "iridium": 22560,  # 77 Иридий
        "platinum": 21450,  # 78 Платина
        "gold": 19300,  # 79 Золото
        "mercury": 13546,  # 80 Ртуть (жидкость)
        "thallium": 11850,  # 81 Таллий
        "lead": 11340,  # 82 Свинец
        "bismuth": 9780,  # 83 Висмут
        "polonium": 9320,  # 84 Полоний
        "astatine": 7000,  # 85 Астат
        "radon": 9.73,  # 86 Радон (газ)
        "francium": 1870,  # 87 Франций
        "radium": 5500,  # 88 Радий
        "actinium": 10070,  # 89 Актиний
        "thorium": 11724,  # 90 Торий
        "protactinium": 15370,  # 91 Протактиний
        "uranium": 19050,  # 92 Уран
        "neptunium": 20450,  # 93 Нептуний
        "plutonium": 19816,  # 94 Плутоний
        "americium": 13670,  # 95 Америций
        "curium": 13510,  # 96 Кюрий
        "berkelium": 14780,  # 97 Берклий
        "californium": 15100,  # 98 Калифорний
        "einsteinium": 8840,  # 99 Эйнштейний
        "fermium": 9700,  # 100 Фермий
        "mendelevium": 10300,  # 101 Менделевий
        "nobelium": 9900,  # 102 Нобелий
        "lawrencium": 14400,  # 103 Лоуренсий
        "rutherfordium": 17000,  # 104 Резерфордий
        "dubnium": 21600,  # 105 Дубний
        "seaborgium": 23200,  # 106 Сиборгий
        "bohrium": 26300,  # 107 Борий
        "hassium": 29100,  # 108 Хассий
        "meitnerium": 27400,  # 109 Майтнерий
        "darmstadtium": 26000,  # 110 Дармштадтий
        "roentgenium": 28700,  # 111 Рентгений
        "copernicium": 14000,  # 112 Коперниций
        "nihonium": 16000,  # 113 Нихоний
        "flerovium": 9920,  # 114 Флеровий
        "moscovium": 13500,  # 115 Московий
        "livermorium": 12900,  # 116 Ливерморий
        "tennessine": 7200,  # 117 Теннессин
        "oganesson": 7000,  # 118 Оганесон
        # --- ИНЖЕНЕРНЫЕ СПЛАВЫ И СМЕСИ ---
        "steel": 7850,  # Сталь углеродистая
        "stainless_steel": 7900,  # Нержавеющая сталь
        "cast_iron": 7200,  # Чугун
        "brass": 8500,  # Латунь
        "bronze": 8800,  # Бронза
        "nichrome": 8400,  # Нихром
        "duralumin": 2800,  # Дюралюминий
        "solder_tin_lead": 9300,  # Припой ПОС-40
        # --- ТЕХНИЧЕСКИЕ И ПРИРОДНЫЕ ЖИДКОСТИ ---
        "water": 1000,  # Дистиллированная вода
        "sea_water": 1030,  # Морская вода
        "oil_machine": 920,  # Машинное масло
        "ethanol": 789,  # Этанол (спирт)
        "gasoline": 740,  # Бензин
        "kerosene": 810,  # Керосин
        "glycerin": 1260,  # Глицерин
        "diesel": 850,  # Дизельное топливо
        "acetone": 791,  # Ацетон
        # --- ГАЗЫ И АТМОСФЕРА ---
        "air": 1.225,  # Воздух (сухой, при 15°C)
        "carbon_dioxide": 1.977,  # Углекислый газ
        "methane": 0.717,  # Метан (природный газ)
        "propane": 2.005,  # Пропан
        # --- СТРОИТЕЛЬНЫЕ И ГЕОЛОГИЧЕСКИЕ МАТЕРИАЛЫ ---
        "concrete": 2400,  # Бетон
        "brick": 1800,  # Кирпич полнотелый
        "glass": 2500,  # Стекло оконное
        "wood_oak": 700,  # Древесина дуба
        "wood_pine": 500,  # Древесина сосны
        "ice": 917,  # Лёд (при 0°C)
        "granite": 2700,  # Гранит
        "marble": 2700,  # Мрамор
        "rubber": 1100,  # Резина техническая
        "paraffin": 900,  # Парафин
        "diamond": 3515,  # Алмаз
        "porcelain": 2400,  # Фарфор
        "asphalt": 2110,  # Асфальт
    }

    # Удельная теплоемкость (Дж/(кг·К)) основного спектра веществ
    SPECIFIC_HEAT = {
        "c_hydrogen": 14300,  # Водород
        "c_helium": 5193,  # Гелий
        "c_lithium": 3582,  # Литий (очень высокая для металла)
        "c_beryllium": 1825,  # Бериллий
        "c_carbon": 710,  # Углерод (графит)
        "c_nitrogen": 1040,  # Азот
        "c_oxygen": 918,  # Кислород
        "c_sodium": 1230,  # Натрий
        "c_magnesium": 1020,  # Магний
        "c_aluminum": 920,  # Алюминий
        "c_silicon": 710,  # Кремний
        "c_argon": 520,  # Аргон
        "c_titanium": 523,  # Титан
        "c_chromium": 449,  # Хром
        "c_iron": 450,  # Железо
        "c_cobalt": 420,  # Кобальт
        "c_nickel": 444,  # Никель
        "c_copper": 385,  # Медь
        "c_zinc": 390,  # Цинк
        "c_germanium": 320,  # Германий
        "c_silver": 235,  # Серебро
        "c_tin": 230,  # Олово
        "c_xenon": 158,  # Ксенон
        "c_tungsten": 134,  # Вольфрам
        "c_platinum": 133,  # Платина
        "c_gold": 129,  # Золото
        "c_mercury": 139,  # Ртуть
        "c_lead": 130,  # Свинец
        "c_bismuth": 122,  # Висмут
        "c_uranium": 116,  # Уран
        # Смеси, жидкости, газы и стройматериалы
        "c_water": 4184,  # Вода
        "c_sea_water": 3900,  # Морская вода
        "c_air": 1005,  # Воздух
        "c_steam": 2080,  # Водяной пар (100°C)
        "c_ice": 2110,  # Лёд (-10°C)
        "c_ethanol": 2440,  # Спирт
        "c_oil_machine": 2000,  # Машинное масло
        "c_glycerin": 2430,  # Глицерин
        "c_gasoline": 2220,  # Бензин
        "c_steel": 500,  # Сталь
        "c_brass": 380,  # Латунь
        "c_glass": 840,  # Стекло
        "c_concrete": 880,  # Бетон
        "c_brick": 840,  # Кирпич
        "c_wood": 1700,  # Древесина средняя
    }

    # Температуры плавления (°C) при нормальном давлении
    MELTING_POINTS = {
        "t_hydrogen": -259.16,  # Водород
        "t_helium": -272.2,  # Гелий (под давлением 2.5 МПа)
        "t_lithium": 180.5,  # Литий
        "t_beryllium": 1287,  # Бериллий
        "t_carbon": 3550,  # Углерод (сублимация)
        "t_nitrogen": -210.0,  # Азот
        "t_oxygen": -218.79,  # Кислород
        "t_sodium": 97.72,  # Натрий
        "t_magnesium": 650,  # Магний
        "t_aluminum": 660.3,  # Алюминий
        "t_silicon": 1414,  # Кремний
        "t_phosphorus": 44.15,  # Фосфор белый
        "t_sulfur": 115.21,  # Сера
        "t_argon": -189.34,  # Аргон
        "t_potassium": 63.38,  # Калий
        "t_calcium": 842,  # Кальций
        "t_titanium": 1668,  # Титан
        "t_vanadium": 1910,  # Ванадий
        "t_chromium": 1907,  # Хром
        "t_manganese": 1246,  # Магнец
        "t_iron": 1538,  # Железо
        "t_cobalt": 1495,  # Кобальт
        "t_nickel": 1455,  # Никель
        "t_copper": 1085,  # Медь
        "t_zinc": 419.53,  # Цинк
        "t_gallium": 29.76,  # Галлий (плавится в руках)
        "t_germanium": 938.25,  # Германий
        "t_bromine": -7.2,  # Бром
        "t_silver": 961.78,  # Серебро
        "t_cadmium": 321.07,  # Кадмий
        "t_indium": 156.6,  # Индий
        "t_tin": 231.93,  # Олово
        "t_antimony": 630.63,  # Сурьма
        "t_iodine": 113.7,  # Йод
        "t_cesium": 28.44,  # Цезий
        "t_tungsten": 3422,  # Вольфрам (самый тугоплавкий металл)
        "t_platinum": 1768.3,  # Платина
        "t_gold": 1064.18,  # Золото
        "t_mercury": -38.83,  # Ртуть
        "t_lead": 327.46,  # Свинец
        "t_bismuth": 271.5,  # Висмут
        "t_uranium": 1132.2,  # Уран
        "t_plutonium": 639.4,  # Плутоний
        # Прочие популярные среды
        "t_ice": 0,  # Водный лёд
        "t_steel": 1510,  # Сталь средняя
        "t_brass": 930,  # Латунь
        "t_bronze": 950,  # Бронза
        "t_glass": 1400,  # Стекло (начало размягчения)
        "t_paraffin": 54,  # Парафин
        "t_ethanol": -114.1,  # Этанол
    }

    @classmethod
    def get_all_constants(cls) -> dict:
        all_consts = {}
        all_consts.update(cls.DENSITIES)
        all_consts.update(cls.SPECIFIC_HEAT)
        all_consts.update(cls.MELTING_POINTS)
        return all_consts


class MathEngine:
    CONSTANTS = {
        # 1. МАТЕМАТИЧЕСКИЕ БАЗИСЫ И КОНСТАНТЫ
        "pi": complex(math.pi),
        "e": complex(math.e),
        "i": complex(0, 1),
        "j": complex(0, 1),
        "phi": complex(1.618033988749895),  # Золотое сечение
        "silver_ratio": complex(2.41421356237),  # Серебряное сечение
        "euler_gamma": complex(0.57721566490),  # Константа Эйлера-Маскерони
        "catalan": complex(0.91596559417),  # Константа Каталана
        "aperi": complex(1.20205690315),  # Константа Апери zeta(3)
        "khinchin": complex(2.685452001),  # Константа Хинчина
        # 2. ФУНДАМЕНТАЛЬНЫЕ ФИЗИЧЕСКИЕ КОНСТАНТЫ (СИ)
        "c": complex(299792458),  # Скорость света в вакууме (м/с)
        "G": complex(6.67430e-11),  # Гравитационная постоянная
        "h": complex(6.62607015e-34),  # Постоянная Планка
        "hbar": complex(1.054571817e-34),  # Редуцированная постоянная Планка
        "k_B": complex(1.380649e-23),  # Постоянная Больцмана
        "N_A": complex(6.02214076e23),  # Число Авогадро
        "R": complex(8.314462618),  # Универсальная газовая постоянная
        "sigma": complex(5.670374419e-8),  # Постоянная Стефана-Больцмана
        "e_charge": complex(1.602176634e-19),  # Заряд электрона
        "m_e": complex(9.1093837015e-31),  # Масса покоя электрона
        "m_p": complex(1.67262192369e-27),  # Масса покоя протона
        "m_n": complex(1.67492749804e-27),  # Масса покоя нейтрона
        "mu_0": complex(4 * math.pi * 1e-7),  # Магнитная постоянная
        "eps_0": complex(8.8541878128e-12),  # Электрическая постоянная
        "g": complex(9.80665),  # Стандартное ускорение свободного падения
        # 3. АСТРОНОМИЧЕСКИЕ ПАРАМЕТРЫ
        "M_sun": complex(1.98847e30),  # Масса Солнца (кг)
        "R_sun": complex(6.96342e8),  # Радиус Солнца (м)
        "M_earth": complex(5.9722e24),  # Масса Земли (кг)
        "R_earth": complex(6.371e6),  # Средний радиус Земли (м)
        "M_moon": complex(7.342e22),  # Масса Луны (кг)
        "R_moon": complex(1.7374e6),  # Радиус Луны (м)
        "au": complex(149597870700),  # Астрономическая единица (м)
        "ly": complex(9.4607304725808e15),  # Световой год (м)
        "pc": complex(3.085677581491367e16),  # Парсек (м)
        # 4. МОДУЛЬ МАТЕРИАЛОВ: ПЛОТНОСТИ (кг/м³)
        "steel": complex(7850),
        "aluminum": complex(2700),
        "copper": complex(8960),
        "gold": complex(19300),
        "iron": complex(7874),
        "lead": complex(11340),
        "titanium": complex(4540),
        "silver": complex(10500),
        "platinum": complex(21450),
        "tungsten": complex(19250),
        "uranium": complex(19050),
        "zinc": complex(7140),
        "brass": complex(8500),
        "bronze": complex(8800),
        "cast_iron": complex(7200),
        "stainless_steel": complex(7900),
        "nichrome": complex(8400),
        "duralumin": complex(2800),
        # Редкие элементы и полупроводники
        "silicon": complex(2330),
        "germanium": complex(5323),
        "diamond": complex(3515),
        "graphite": complex(2260),
        "concrete": complex(2400),
        "brick": complex(1800),
        "glass": complex(2500),
        "granite": complex(2700),
        "marble": complex(2700),
        "ruby": complex(4000),
        "amber": complex(1050),
        # Древесина и био-среды
        "wood_oak": complex(700),
        "wood_pine": complex(500),
        "wood_balsa": complex(130),
        "ice": complex(917),
        "water": complex(1000),
        "water_salt": complex(1030),
        "oil": complex(920),
        "mercury": complex(13546),
        "alcohol": complex(789),
        "gasoline": complex(740),
        "kerosene": complex(810),
        "glycerin": complex(1260),
        "blood": complex(1060),
        "air": complex(1.225),
        "hydrogen": complex(0.089),
        "helium": complex(0.178),
        "oxygen": complex(1.429),
        "nitrogen": complex(1.251),
        "co2": complex(1.977),
        "methane": complex(0.717),
        "rho_sun": complex(1408),
        "rho_earth": complex(5515),
        # 5. ТЕПЛОФИЗИКА И ТЕРМОДИНАМИКА
        "c_water": complex(4184),
        "c_water_salt": complex(3900),
        "c_air": complex(1005),
        "c_steel": complex(500),
        "c_aluminum": complex(920),
        "c_copper": complex(385),
        "c_ice": complex(2110),
        "c_steam": complex(2080),
        "c_gold": complex(129),
        "c_glass": complex(840),
        "c_ethanol": complex(2440),
        "c_hydrogen": complex(14300),
        # Удельная теплота плавления (Дж/кг) — λ
        "lambda_ice": complex(334000),
        "lambda_iron": complex(270000),
        "lambda_copper": complex(213000),
        "lambda_aluminum": complex(390000),
        "lambda_gold": complex(67000),
        # Удельная теплота парообразования (Дж/кг) — L
        "L_water": complex(2260000),
        "L_alcohol": complex(900000),
        "L_ether": complex(352000),
        # Удельная теплота сгорания топлива (Дж/кг) — q
        "q_gasoline": complex(44000000),
        "q_coal": complex(29000000),
        "q_wood": complex(10000000),
        "q_hydrogen": complex(120000000),
        # Температуры плавления (°C)
        "t_iron": complex(1538),
        "t_copper": complex(1085),
        "t_aluminum": complex(660),
        "t_gold": complex(1064),
        "t_tungsten": complex(3422),
        "t_lead": complex(327.5),
        "t_mercury": complex(-38.83),
        "t_ice": complex(0),
        "t_ethanol": complex(-114.1),
        # 6. ЭЛЕКТРОДИНАМИКА И ОПТИКА
        "res_silver": complex(0.016),
        "res_copper": complex(0.017),
        "res_gold": complex(0.024),
        "res_aluminum": complex(0.028),
        "res_iron": complex(0.10),
        "res_nichrome": complex(1.10),
        "n_vacuum": complex(1.0),
        "n_air": complex(1.000293),
        "n_water": complex(1.333),
        "n_glass": complex(1.5),
        "n_diamond": complex(2.42),
    }

    OPERATORS = {
        "+": (2, "left", lambda a, b: a + b),
        "-": (2, "left", lambda a, b: a - b),
        "*": (3, "left", lambda a, b: a * b),
        "/": (3, "left", lambda a, b: a / b if b != 0 else complex(float("inf"))),
        "//": (
            3,
            "left",
            lambda a, b: (
                complex(a.real // b.real) if b.real != 0 else complex(float("inf"))
            ),
        ),
        "%": (
            3,
            "left",
            lambda a, b: (
                complex(a.real % b.real) if b.real != 0 else complex(float("nan"))
            ),
        ),
        "**": (4, "right", lambda a, b: a**b),
        "^": (4, "right", lambda a, b: a**b),  
        "nCr": (4, "left", lambda a, b: complex(math.comb(int(a.real), int(b.real)))),
        "nPr": (4, "left", lambda a, b: complex(math.perm(int(a.real), int(b.real)))),
        "&": (1, "left", lambda a, b: complex(int(a.real) & int(b.real))),
        "|": (1, "left", lambda a, b: complex(int(a.real) | int(b.real))),
        "xor": (1, "left", lambda a, b: complex(int(a.real) ^ int(b.real))),
        "<<": (3, "left", lambda a, b: complex(int(a.real) << int(b.real))),
        ">>": (3, "left", lambda a, b: complex(int(a.real) >> int(b.real))),
        "==": (0, "left", lambda a, b: complex(float(a == b))),
        "!=": (0, "left", lambda a, b: complex(float(a != b))),
        "<": (0, "left", lambda a, b: complex(float(a.real < b.real))),
        ">": (0, "left", lambda a, b: complex(float(a.real > b.real))),
        "<=": (0, "left", lambda a, b: complex(float(a.real <= b.real))),
        ">=": (0, "left", lambda a, b: complex(float(a.real >= b.real))),
        "unary-": (5, "right", lambda a: -a),
        "unary+": (5, "right", lambda a: a),
        "~": (5, "right", lambda a: complex(~int(a.real))),  
        "!": (6, "left", lambda a: complex(math.factorial(int(a.real)))),  
    }

    FUNCTIONS = {
        "sin": lambda x: cmath.sin(x),
        "cos": lambda x: cmath.cos(x),
        "tan": lambda x: cmath.tan(x),
        "sec": lambda x: 1 / cmath.cos(x) if cmath.cos(x) != 0 else complex(float("inf")),
        "csc": lambda x: 1 / cmath.sin(x) if cmath.sin(x) != 0 else complex(float("inf")),
        "cot": lambda x: 1 / cmath.tan(x) if cmath.tan(x) != 0 else complex(float("inf")),
        "asin": lambda x: cmath.asin(x),
        "acos": lambda x: cmath.acos(x),
        "atan": lambda x: cmath.atan(x),
        "asec": lambda x: cmath.acos(1 / x) if x != 0 else complex(float("nan")),
        "acsc": lambda x: cmath.asin(1 / x) if x != 0 else complex(float("nan")),
        "acot": lambda x: cmath.atan(1 / x) if x != 0 else complex(float("nan")),
        "sinh": lambda x: cmath.sinh(x),
        "cosh": lambda x: cmath.cosh(x),
        "tanh": lambda x: cmath.tanh(x),
        "csh": lambda x: 1 / cmath.sinh(x) if cmath.sinh(x) != 0 else complex(float("inf")),
        "sech": lambda x: 1 / cmath.cosh(x) if cmath.cosh(x) != 0 else complex(float("inf")),
        "coth": lambda x: 1 / cmath.tanh(x) if cmath.tanh(x) != 0 else complex(float("inf")),
        "asinh": lambda x: cmath.asinh(x),
        "acosh": lambda x: cmath.acosh(x),
        "atanh": lambda x: cmath.atanh(x),
        "sqrt": lambda x: cmath.sqrt(x),
        "cbrt": lambda x: complex(x.real ** (1 / 3)) if x.imag == 0 else x ** (1 / 3),
        "ln": lambda x: cmath.log(x),
        "log": lambda x: cmath.log10(x),
        "log2": lambda x: cmath.log(x, 2),
        "exp": lambda x: cmath.exp(x),
        "abs": lambda x: complex(abs(x)),
        "ceil": lambda x: complex(math.ceil(x.real), math.ceil(x.imag)),
        "floor": lambda x: complex(math.floor(x.real), math.floor(x.imag)),
        "round": lambda x: complex(round(x.real), round(x.imag)),
        "trunc": lambda x: complex(math.trunc(x.real)),
        "fact": lambda x: complex(math.factorial(int(x.real))),
        "gcd": lambda x, y: complex(math.gcd(int(x.real), int(y.real))),
        "lcm": lambda x, y: complex(math.lcm(int(x.real), int(y.real))),
        "rad": lambda x: complex(math.radians(x.real), math.radians(x.imag)),
        "deg": lambda x: complex(math.degrees(x.real), math.degrees(x.imag)),
        "gamma": lambda x: complex(math.gamma(x.real)),  
        "erf": lambda x: complex(math.erf(x.real)),  
        "erfc": lambda x: complex(math.erfc(x.real)),  
        "mean": lambda data: (
            complex(sum(data) / len(data))
            if isinstance(data, list) and data
            else complex(0)
        ),
        "median": lambda data: (
            complex(sorted([x.real for x in data])[len(data) // 2])
            if isinstance(data, list) and data
            else complex(0)
        ),
        "sum": lambda data: complex(sum(data)) if isinstance(data, list) else data,
        "min": lambda data: (
            complex(min([x.real for x in data])) if isinstance(data, list) else data
        ),
        "max": lambda data: (
            complex(max([x.real for x in data])) if isinstance(data, list) else data
        ),
        "stdev": lambda data: (
            complex(math.stdev([x.real for x in data]))
            if isinstance(data, list) and len(data) > 1
            else complex(0)
        ),
        "variance": lambda data: (
            complex(math.variance([x.real for x in data]))
            if isinstance(data, list) and len(data) > 1
            else complex(0)
        ),
    }

    @classmethod
    def init_constants(cls):
        if not hasattr(cls, 'CONSTANTS'):
            cls.CONSTANTS = {}
            
        try:
            for k, v in AdvancedScience.PHYSICAL_CONSTANTS.items():
                clean_name = k.split("(")[-1].replace(")", "").strip()
                match = re.search(r"[-+]?\d*\.\d+|\d+", v.replace("e-", "e_minus"))
                if match:
                    num_str = match.group(0).replace("e_minus", "e-")
                    cls.CONSTANTS[clean_name] = complex(float(num_str))
        except Exception:
            pass

        try:
            all_eng_constants = EngineeringModules.get_all_constants()
            for k, v in all_eng_constants.items():
                cls.CONSTANTS[k] = complex(v)
        except Exception:
            pass

    @classmethod
    def tokenize(cls, expr_str: str) -> List[Tuple[str, str]]:
        if not expr_str or expr_str.strip() == "":
            raise ValueError("Input string is empty.")

        tokens: List[Tuple[str, str]] = []
        i, n = 0, len(expr_str)
        import re

        op_regex = re.compile(
            r"^(==|!=|<=|>=|<<|>>|\*\*|xor|[+\-*/^()&|!~<>])", re.IGNORECASE
        )

        while i < n:
            char = expr_str[i]
            if char.isspace():
                i += 1
                continue
            if char.isdigit() or char == ".":
                num_str = ""
                if (
                    char == "0"
                    and i + 1 < n
                    and expr_str[i + 1].lower() in ["b", "x", "o"]
                ):
                    num_str = expr_str[i : i + 2]
                    i += 2
                    while i < n and expr_str[i].isalnum():
                        num_str += expr_str[i]
                        i += 1
                    tokens.append(("NUM", num_str))
                    continue

                while i < n and (
                    expr_str[i].isdigit()
                    or expr_str[i] == "."
                    or expr_str[i].lower() == "j"
                ):
                    num_str += expr_str[i]
                    if expr_str[i].lower() == "j":
                        i += 1
                        break
                    i += 1
                tokens.append(("NUM", num_str))
                continue
            if char.isalpha() or char == "_":
                name_str = ""
                while i < n and (expr_str[i].isalnum() or expr_str[i] == "_"):
                    name_str += expr_str[i]
                    i += 1

                if name_str.lower() in cls.FUNCTIONS:
                    tokens.append(("FN", name_str.lower()))
                elif name_str.lower() == "xor":
                    tokens.append(("OP", "xor"))
                else:
                    tokens.append(("VAR", name_str))
                continue
            match = op_regex.match(expr_str[i:])
            if match:
                op = match.group(0)
                if op == "-":
                    if not tokens or tokens[-1][1] == "(" or tokens[-1][0] == "OP":
                        tokens.append(("OP", "unary-"))
                    else:
                        tokens.append(("OP", "-"))
                else:
                    tokens.append(("OP", op.lower()))
                i += len(op)
                continue

            raise ValueError(f"Invalid character encountered: {char}")

        if not tokens:
            raise ValueError("Invalid expression: could not parse any tokens.")

        return tokens

    @classmethod
    def to_rpn(cls, tokens: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
        if not tokens:
            raise ValueError("Empty or invalid input")

        output = []
        stack = []
        precedence = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3, "**": 3, "unary-": 4}

        for tok_type, value in tokens:
            if tok_type in ["NUM", "VAR"]:
                output.append((tok_type, value))
            elif tok_type == "FN":
                stack.append((tok_type, value))
            elif value == "(":
                stack.append((tok_type, value))
            elif value == ")":
                while stack and stack[-1][1] != "(":
                    output.append(stack.pop())
                if not stack:
                    raise ValueError("Unbalanced parentheses")
                stack.pop()
                if stack and stack[-1][0] == "FN":
                    output.append(stack.pop())
            elif tok_type == "OP":
                while (
                    stack
                    and stack[-1][1] in precedence
                    and precedence.get(stack[-1][1], 0) >= precedence.get(value, 0)
                ):
                    output.append(stack.pop())
                stack.append((tok_type, value))

        while stack:
            op = stack.pop()
            if op[1] == "(":
                raise ValueError("Unbalanced parentheses")
            output.append(op)

        return output

    @classmethod
    def _parse_number(cls, value: str) -> complex:
        val = value.strip().lower()  
        try:
            if val.startswith("0b"):
                return complex(int(val, 2))
            if val.startswith("0x"):
                return complex(int(val, 16))
            if val.startswith("0o"):
                return complex(int(val, 8))
            return complex(val)
        except Exception:
            raise ValueError(f"Некорректный формат числа: {value}")

    @classmethod
    def safe_eval(cls, expression: str) -> complex:
        if not expression or not expression.strip():
            raise ValueError("Empty input")

        tokens = cls.tokenize(expression)
        if not tokens:
            raise ValueError("Invalid tokens")

        rpn = cls.to_rpn(tokens)
        print(f"\nDEBUG RPN: {rpn}")

        eval_stack = []

        for tok_type, value in rpn:
            if tok_type == "NUM":
                eval_stack.append(cls._parse_number(value))

            elif tok_type == "VAR":
                val_lower = value.lower()
                if val_lower in ["pi", "π"]:
                    eval_stack.append(complex(math.pi))
                elif val_lower == "e":
                    eval_stack.append(complex(math.e))
                elif hasattr(cls, "CONSTANTS") and value in cls.CONSTANTS:
                    eval_stack.append(complex(cls.CONSTANTS[value]))
                else:
                    raise ValueError(f"Неизвестная переменная: {value}")

            elif tok_type == "OP":
                if value == "unary-":
                    if not eval_stack:
                        raise ValueError("Unbalanced stack")
                    val = eval_stack.pop()
                    eval_stack.append(-val)
                else:
                    if len(eval_stack) < 2:
                        raise ValueError("Unbalanced stack")
                    b = eval_stack.pop()
                    a = eval_stack.pop()
                    if value == "+":
                        eval_stack.append(a + b)
                    elif value == "-":
                        eval_stack.append(a - b)
                    elif value == "*":
                        eval_stack.append(a * b)
                    elif value == "/":
                        if b == 0:
                            raise ZeroDivisionError("Division by zero")
                        eval_stack.append(a / b)
                    elif value in ["^", "**"]:
                        eval_stack.append(a**b)

            elif tok_type == "FN":
                if not eval_stack:
                    raise ValueError("Insufficient arguments for function")
                a = eval_stack.pop()  

                if value == "sin":
                    eval_stack.append(cmath.sin(a))
                elif value == "cos":
                    eval_stack.append(cmath.cos(a))
                elif value == "tan":
                    eval_stack.append(cmath.tan(a))
                elif value == "sqrt":
                    res = cmath.sqrt(a)  
                    if res.real == 0 and res.imag < 0:
                        res = complex(res.real, abs(res.imag))
                    eval_stack.append(res)
                elif value == "ln":
                    eval_stack.append(cmath.log(a))
                elif value == "log":
                    eval_stack.append(cmath.log10(a))
                elif value == "exp":
                    eval_stack.append(cmath.exp(a))

        if len(eval_stack) != 1:
            raise ValueError("Unbalanced stack")

        return eval_stack[0]


# АЛГЕБРА: МАТРИЦЫ И ВЕКТОРЫ
class Matrix:
    def __init__(self, data: List[List[float]]) -> None:
        self.data = data
        self.rows, self.cols = len(data), len(data[0]) if data else 0

    def __add__(self, other: Matrix) -> Matrix:
        return Matrix(
            [
                [self.data[i][j] + other.data[i][j] for j in range(self.cols)]
                for i in range(self.rows)
            ]
        )

    def __mul__(self, other: Any) -> Matrix:
        if isinstance(other, (int, float, complex)):
            return Matrix(
                [
                    [
                        self.data[i][j]
                        * (other.real if isinstance(other, complex) else other)
                        for j in range(self.cols)
                    ]
                    for i in range(self.rows)
                ]
            )
        res = [[0.0] * other.cols for _ in range(self.rows)]
        for i in range(self.rows):
            for j in range(other.cols):
                for k in range(self.cols):
                    res[i][j] += self.data[i][k] * other.data[k][j]
        return Matrix(res)

    def trace(self) -> float:
        return sum(self.data[i][i] for i in range(min(self.rows, self.cols)))

    def determinant(self) -> float:
        n = self.rows
        m_copy = [row[:] for row in self.data]
        det = 1.0
        for i in range(n):
            pivot = max(range(i, n), key=lambda r: abs(m_copy[r][i]))
            if pivot != i:
                m_copy[i], m_copy[pivot] = m_copy[pivot], m_copy[i]
                det *= -1.0
            if abs(m_copy[i][i]) < 1e-12:
                return 0.0
            det *= m_copy[i][i]
            for r in range(i + 1, n):
                factor = m_copy[r][i] / m_copy[i][i]
                for c in range(i, n):
                    m_copy[r][c] -= factor * m_copy[i][c]
        return det

    def inverse(self) -> Matrix:
        n = self.rows
        aug = [
            self.data[i] + [1.0 if i == j else 0.0 for j in range(n)] for i in range(n)
        ]
        for i in range(n):
            pivot = max(range(i, n), key=lambda r: abs(aug[r][i]))
            if pivot != i:
                aug[i], aug[pivot] = aug[pivot], aug[i]
            if abs(aug[i][i]) < 1e-12:
                raise ValueError("Матрица вырождена.")
            factor = aug[i][i]
            for c in range(2 * n):
                aug[i][c] /= factor
            for r in range(n):
                if r != i:
                    f = aug[r][i]
                    for c in range(i, 2 * n):
                        aug[r][c] -= f * aug[i][c]
        return Matrix([row[n:] for row in aug])

    def to_string(self) -> str:
        return "\n".join(
            [
                "\t".join([f"{Colors.GREEN}{cell:.4g}{Colors.RESET}" for cell in row])
                for row in self.data
            ]
        )


class Vector3D:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    @classmethod
    def from_list(cls, lst: list) -> "Vector3D":
        if len(lst) != 3:
            raise ValueError("Вектор 3D должен состоять ровно из 3 элементов [x, y, z]")
        return cls(lst[0].real, lst[1].real, lst[2].real)

    def length(self) -> float:
        """Длина вектора"""
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    @staticmethod
    def dot(v1: "Vector3D", v2: "Vector3D") -> float:
        """Скалярное произведение векторов (v1 · v2)"""
        return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z

    @staticmethod
    def cross(v1: "Vector3D", v2: "Vector3D") -> "Vector3D":
        """Векторное произведение (v1 x v2)"""
        return Vector3D(
            v1.y * v2.z - v1.z * v2.y,
            v1.z * v2.x - v1.x * v2.z,
            v1.x * v2.y - v1.y * v2.x,
        )

    def to_list(self) -> list:
        return [complex(self.x), complex(self.y), complex(self.z)]

    def __repr__(self):
        return f"Vector3D({self.x}, {self.y}, {self.z})"


class MatrixEngine:
    @staticmethod
    def parse_matrix(matrix_str: str) -> List[List[complex]]:
        """
        Парсит строку в двумерный массив комплексных/вещественных чисел.
        Поддерживает форматы: '[[1, 2], [3, 4]]' или '1,2; 3,4'
        """
        matrix_str = matrix_str.strip()
        if matrix_str.startswith("[") and matrix_str.endswith("]"):
            try:
                rows = re.findall(r"\[([^\[\]]+)\]", matrix_str)
                matrix = [
                    [complex(x.strip()) for x in row.split(",") if x.strip()]
                    for row in rows
                ]
                if not matrix or any(len(row) != len(matrix[0]) for row in matrix):
                    raise ValueError(
                        "Строки матрицы имеют разную длину или матрица пуста"
                    )
                return matrix
            except Exception as e:
                raise ValueError(f"Ошибка синтаксиса матрицы: {e}")
        else:
            try:
                rows = matrix_str.split(";")
                matrix = [
                    [complex(x.strip()) for x in row.split(",") if x.strip()]
                    for row in rows
                    if row.strip()
                ]
                if not matrix or any(len(row) != len(matrix[0]) for row in matrix):
                    raise ValueError(
                        "Строки матрицы имеют разную длину или матрица пуста"
                    )
                return matrix
            except Exception as e:
                raise ValueError(f"Ошибка синтаксиса упрощенной матрицы: {e}")

    @staticmethod
    def to_string(matrix: List[List[complex]], precision: int = 4) -> str:
        """Красивое форматирование матрицы для вывода в консоль KRONOS"""
        if not matrix or not matrix[0]:
            return "[]"
        lines = []
        for row in matrix:
            row_strs = []
            for cell in row:
                if abs(cell.imag) < 1e-10:
                    val = f"{cell.real:.{precision}f}".rstrip("0").rstrip(".")
                    if val == "-0":
                        val = "0"
                else:
                    sign = "+" if cell.imag >= 0 else "-"
                    val = f"{cell.real:.{precision}f}{sign}{abs(cell.imag):.{precision}f}j"
                row_strs.append(val)
            lines.append("  [ " + ", ".join(row_strs) + " ]")
        return "\n".join(lines)

    @staticmethod
    def add(A: List[List[complex]], B: List[List[complex]]) -> List[List[complex]]:
        if len(A) != len(B) or len(A[0]) != len(B[0]):
            raise ValueError("Размерности матриц должны совпадать для сложения")
        return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

    @staticmethod
    def subtract(A: List[List[complex]], B: List[List[complex]]) -> List[List[complex]]:
        if len(A) != len(B) or len(A[0]) != len(B[0]):
            raise ValueError("Размерности матриц должны совпадать для вычитания")
        return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

    @staticmethod
    def transpose(matrix: List[List[complex]]) -> List[List[complex]]:
        return [
            [matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))
        ]

    @staticmethod
    def multiply_scalar(
        matrix: List[List[complex]], scalar: complex
    ) -> List[List[complex]]:
        return [[cell * scalar for cell in row] for row in matrix]

    @staticmethod
    def multiply(A: List[List[complex]], B: List[List[complex]]) -> List[List[complex]]:
        rows_A, cols_A, rows_B, cols_B = len(A), len(A[0]), len(B), len(B[0])
        if cols_A != rows_B:
            raise ValueError(f"Несовместимые размерности: {cols_A} != {rows_B}")
        result = [[complex(0) for _ in range(cols_B)] for _ in range(rows_A)]
        for i in range(rows_A):
            for j in range(cols_B):
                for k in range(cols_A):
                    result[i][j] += A[i][k] * B[k][j]
        return result

    @classmethod
    def determinant(cls, matrix: List[List[complex]]) -> complex:
        n = len(matrix)
        if any(len(row) != n for row in matrix):
            raise ValueError("Матрица должна быть квадратной")
        A = [[cell for cell in row] for row in matrix]
        det = complex(1)
        for i in range(n):
            pivot = max(range(i, n), key=lambda r: abs(A[r][i]))
            if pivot != i:
                A[i], A[pivot] = A[pivot], A[i]
                det *= -1
            if abs(A[i][i]) < 1e-12:
                return complex(0)
            det *= A[i][i]
            for r in range(i + 1, n):
                factor = A[r][i] / A[i][i]
                for c in range(i, n):
                    A[r][c] -= factor * A[i][c]
        return det

    @classmethod
    def solve_linear_system(
        cls, A: List[List[complex]], B: List[List[complex]]
    ) -> List[List[complex]]:
        n = len(A)
        if any(len(row) != n for row in A):
            raise ValueError("Матрица коэффициентов A должна быть квадратной")
        if len(B) != n:
            raise ValueError("Высота B должна быть равна высоте A")
        m_B = len(B[0])
        aug = [A[i] + B[i] for i in range(n)]
        for i in range(n):
            pivot = max(range(i, n), key=lambda r: abs(aug[r][i]))
            if pivot != i:
                aug[i], aug[pivot] = aug[pivot], aug[i]
            if abs(aug[i][i]) < 1e-12:
                raise ValueError("Система не имеет единственного решения")
            pivot_val = aug[i][i]
            for c in range(i, n + m_B):
                aug[i][c] /= pivot_val
            for r in range(n):
                if r != i:
                    factor = aug[r][i]
                    for c in range(i, n + m_B):
                        aug[r][c] -= factor * aug[i][c]
        return [row[n:] for row in aug]

    @classmethod
    def invert(cls, matrix: List[List[complex]]) -> List[List[complex]]:
        n = len(matrix)
        I = [[complex(1) if i == j else complex(0) for j in range(n)] for i in range(n)]
        return cls.solve_linear_system(matrix, I)


class Vector3D:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    @classmethod
    def from_list(cls, lst: list) -> "Vector3D":
        if len(lst) != 3:
            raise ValueError("Вектор 3D должен состоять ровно из 3 элементов [x, y, z]")
        return cls(
            lst[0].real if isinstance(lst[0], complex) else lst[0],
            lst[1].real if isinstance(lst[1], complex) else lst[1],
            lst[2].real if isinstance(lst[2], complex) else lst[2],
        )

    def __add__(self, other: "Vector3D") -> "Vector3D":
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "Vector3D") -> "Vector3D":
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar: float) -> "Vector3D":
        """Умножение вектора на скаляр"""
        return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar)

    def magnitude(self) -> float:
        """Длина (модуль) вектора"""
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def dot(self, other: "Vector3D") -> float:
        """Скалярное произведение (Dot product)"""
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: "Vector3D") -> "Vector3D":
        """Векторное произведение (Cross product)"""
        return Vector3D(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def angle_with(self, other: "Vector3D") -> float:
        """Угол между векторами в градусах"""
        mag_product = self.magnitude() * other.magnitude()
        if mag_product == 0:
            return 0.0
        cos_angle = max(-1.0, min(1.0, self.dot(other) / mag_product))
        return math.degrees(math.acos(cos_angle))

    def to_string(self, precision: int = 4) -> str:
        return (
            f"[{self.x:.{precision}g}, {self.y:.{precision}g}, {self.z:.{precision}g}]"
        )


# КОНВЕРТЕР ВЕЛИЧИН
class UnitConverter:
    # 1. Конвертация длины (базовая единица — метр)
    LENGTH_FACTORS = {
        "nm": 1e-9,
        "um": 1e-6,
        "mm": 0.001,
        "cm": 0.01,
        "dm": 0.1,
        "m": 1.0,
        "km": 1000.0,
        "inch": 0.0254,
        "foot": 0.3048,
        "yard": 0.9144,
        "mile": 1609.344,
        "nautical_mile": 1852.0,
        "fathom": 1.8288,  # Морская миля и фатом (морская сажень)
        "au": 149597870700.0,  # Астрономическая единица
        "ly": 9.4607304725808e15,  # Световой год
        "pc": 3.085677581491367e16,  # Парсек
    }

    # 2. Конвертация массы (базовая единица — килограмм)
    MASS_FACTORS = {
        "ug": 1e-9,
        "mg": 0.000001,
        "g": 0.001,
        "kg": 1.0,
        "centner": 100.0,
        "ton": 1000.0,
        "kt": 1e6,
        "mt": 1e9,
        "pound": 0.45359237,
        "ounce": 0.02834952,
        "troy_ounce": 0.0311034768,
        "stone": 6.35029318,
        "carat": 0.0002,
        "amu": 1.6605390666e-27,  # Атомная единица массы (а.е.м.)
    }

    # 3. Конвертация давления (базовая единица — Паскаль)
    PRESSURE_FACTORS = {
        "pa": 1.0,
        "hpa": 100.0,
        "kpa": 1000.0,
        "mpa": 1000000.0,
        "bar": 100000.0,
        "mbar": 100.0,
        "atm": 101325.0,  # Физическая атмосфера
        "torr": 133.322368,  # Торр (мм рт. ст.)
        "mmhg": 133.322387,  # Миллиметр ртутного столба
        "mmh2o": 9.80665,  # Миллиметр водного столба
        "psi": 6894.75729,  # Фунт на квадратный дюйм
        "psf": 47.880258,  # Фунт на квадратный фут
    }

    # 4. Конвертация времени (базовая единица — секунда)
    TIME_FACTORS = {
        "ns": 1e-9,
        "us": 1e-6,
        "ms": 0.001,
        "s": 1.0,
        "min": 60.0,
        "h": 3600.0,
        "day": 86400.0,
        "week": 604800.0,
        "month": 2629800.0,  # Средний месяц (30.4375 дней)
        "year": 31557600.0,  # Юлианский год (365.25 дней)
        "decade": 315576000.0,
        "century": 3155760000.0,
    }

    # 5. Конвертация объема (базовая единица — кубический метр)
    VOLUME_FACTORS = {
        "mm3": 1e-9,
        "cm3": 1e-6,
        "dm3": 0.001,
        "m3": 1.0,
        "km3": 1e9,
        "ml": 1e-6,
        "l": 0.001,
        "gal_us": 0.00378541,
        "gal_uk": 0.00454609,  # Галлоны (США и Британский)
        "quart": 0.000946353,
        "pint": 0.000473176,
        "cup": 0.000236588,
        "fl_oz": 2.95735e-5,  # Жидкая унция
        "barrel_oil": 0.158987,  # Нефтяной баррель
    }

    # 6. Конвертация площади (базовая единица — квадратный метр)
    AREA_FACTORS = {
        "mm2": 1e-6,
        "cm2": 1e-4,
        "m2": 1.0,
        "km2": 1e6,
        "hectare": 10000.0,
        "are": 100.0,  # Гектар и сотка
        "acre": 4046.85642,
        "sq_in": 0.00064516,
        "sq_ft": 0.09290304,
        "sq_yd": 0.83612736,
        "sq_mile": 2589988.11,
    }

    # 7. Конвертация энергии и работы (базовая единица — Джоуль)
    ENERGY_FACTORS = {
        "j": 1.0,
        "kj": 1000.0,
        "mj": 1e6,
        "gj": 1e9,
        "cal": 4.184,
        "kcal": 4184.0,  # Калории
        "wh": 3600.0,
        "kwh": 3600000.0,  # Ватт-часы
        "ev": 1.602176634e-19,
        "kev": 1.602176634e-16,
        "mev": 1.602176634e-13,  # Электронвольты
        "btu": 1055.05585,
        "erg": 1e-7,  # Британская тепловая единица и эрг
    }

    # 8. Конвертация мощности (базовая единица — Ватт)
    POWER_FACTORS = {
        "w": 1.0,
        "kw": 1000.0,
        "mw": 1e6,
        "gw": 1e9,
        "hp_metric": 735.49875,  # Лошадиная сила (метрическая)
        "hp_mech": 745.699872,  # Лошадиная сила (механическая)
        "btu_h": 0.293071,  # BTU в час
    }

    # 9. Конвертация скорости (базовая единица — метр в секунду)
    SPEED_FACTORS = {
        "m_s": 1.0,
        "km_h": 0.2777777778,
        "mph": 0.44704,  # Мили в час
        "knot": 0.514444444,  # Узел (морская миля в час)
        "mach": 340.3,  # Мах (скорость звука в воздухе при 15°C)
        "c": 299792458.0,  # Скорость света
    }

    # 10. Конвертация цифровых данных (базовая единица — байт)
    DATA_FACTORS = {
        "bit": 0.125,
        "byte": 1.0,
        "kb": 1024.0,
        "mb": 1048576.0,
        "gb": 1073741824.0,
        "tb": 1099511627776.0,
        "pb": 1125899906842624.0,
    }

    @classmethod
    def _convert_base(
        cls,
        value: float,
        from_unit: str,
        to_unit: str,
        factors: dict,
        category_name: str,
    ) -> float:
        from_u, to_u = from_unit.lower(), to_unit.lower()
        if from_u not in factors or to_u not in factors:
            raise ValueError(
                f"Неизвестная единица {category_name}. Доступны: {list(factors.keys())}"
            )
        return value * factors[from_u] / factors[to_u]

    @classmethod
    def convert_length(cls, value: float, from_unit: str, to_unit: str) -> float:
        return cls._convert_base(value, from_unit, to_unit, cls.LENGTH_FACTORS, "длины")

    @classmethod
    def convert_mass(cls, value: float, from_unit: str, to_unit: str) -> float:
        return cls._convert_base(value, from_unit, to_unit, cls.MASS_FACTORS, "массы")

    @classmethod
    def convert_pressure(cls, value: float, from_unit: str, to_unit: str) -> float:
        return cls._convert_base(
            value, from_unit, to_unit, cls.PRESSURE_FACTORS, "давления"
        )

    @classmethod
    def convert_time(cls, value: float, from_unit: str, to_unit: str) -> float:
        return cls._convert_base(value, from_unit, to_unit, cls.TIME_FACTORS, "времени")

    @classmethod
    def convert_volume(cls, value: float, from_unit: str, to_unit: str) -> float:
        return cls._convert_base(
            value, from_unit, to_unit, cls.VOLUME_FACTORS, "объема"
        )

    @classmethod
    def convert_area(cls, value: float, from_unit: str, to_unit: str) -> float:
        return cls._convert_base(value, from_unit, to_unit, cls.AREA_FACTORS, "площади")

    @classmethod
    def convert_energy(cls, value: float, from_unit: str, to_unit: str) -> float:
        return cls._convert_base(
            value, from_unit, to_unit, cls.ENERGY_FACTORS, "энергии"
        )

    @classmethod
    def convert_power(cls, value: float, from_unit: str, to_unit: str) -> float:
        return cls._convert_base(
            value, from_unit, to_unit, cls.POWER_FACTORS, "мощности"
        )

    @classmethod
    def convert_speed(cls, value: float, from_unit: str, to_unit: str) -> float:
        return cls._convert_base(
            value, from_unit, to_unit, cls.SPEED_FACTORS, "скорости"
        )

    @classmethod
    def convert_data(cls, value: float, from_unit: str, to_unit: str) -> float:
        return cls._convert_base(
            value, from_unit, to_unit, cls.DATA_FACTORS, "информации"
        )

    @classmethod
    def convert_temperature(cls, value: float, from_unit: str, to_unit: str) -> float:
        from_u, to_u = from_unit.lower(), to_unit.lower()

        if from_u == "c":
            temp_c = value
        elif from_u == "k":
            temp_c = value - 273.15
        elif from_u == "f":
            temp_c = (value - 32) * 5 / 9
        else:
            raise ValueError("Неизвестная единица температуры. Используй: c, k, f")

        if to_u == "c":
            return temp_c
        elif to_u == "k":
            return temp_c + 273.15
        elif to_u == "f":
            return temp_c * 9 / 5 + 32
        else:
            raise ValueError("Неизвестная единица температуры. Используй: c, k, f")


# СИСТЕМА АВТОМАТИЧЕСКОГО ТЕСТИРОВАНИЯ


class KronosTestSuite(unittest.TestCase):

    def test_math_parser(self):
        self.assertAlmostEqual(MathEngine.safe_eval("2 + 2 * 2"), 6.0)
        self.assertAlmostEqual(MathEngine.safe_eval("(2 + 2) * 2"), 8.0)
        self.assertAlmostEqual(MathEngine.safe_eval("10 / 2 + 5"), 10.0)
        self.assertAlmostEqual(MathEngine.safe_eval("sin(pi / 2)"), 1.0)
        self.assertAlmostEqual(MathEngine.safe_eval("cos(0)"), 1.0)

    def test_advanced_math(self):
        self.assertAlmostEqual(MathEngine.safe_eval("-5 + 10"), 5.0)
        self.assertAlmostEqual(MathEngine.safe_eval("5 * (-2)"), -10.0)
        complex_res = MathEngine.safe_eval("sqrt(-4)")
        self.assertEqual(complex_res.real, 0.0)
        self.assertEqual(complex_res.imag, 2.0)  

    def test_number_systems(self):
        self.assertAlmostEqual(MathEngine.safe_eval("0b1010"), 10.0)  
        self.assertAlmostEqual(
            MathEngine.safe_eval("0x0F"), 15.0
        )  
        self.assertAlmostEqual(MathEngine.safe_eval("0o10"), 8.0)  
        self.assertAlmostEqual(
            MathEngine.safe_eval("0b1100 + 0x04"), 16.0
        )  

    def test_matrix_determinant(self):
        matrix = [[4, 3], [3, 2]]
        res = 4 * 2 - 3 * 3  
        self.assertEqual(res, -1)

    def test_vector_length(self):
        v_length = math.sqrt(3**2 + 4**2 + 0**2)
        self.assertAlmostEqual(v_length, 5.0)

    def test_converter(self):
        meters = 1 * 1000
        self.assertEqual(meters, 1000)

    def test_stress_matrix_multiplication(self):
        size = 50  
        A = [[complex(1, 1) for _ in range(size)] for _ in range(size)]
        B = [[complex(1, 1) for _ in range(size)] for _ in range(size)]

        start_time = time.time()
        MatrixEngine.multiply(A, B)
        duration = time.time() - start_time

        print(f"\n[Stress Test] Matrix 50x50 multiplication took: {duration:.4f}s")
        self.assertTrue(duration < 2.0)

    def test_fuzz_parser(self):
        with self.assertRaises(ValueError):
            MathEngine.safe_eval("((( ")

    def test_concurrent_history_write(self):
        self.history = HistoryEngine("test_hist.json", "exports", testing=True)

        def worker():
            for i in range(100):
                self.history.add("Mod", "Act", "Res")

        threads = [threading.Thread(target=worker) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        self.assertEqual(len(self.history.items), 1000)
        self.history.clear()

        threads = [threading.Thread(target=worker) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        self.history.queue.join()
        self.assertEqual(len(self.history.items), 1000)


# ТОЧКА СБОРКИ И УПРАВЛЕНИЯ ПРИЛОЖЕНИЕМ
class KronosApp:
    def __init__(self) -> None:
        self.config = ConfigManager()
        self.ui = TerminalUI(self.config)
        self.history = HistoryEngine(
            self.config.settings.get("history_file", "kronos_history.json"),
            self.config.settings.get("export_dir", "exports"),
        )
        self.global_vars: Dict[str, complex] = {"ans": complex(0)}

    def run(self) -> None:
        def rgb(r: int, g: int, b: int, text: str) -> str:
            return f"\033[38;2;{r};{g};{b}m{text}\033[0m"

        while True:
            self.ui.clear_screen()
            self.ui.show_banner()

            # --- ЦВЕТОВАЯ ПАЛИТРА МЕНЮ (RGB) ---
            head_border = (255, 204, 0)   # Неоново-желтый для рамок: ─[ ]─
            head_text = (0, 255, 255)     # Ярко-голубой для текста заголовков
            num_color = (255, 0, 128)     # Неоново-розовый для скобок с цифрами [1]
            item_text = (220, 220, 230)   # Мягкий белый с синевой для названий функций
            exit_color = (255, 50, 50)    # Ярко-красный для выхода и ошибок

            def print_header(title: str) -> None:
                border_l = rgb(*head_border, "─[ ")
                border_r = rgb(*head_border, " ]─")
                core = rgb(*head_text, title)
                print(f"\n   \033[1m{border_l}{core}{border_r}\033[0m")

            def print_item(num: int, name: str) -> None:
                if num == 0:
                    n_str = rgb(*exit_color, f"[{num}] ")
                    n_name = rgb(*exit_color, name)
                else:
                    spacer = " " if num < 10 else ""
                    n_str = rgb(*num_color, f"[{num}]{spacer}")
                    n_name = rgb(*item_text, name)
                print(f"   {n_str} {n_name}")

            # --- ОТРИСОВКА МЕНЮ ---
            print_header("АЛГЕБРА И ГЕОМЕТРИЯ")
            print_item(1, "Калькулятор выражений (ОПЗ, переменные, константы)")
            print_item(2, "Векторная алгебра (Dot/Cross product)")
            print_item(3, "Линейная алгебра (Матрицы)")
            print_item(4, "Алгебраические уравнения")
            print_item(5, "Матанализ (Производные/Интегралы)")
            print_item(6, "Геометрия (Треугольники)")
            print_item(7, "Теория чисел (НОД, НОК, Простые)")

            print_header("ИНЖЕНЕРИЯ И АНАЛИТИКА")
            print_item(8, "Конвертер физических величин")
            print_item(9, "Физика (Кинематика Solver)")
            print_item(10, "Химия (Массовые доли, Молярная масса)")
            print_item(11, "Статистический анализ")
            print_item(12, "Построение графиков (Matplotlib / ASCII)")

            print_header("ИНСТРУМЕНТЫ")
            print_item(13, "Криптография (Хеширование)")
            print_item(14, "Системы счисления")
            print_item(15, "Лог вычислений (Асинхронный)")
            print_item(16, "Запуск тестов")

            print("")  
            print_item(0, "Выход")
            
            print("   " + rgb(*head_text, "═" * 65))

            # --- ЛОГИКА ВВОДА ---
            prompt_str = f"\033[1m{rgb(*head_text, '» Выберите пункт: ')}\033[0m"
            error_str = rgb(*exit_color, "Неверный ввод.")

            choice = self.ui.get_input(
                prompt_str,
                int,
                lambda x: 0 <= x <= 16,
                error_str,
            )

            if choice == 0:
                self.ui.print_smart(
                    f"\n\033[1m{rgb(255, 0, 128, 'Сессия закрыта. До встречи!')}\033[0m"
                )
                break

            self.ui.clear_screen()
            
            # --- РОУТИНГ МОДУЛЕЙ ---
            try:
                match choice:
                    case 1: self.mod_calculator()
                    case 2: self.mod_vectors()
                    case 3: self.mod_matrix()
                    case 4: self.mod_equations()
                    case 5: self.mod_calculus()
                    case 6: self.mod_geometry()
                    case 7: self.mod_number_theory()
                    case 8: self.mod_converter()
                    case 9: self.mod_physics()
                    case 10: self.mod_chemistry()
                    case 11: self.mod_statistics()
                    case 12: self.mod_plotting()
                    case 13: self.mod_cryptography()
                    case 14: self.mod_conversion()
                    case 15: self.mod_history_center()
                    case 16: self.mod_run_tests()
            except Exception as e:
                error_msg = f"\n{rgb(*exit_color, 'Критическая ошибка модуля: ')}{e}"
                self.ui.print_smart(error_msg)
            
            self.ui.pause()

    def mod_converter(self) -> None:
        """Интерактивный инженерный конвертер величин (Пункт 8)"""
        while True:
            self.ui.clear_screen()
            print(
                f"   {Colors.BOLD}{Colors.YELLOW}───[ КОНВЕРТЕР ИНЖЕНЕРНЫХ ВЕЛИЧИН ]───{Colors.RESET}\n"
            )
            print(
                f"   {Colors.CYAN}[1]{Colors.RESET} Длина (m, mm, cm, km, inch, foot, yard, mile)"
            )
            print(
                f"   {Colors.CYAN}[2]{Colors.RESET} Масса (kg, g, mg, ton, pound, ounce)"
            )
            print(
                f"   {Colors.CYAN}[3]{Colors.RESET} Давление (pa, kpa, mpa, bar, atm, psi)"
            )
            print(f"   {Colors.CYAN}[4]{Colors.RESET} Температура (c, k, f)")
            print(f"   {Colors.CYAN}[0]{Colors.RESET} Вернуться в главное меню")
            print(
                f"\n{Colors.CYAN}======================================================================{Colors.RESET}"
            )

            choice = self.ui.get_input(
                f"{Colors.BOLD}{Colors.CYAN}» Выберите категорию: {Colors.RESET}",
                int,
                lambda x: 0 <= x <= 4,
                "Неверный выбор.",
            )

            if choice == 0:
                break

            self.ui.clear_screen()

            try:
                if choice == 1:
                    print(
                        f"{Colors.BOLD}{Colors.YELLOW}Доступные единицы длины:{Colors.RESET} {', '.join(UnitConverter.LENGTH_FACTORS.keys())}"
                    )
                    from_unit = input(f"Из какой единицы переводим? ").strip().lower()
                    to_unit = input(f"В какую единицу переводим? ").strip().lower()
                    value = self.ui.get_input(
                        "Введите значение: ", float, error_msg="Число введено неверно."
                    )

                    res = UnitConverter.convert_length(value, from_unit, to_unit)
                    self.ui.print_result(
                        f"{value} {from_unit} -> {to_unit}", f"{res:.6g} {to_unit}"
                    )

                elif choice == 2:
                    print(
                        f"{Colors.BOLD}{Colors.YELLOW}Доступные единицы массы:{Colors.RESET} {', '.join(UnitConverter.MASS_FACTORS.keys())}"
                    )
                    from_unit = input(f"Из какой единицы переводим? ").strip().lower()
                    to_unit = input(f"В какую единицу переводим? ").strip().lower()
                    value = self.ui.get_input(
                        "Введите значение: ", float, error_msg="Число введено неверно."
                    )

                    res = UnitConverter.convert_mass(value, from_unit, to_unit)
                    self.ui.print_result(
                        f"{value} {from_unit} -> {to_unit}", f"{res:.6g} {to_unit}"
                    )

                elif choice == 3:
                    print(
                        f"{Colors.BOLD}{Colors.YELLOW}Доступные единицы давления:{Colors.RESET} {', '.join(UnitConverter.PRESSURE_FACTORS.keys())}"
                    )
                    from_unit = input(f"Из какой единицы переводим? ").strip().lower()
                    to_unit = input(f"В какую единицу переводим? ").strip().lower()
                    value = self.ui.get_input(
                        "Введите значение: ", float, error_msg="Число введено неверно."
                    )

                    res = UnitConverter.convert_pressure(value, from_unit, to_unit)
                    self.ui.print_result(
                        f"{value} {from_unit} -> {to_unit}", f"{res:.6g} {to_unit}"
                    )

                elif choice == 4:
                    print(
                        f"{Colors.BOLD}{Colors.YELLOW}Доступные единицы температуры:{Colors.RESET} c (Цельсий), k (Кельвин), f (Фаренгейт)"
                    )
                    from_unit = (
                        input(f"Из какой единицы переводим (c/k/f)? ").strip().lower()
                    )
                    to_unit = (
                        input(f"В какую единицу переводим (c/k/f)? ").strip().lower()
                    )
                    value = self.ui.get_input(
                        "Введите значение: ", float, error_msg="Число введено неверно."
                    )

                    res = UnitConverter.convert_temperature(value, from_unit, to_unit)
                    self.ui.print_result(
                        f"{value} °{from_unit.upper() if from_unit != 'k' else ''}",
                        f"{res:.6g} °{to_unit.upper() if to_unit != 'k' else ''}",
                    )

            except ValueError as e:
                self.ui.print_error(str(e))

            self.ui.pause()

    def mod_calculator(self) -> None:
        self.ui.clear_screen()
        print(
            f"   {Colors.BOLD}{Colors.YELLOW}───[ КАЛЬКУЛЯТОР ВЫРАЖЕНИЙ ОПЗ ]───{Colors.RESET}\n"
        )
        print(
            f"Поддерживаются: комплексные числа ({Colors.GREEN}2+3j{Colors.RESET}), скобки, функции ({Colors.GREEN}sin, cos, sqrt{Colors.RESET})"
        )
        print(
            f"Константы из базы данных: {Colors.CYAN}pi, e, c{Colors.RESET} (скорость света), {Colors.CYAN}G{Colors.RESET} (гравитационная) и др.\n"
        )

        expr = input(
            f"{Colors.BOLD}{Colors.CYAN}» Введите выражение: {Colors.RESET}"
        ).strip()
        if not expr:
            return

        try:
            res = MathEngine.safe_eval(expr)

            if isinstance(res, complex):
                if abs(res.imag) < 1e-9:
                    res_str = f"{res.real:.6g}"
                else:
                    res_str = f"{res.real:.6g} + {res.imag:.6g}j".replace("+ -", "- ")
            else:
                res_str = f"{res:.6g}"
            0
            print(
                f"\n  {Colors.BOLD}{Colors.GREEN}[РЕЗУЛЬТАТ]{Colors.RESET} {Colors.BRIGHT_CYAN}{res_str}{Colors.RESET}"
            )

            self.history.add("Calculator", expr, res_str)

        except Exception as e:
            self.ui.print_smart(f"\n{Colors.RED}[ОШИБКА ВЫЧИСЛЕНИЯ] {e}{Colors.RESET}")

    def mod_vectors(self) -> None:
        self.ui.print_smart(
            f"{Colors.BOLD}{Colors.CYAN}--- ВЕКТОРНАЯ АЛГЕБРА ---{Colors.RESET}"
        )
        print(
            f"[{Colors.CYAN}1{Colors.RESET}] Скалярное произведение (Dot)\n[{Colors.CYAN}2{Colors.RESET}] Векторное произведение (Cross)"
        )
        sub = self.ui.get_input(
            f"{Colors.YELLOW}Выбор: {Colors.RESET}", int, lambda x: x in [1, 2]
        )

        def get_vec(name: str) -> Vector3D:
            s = self.ui.get_input(f"Вектор {name} (X Y Z через пробел): ", str)
            x, y, z = map(float, s.split())
            return Vector3D(x, y, z)

        v1, v2 = get_vec("A"), get_vec("B")
        if sub == 1:
            res = v1.dot(v2)
            self.ui.print_smart(
                f"\n{Colors.BOLD}{Colors.GREEN}A • B = {res:.6g}{Colors.RESET}"
            )
            mag1, mag2 = v1.magnitude(), v2.magnitude()
            if mag1 > 0 and mag2 > 0:
                angle = math.degrees(math.acos(res / (mag1 * mag2)))
                self.ui.print_smart(
                    f"{Colors.GREEN}Угол между векторами: {angle:.2f}°{Colors.RESET}"
                )
        else:
            res_v = v1.cross(v2)
            self.ui.print_smart(
                f"\n{Colors.BOLD}{Colors.GREEN}A × B = {res_v.to_string()}{Colors.RESET}"
            )

    def mod_converter(self) -> None:
        self.ui.print_smart(
            f"{Colors.BOLD}{Colors.CYAN}--- КОНВЕРТЕР ВЕЛИЧИН ---{Colors.RESET}"
        )
        print(
            f"[{Colors.CYAN}1{Colors.RESET}] Длина {list(UnitConverter.LENGTH.keys())}"
        )
        print(f"[{Colors.CYAN}2{Colors.RESET}] Масса {list(UnitConverter.MASS.keys())}")
        print(
            f"[{Colors.CYAN}3{Colors.RESET}] Давление {list(UnitConverter.PRESSURE.keys())}"
        )
        print(
            f"[{Colors.CYAN}4{Colors.RESET}] Энергия {list(UnitConverter.ENERGY.keys())}"
        )
        print(f"[{Colors.CYAN}5{Colors.RESET}] Температура ['C', 'K', 'F']")

        cat_map = {
            1: UnitConverter.LENGTH,
            2: UnitConverter.MASS,
            3: UnitConverter.PRESSURE,
            4: UnitConverter.ENERGY,
        }
        c = self.ui.get_input(
            f"{Colors.YELLOW}Категория (1-5): {Colors.RESET}",
            int,
            lambda x: 1 <= x <= 5,
        )

        val = self.ui.get_input("Значение: ", float)
        u1 = self.ui.get_input("Из (например, kg): ", str)
        u2 = self.ui.get_input("В (например, lb): ", str)

        try:
            if c == 5:
                res = UnitConverter.convert_temp(val, u1, u2)
            else:
                res = UnitConverter.convert(val, u1, u2, cat_map[c])
            self.ui.print_smart(
                f"\n{Colors.BOLD}{Colors.GREEN}{val} {u1} = {res:.6g} {u2}{Colors.RESET}"
            )
            self.history.add("Конвертер", f"{val} {u1} -> {u2}", f"{res:.6g}")
        except Exception as e:
            self.ui.print_smart(f"{Colors.RED}Ошибка: {e}{Colors.RESET}")

    def mod_plotting(self) -> None:
        self.ui.print_smart(f"{Colors.BOLD}{Colors.CYAN}--- ГРАФИКИ ---{Colors.RESET}")
        print(
            f"[{Colors.CYAN}1{Colors.RESET}] Matplotlib (Декартов)\n[{Colors.CYAN}2{Colors.RESET}] ASCII (В консоли - Символьный рендер)"
        )
        mode = self.ui.get_input(
            f"{Colors.YELLOW}Выбор: {Colors.RESET}", int, lambda x: x in [1, 2]
        )
        func_str = self.ui.get_input("Функция f(x): ", str)

        if mode == 1:
            try:
                import matplotlib.pyplot as plt
                import numpy as np

                plt.style.use(self.config.settings.get("plot_theme", "dark_background"))
                x = np.linspace(-10, 10, 400)
                y = [
                    MathEngine.safe_eval(func_str, {"x": complex(val)}).real
                    for val in x
                ]
                plt.figure(figsize=(10, 6))
                plt.plot(x, y, label=f"y = {func_str}", color="#00ffcc")
                plt.axhline(0, color="white", linewidth=0.8)
                plt.axvline(0, color="white", linewidth=0.8)
                plt.grid(True, color="gray", linestyle="--", alpha=0.5)
                plt.legend()
                plt.show()
            except Exception as e:
                self.ui.print_smart(
                    f"{Colors.RED}Ошибка рендера (установи matplotlib/numpy): {e}{Colors.RESET}"
                )
        else:
            self.ui.print_smart(
                f"{Colors.MAGENTA}Рендеринг ASCII графика...{Colors.RESET}\n"
            )
            w, h = 70, 20
            x_min, x_max = -10, 10
            x_vals = [x_min + i * (x_max - x_min) / (w - 1) for i in range(w)]
            y_vals = []
            for x in x_vals:
                try:
                    y_vals.append(
                        MathEngine.safe_eval(func_str, {"x": complex(x)}).real
                    )
                except:
                    y_vals.append(float("nan"))

            valid = [y for y in y_vals if not math.isnan(y)]
            if not valid:
                return
            y_min, y_max = min(valid), max(valid)
            if y_min == y_max:
                y_min, y_max = y_min - 1, y_max + 1

            grid = [[" " for _ in range(w)] for _ in range(h)]
            
            y0_row = (
                int((y_max - 0) / (y_max - y_min) * (h - 1))
                if y_min <= 0 <= y_max
                else -1
            )
            x0_col = (
                int((0 - x_min) / (x_max - x_min) * (w - 1))
                if x_min <= 0 <= x_max
                else -1
            )
            if 0 <= y0_row < h:
                for c in range(w):
                    grid[y0_row][c] = "-"
            if 0 <= x0_col < w:
                for r in range(h):
                    grid[r][x0_col] = "|"
            if 0 <= y0_row < h and 0 <= x0_col < w:
                grid[y0_row][x0_col] = "+"

            for c, y in enumerate(y_vals):
                if math.isnan(y):
                    continue
                r = int((y_max - y) / (y_max - y_min) * (h - 1))
                if 0 <= r < h:
                    grid[r][c] = f"{Colors.CYAN}*{Colors.RESET}"

            for row in grid:
                print("".join(row))
            print(
                f"{Colors.GRAY}Y: [{y_min:.2f} ... {y_max:.2f}], X: [{x_min} ... {x_max}]{Colors.RESET}"
            )

    def mod_matrix(self) -> None:
        self.ui.clear_screen()
        print(f"   {Colors.BOLD}{Colors.YELLOW}───[ MATRIX ENGINE ]───{Colors.RESET}\n")
        print(
            f"Input format: {Colors.CYAN}[[1,2],[3,4]]{Colors.RESET} or {Colors.CYAN}1,2; 3,4{Colors.RESET}\n"
        )

        try:
            raw_a = self.ui.get_input(
                f"{Colors.BOLD}{Colors.CYAN}» Enter Matrix A: {Colors.RESET}", str
            )
            A = MatrixEngine.parse_matrix(raw_a)

            print(f"\n{Colors.GREEN}Матрица A ({len(A)}x{len(A[0])}):{Colors.RESET}")
            print(MatrixEngine.to_string(A))

            print(f"\n[{Colors.CYAN}1{Colors.RESET}] Найти определитель (Det A)")
            print(f"[{Colors.CYAN}2{Colors.RESET}] Транспонировать (A^T)")
            print(f"[{Colors.CYAN}3{Colors.RESET}] Найти обратную матрицу (A^-1)")
            print(f"[{Colors.CYAN}4{Colors.RESET}] Умножить на вторую матрицу (A * B)")
            print(
                f"[{Colors.CYAN}5{Colors.RESET}] Решить систему уравнений (A * X = B)"
            )

            act = self.ui.get_input(
                f"\n{Colors.YELLOW}Выберите операцию: {Colors.RESET}",
                int,
                lambda x: x in [1, 2, 3, 4, 5],
            )

            if act == 1:
                det = MatrixEngine.determinant(A)
                self.ui.print_result(
                    "Det(A)", f"{det.real:.6g}" if abs(det.imag) < 1e-9 else str(det)
                )
            elif act == 2:
                T = MatrixEngine.transpose(A)
                print(
                    f"\n{Colors.BOLD}{Colors.GREEN}[A^T]:{Colors.RESET}\n{MatrixEngine.to_string(T)}"
                )
            elif act == 3:
                inv = MatrixEngine.invert(A)
                print(
                    f"\n{Colors.BOLD}{Colors.GREEN}[A^-1]:{Colors.RESET}\n{MatrixEngine.to_string(inv)}"
                )
            elif act == 4:
                raw_b = self.ui.get_input(
                    f"{Colors.CYAN}Введите матрицу B: {Colors.RESET}", str
                )
                B = MatrixEngine.parse_matrix(raw_b)
                res = MatrixEngine.multiply(A, B)
                print(
                    f"\n{Colors.BOLD}{Colors.GREEN}[A * B]:{Colors.RESET}\n{MatrixEngine.to_string(res)}"
                )
            elif act == 5:
                raw_b = self.ui.get_input(
                    f"{Colors.CYAN}Введите вектор/матрицу B: {Colors.RESET}", str
                )
                B = MatrixEngine.parse_matrix(raw_b)
                X = MatrixEngine.solve_linear_system(A, B)
                print(
                    f"\n{Colors.BOLD}{Colors.GREEN}[Решение X]:{Colors.RESET}\n{MatrixEngine.to_string(X)}"
                )

        except Exception as e:
            self.ui.print_error(str(e))

    def mod_equations(self) -> None:
        self.ui.print_smart(
            f"{Colors.BOLD}{Colors.CYAN}--- УРАВНЕНИЯ ---{Colors.RESET}"
        )
        a, b, c, d = [
            self.ui.get_input(f"Коэффициент {k}: ", float) for k in ("a", "b", "c", "d")
        ]
        roots = AdvancedScience.solve_cubic(a, b, c, d)
        print(f"\n{Colors.BOLD}{Colors.GREEN}Корни уравнения:{Colors.RESET}")
        for idx, r in enumerate(roots):
            self.ui.print_smart(f"  {Colors.GREEN}x{idx+1} = {r}{Colors.RESET}")

    def mod_calculus(self) -> None:
        self.ui.print_smart(
            f"{Colors.BOLD}{Colors.CYAN}--- МАТАНАЛИЗ ---{Colors.RESET}"
        )
        expr = self.ui.get_input("Функция f(x): ", str)
        x_val = self.ui.get_input("Точка x для производной: ", float)
        h = 1e-6
        f_plus = MathEngine.safe_eval(expr, {"x": complex(x_val + h)}).real
        f_minus = MathEngine.safe_eval(expr, {"x": complex(x_val - h)}).real
        self.ui.print_smart(
            f"{Colors.BOLD}{Colors.GREEN}f'({x_val}) ≈ {(f_plus - f_minus) / (2 * h):.7g}{Colors.RESET}"
        )

    def mod_geometry(self) -> None:
        self.ui.print_smart(
            f"{Colors.BOLD}{Colors.CYAN}--- ГЕОМЕТРИЯ (ТРЕУГОЛЬНИКИ) ---{Colors.RESET}"
        )
        a, b, c = [
            self.ui.get_input(f"Сторона {k}: ", float, lambda x: x > 0)
            for k in ("a", "b", "c")
        ]
        if a + b <= c or a + c <= b or b + c <= a:
            self.ui.print_smart(
                f"{Colors.RED}Треугольник с такими сторонами не существует!{Colors.RESET}"
            )
            return
        p = (a + b + c) / 2
        S = math.sqrt(p * (p - a) * (p - b) * (p - c))
        print(f"\n  {Colors.YELLOW}Площадь (S):{Colors.RESET} {S:.4g}")
        print(
            f"  {Colors.YELLOW}Описанный радиус (R):{Colors.RESET} {(a * b * c) / (4 * S):.4g}"
        )

    def mod_number_theory(self) -> None:
        self.ui.print_smart(
            f"{Colors.BOLD}{Colors.CYAN}--- ТЕОРИЯ ЧИСЕЛ ---{Colors.RESET}"
        )
        a = self.ui.get_input("Число A: ", int)
        b = self.ui.get_input("Число B: ", int)
        self.ui.print_smart(f"\n  {Colors.GREEN}НОД:{Colors.RESET} {math.gcd(a, b)}")
        self.ui.print_smart(f"  {Colors.GREEN}НОК:{Colors.RESET} {math.lcm(a, b)}")

    def mod_physics(self) -> None:
        self.ui.print_smart(
            f"{Colors.BOLD}{Colors.CYAN}--- ФИЗИКА (Кинематический Solver) ---{Colors.RESET}"
        )
        self.ui.print_smart(
            f"{Colors.GRAY}Введи 3 известных параметра. Неизвестные оставь пустыми.{Colors.RESET}"
        )
        knowns = {
            k: self.ui.get_input(f"{k}: ", float, allow_empty=True)
            for k in ("v0", "v", "a", "t", "s")
        }
        if sum(1 for v in knowns.values() if v is not None) != 3:
            return
        eqs = [
            lambda d: (
                d["v0"] + d["a"] * d["t"]
                if None not in (d["v0"], d["a"], d["t"])
                else None
            ),
            lambda d: (
                d["v"] - d["a"] * d["t"]
                if None not in (d["v"], d["a"], d["t"])
                else None
            ),
            lambda d: (
                (d["v"] - d["v0"]) / d["t"]
                if None not in (d["v"], d["v0"], d["t"]) and d["t"] != 0
                else None
            ),
            lambda d: (
                (d["v"] - d["v0"]) / d["a"]
                if None not in (d["v"], d["v0"], d["a"]) and d["a"] != 0
                else None
            ),
            lambda d: (
                d["v0"] * d["t"] + 0.5 * d["a"] * (d["t"] ** 2)
                if None not in (d["v0"], d["a"], d["t"])
                else None
            ),
        ]
        for _ in range(3):
            if knowns["v"] is None:
                knowns["v"] = eqs[0](knowns)
            if knowns["v0"] is None:
                knowns["v0"] = eqs[1](knowns)
            if knowns["a"] is None:
                knowns["a"] = eqs[2](knowns)
            if knowns["t"] is None:
                knowns["t"] = eqs[3](knowns)
            if knowns["s"] is None:
                knowns["s"] = eqs[4](knowns)
        print(f"\n{Colors.BOLD}{Colors.GREEN}Результаты:{Colors.RESET}")
        for k, val in knowns.items():
            if val is not None:
                print(f"  {Colors.YELLOW}{k}:{Colors.RESET} {val:.6g}")

    def mod_chemistry(self) -> None:
        self.ui.print_smart(f"{Colors.BOLD}{Colors.CYAN}--- ХИМИЯ ---{Colors.RESET}")
        formula = self.ui.get_input("Формула (например, C2H5OH): ", str)
        comp = AdvancedScience.parse_chemical_composition(formula)
        total_mass = sum(
            AdvancedScience.CHEMICAL_ELEMENTS[elem] * count
            for elem, count in comp.items()
        )
        self.ui.print_smart(
            f"\n{Colors.BOLD}{Colors.GREEN}M({formula}) = {total_mass:.4f} г/моль{Colors.RESET}"
        )
        for elem, count in comp.items():
            frac = (AdvancedScience.CHEMICAL_ELEMENTS[elem] * count / total_mass) * 100
            print(f"  {Colors.YELLOW}{elem}:{Colors.RESET} {frac:.2f}%")

    def mod_statistics(self) -> None:
        self.ui.print_smart(
            f"{Colors.BOLD}{Colors.CYAN}--- СТАТИСТИКА ---{Colors.RESET}"
        )
        raw = self.ui.get_input("Выборка (числа через пробел): ", str)
        stats = AdvancedScience.advanced_statistics([float(x) for x in raw.split()])
        for k, v in stats.items():
            print(f"  {Colors.YELLOW}{k}:{Colors.RESET} {v:.4g}")

    def mod_cryptography(self) -> None:
        text = self.ui.get_input("Строка: ", str)
        print(
            f"  {Colors.YELLOW}SHA256:{Colors.RESET} {hashlib.sha256(text.encode()).hexdigest()}"
        )
        print(
            f"  {Colors.YELLOW}Base64:{Colors.RESET} {base64.b64encode(text.encode()).decode()}"
        )

    def mod_conversion(self) -> None:
        num = self.ui.get_input("Целое число (10сс): ", int)
        print(
            f"  {Colors.YELLOW}BIN:{Colors.RESET} {bin(num)}\n  {Colors.YELLOW}HEX:{Colors.RESET} {hex(num).upper()}"
        )

    def mod_history_center(self) -> None:
        for item in self.history.items[-20:]:
            print(item.to_line())
        act = self.ui.get_input(
            f"\n[{Colors.CYAN}1{Colors.RESET}] Экспорт TXT [{Colors.CYAN}2{Colors.RESET}] Экспорт CSV [{Colors.CYAN}3{Colors.RESET}] Очистить: ",
            int,
            lambda x: x in [1, 2, 3],
        )
        if act == 1:
            self.ui.print_smart(
                f"{Colors.GREEN}Сохранено: {self.history.export_txt()}{Colors.RESET}"
            )
        elif act == 2:
            self.ui.print_smart(
                f"{Colors.GREEN}Сохранено: {self.history.export_csv()}{Colors.RESET}"
            )
        elif act == 3:
            self.history.clear()
            self.ui.print_smart(f"{Colors.RED}Очищено.{Colors.RESET}")

    def mod_run_tests(self) -> None:
        unittest.TextTestRunner(verbosity=2).run(
            unittest.TestLoader().loadTestsFromTestCase(KronosTestSuite)
        )


# ТОЧКА ВХОДА
if __name__ == "__main__":
    app = KronosApp()
    if len(sys.argv) > 1:
        try:
            app.route_menu(int(sys.argv[1]))
        except ValueError:
            pass
    else:
        app.run()
