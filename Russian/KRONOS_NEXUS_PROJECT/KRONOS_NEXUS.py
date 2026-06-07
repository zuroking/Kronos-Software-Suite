import os
import sys
import subprocess
import time
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.align import Align  

console = Console()

AVAILABLE_MODELS = {
    "1": "qwen2.5:3b",
    "2": "deepseek-r1:8b",
    "3": "deepseek-r1:1.5b",
    "4": "gemma2:2b",
    "5": "qwen2.5-coder:3b",
    "6": "phi3:latest"
}
CURRENT_MODEL = "qwen2.5:3b" 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODULES_DIR = os.path.join(BASE_DIR, "modules")
DATA_DIR = os.path.join(BASE_DIR, "data")

def Проверить_инфраструктуру():
    """Автоматически создает папки модулей и данных, если они отсутствуют"""
    for folder in [MODULES_DIR, DATA_DIR]:
        if not os.path.exists(folder):
            os.makedirs(folder)

def Запустить_модуль(script_name):
    """Запускает модуль в изолированном процессе для полной выгрузки из ОЗУ при выходе"""
    script_path = os.path.join(MODULES_DIR, script_name)
    
    if not os.path.exists(script_path):
        console.print(f"\n[bold red]❌ Ошибка: Модуль {script_name} отсутствует в директории modules/![/bold red]\n")
        input("Нажмите Enter для возврата в Хаб...")
        return

    console.print(f"\n[bold cyan]🚀 Инициализация подпроцесса {script_name} на ядре {CURRENT_MODEL}...[/bold cyan]\n")
    try:
        env = os.environ.copy()
        env["KRONOS_MODEL"] = CURRENT_MODEL
        
        subprocess.run([sys.executable, script_path], env=env)
    except Exception as e:
        console.print(f"[bold red]💥 Критический сбой внутри модуля: {e}[/bold red]")
        input("Нажмите Enter для аварийного возврата в Хаб...")

def Управление_ядрами():
    global CURRENT_MODEL
    while True:
        console.clear()
        console.print(Panel("[bold yellow]⚙ КОНФИГУРАЦИЯ ИИ-ЯДРА KRONOS NEXUS[/bold yellow]", style="yellow", expand=False))
        console.print(f"\nТекущее активное ядро: [bold cyan]{CURRENT_MODEL}[/bold cyan]\n")
        
        console.print("[bold green]💻 Оптимально для твоего Ноутбука (Быстрый отклик):[/bold green]")
        console.print("  1. Переключить на [bold green]qwen2.5:3b[/bold green] (Универсальный ассистент)")
        console.print("  3. Переключить на [bold green]deepseek-r1:1.5b[/bold green] (Легкое ИИ-рассуждение)")
        console.print("  4. Переключить на [bold green]gemma2:2b[/bold green] (Живой диалог от Google)")
        console.print("  5. Переключить на [bold green]qwen2.5-coder:3b[/bold green] (Программирование и парсинг)")
        console.print("  6. Переключить на [bold green]phi3:latest[/bold green] (Строгая логика от Microsoft)")
        
        console.print("\n[bold red]🔥 Тяжелые модели (Высокая нагрузка на CPU):[/bold red]")
        console.print("  2. Переключить на [bold purple]deepseek-r1:8b[/bold purple] (Глубокий ИИ-аудит и математика)")
        
        console.print("\n0. Вернуться в Главный Хаб\n")
        
        choices = list(AVAILABLE_MODELS.keys()) + ["0"]
        choice = Prompt.ask("Выберите вычислительное ядро", choices=choices)
        
        if choice == "0":
            break
            
        if choice in AVAILABLE_MODELS:
            SELECTED_MODEL = AVAILABLE_MODELS[choice]
            
            if choice == "2":
                console.print("\n[bold orange3]⚠ ВНИМАНИЕ:[/bold orange3] Выбрано ядро 8B. На твоем устройстве генерация будет идти медленно (на CPU). Идеально для ПК с RTX.")
                confirm = Prompt.ask("Продолжить активацию?", choices=["y", "n"], default="y")
                if confirm == "n":
                    continue
            
            CURRENT_MODEL = SELECTED_MODEL
            console.print(f"\n[bold green]✔ Ядро успешно перенаправлено на {CURRENT_MODEL}![/bold green]")
            time.sleep(1.5)

def Главное_меню():
    """Отрисовка интерфейса главного хаба управления"""
    Проверить_инфраструктуру()
    
    while True:
        console.clear()
        banner = """
   __   ██╗  ██╗██████╗  ██████╗ ███╗   ██╗ ██████╗ ███████╗  __
  /_/   ██║ ██╔╝██╔══██╗██╔═══██╗████╗  ██║██╔═══██╗██╔════╝ /_/
        █████╔╝ ██████╔╝██║   ██║██╔██╗ ██║██║   ██║███████╗
        ██╔═██╗ ██╔══██╗██║   ██║██║╚██╗██║██║   ██║╚════██║
  ██╗   ██║  ██╗██║  ██║╚██████╔╝██║ ╚████║╚██████╔╝███████║  ██╗
  ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚══════╝  ╚═╝
        """
        console.print(Align(f"[bold cyan]{banner}[/bold cyan]", align="center"))
        console.print(Align("[bold white]⚡ СИСТЕМА АВТОНОМНЫХ МОДУЛЕЙ СЕМЕЙНОЙ ИНТЕЛЛЕКТУАЛЬНОЙ ЭКОСИСТЕМЫ ⚡[/bold white]\n", align="center"))
    
        status_text = f"Активное ИИ-Ядро: [bold magenta]{CURRENT_MODEL}[/bold magenta] | Статус ОЗУ: [bold green]Стабилен (Lazy Loading)[/bold green]"
        status_panel = Panel(status_text, style="dim white", expand=False)
        console.print(Align(status_panel, align="center"))
        
        console.print("\n[bold white]ДОСТУПНЫЕ ИНСТРУМЕНТЫ ЭКОСИСТЕМЫ:[/bold white]\n")
        
        console.print("1. 💬 [bold white]KRONOS TERMINAL CHAT[/bold white]    — Собеседник с долгосрочной контекстной памятью")
        console.print("2. 🌪️  [bold white]DATA VORTEX PARSER[/bold white]      — Анализатор больших текстов и выжимка документов")
        console.print("3. 📐 [bold white]SMART SOLVER[/bold white]            — Пошаговый математический и кодовый решатель")
        console.print("4. 📝 [bold white]DATA GENERATOR[/bold white]          — Автономный создатель баз данных и отчетов")
        console.print("5. 💻 [bold cyan]KRONOS COMMANDER[/bold cyan]        — [КИЛЛЕР-ФИЧА] Управление ОС Windows")
        console.print("6. 🧠 [bold white]KRONOS MENTOR[/bold white]           — Модуль кастомного ИИ-ментора ")
        console.print("────────────────────────────────────────────────────────────────────────────────")
        console.print("9. ⚙  [bold yellow]КОНФИГУРАЦИЯ ИИ-ЯДРА[/bold yellow]    — Смена активной нейросети (Qwen / DeepSeek)")
        console.print("0. ❌ [bold red]ВЫХОД ИЗ СИСТЕМЫ[/bold red]        — Завершение работы всех процессов Nexus")
        console.print("")

        choice = Prompt.ask("Выполнить запуск модуля", choices=["1", "2", "3", "4", "5", "6", "9", "0"])

        if choice == "1":
            Запустить_модуль("kronos_chat.py")
        elif choice == "2":
            Запустить_модуль("kronos_vortex.py")
        elif choice == "3":
            Запустить_модуль("kronos_solver.py")
        elif choice == "4":
            Запустить_модуль("kronos_generator.py")
        elif choice == "5":
            Запустить_модуль("kronos_commander.py")
        elif choice == "6":
            Запустить_модуль("kronos_mentor.py")
        elif choice == "9":
            Управление_ядрами()
        elif choice == "0":
            console.print("\n[bold red]⚡ KRONOS AI NEXUS отключен. Все дочерние процессы завершены.[/bold red]\n")
            sys.exit(0)

if __name__ == "__main__":
    Главное_меню()