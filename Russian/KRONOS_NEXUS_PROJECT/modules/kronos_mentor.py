# ⚡ KRONOS AI NEXUS: DYNAMIC AI MENTOR & ASSISTANT

import os
import sys
import ollama
import time
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()
MODEL_NAME = os.environ.get("KRONOS_MODEL", "qwen2.5:3b")

def Очистить_экран():
    console.clear()

def Фильтровать_мысли(text):
    if "</think>" in text:
        return text.split("</think>")[-1].strip()
    return text.strip()

def Запустить_калькулятор_весов():
    console.print(Panel("📊 ЛОКАЛЬНЫЙ КАЛЬКУЛЯТОР НАГРУЗОК KRONOS", style="bold green", expand=False))
    try:
        bench_press = float(Prompt.ask("[bold white]Ваш максимум в жиме лежа на 1 повтор (кг)[/bold white]", default="50"))
        working_weight_80 = bench_press * 0.80
        working_weight_70 = bench_press * 0.70
        
        console.print(f"\n[bold green]✔ Расчет окончен:[/bold green]")
        console.print(f"  • Силовая работа (80% от 1ПМ): [yellow]{working_weight_80:.1f} кг[/yellow]")
        console.print(f"  • Работа на массу (70% от 1ПМ): [yellow]{working_weight_70:.1f} кг[/yellow]\n")
    except Exception:
        console.print("[red]❌ Ошибка ввода данных.[/red]\n")
    input("Нажмите Enter, чтобы продолжить...")

def Динамическая_сессия_ИИ():
    Очистить_экран()
    console.print(Panel("🧠 НАСТРОЙКА ЛИЧНОСТИ ИИ KRONOS", style="bold magenta", expand=False))
    
    custom_role = Prompt.ask(
        "[bold yellow]Опишите, кем должен быть ИИ (его роль, характер, правила)[/bold yellow]\n"
        "Пример: Ты жесткий тренер по бодибилдингу / Ты китаевед и эксперт по WeChat\n"
        "Ввод"
    ).strip()

    if not custom_role:
        console.print("[red]Роль не может быть пустой![/red]")
        time.sleep(1.5)
        return

    system_instruction = f"{custom_role} ОТВЕЧАЙ СТРОГО НА РУССКОМ ЯЗЫКЕ."

    Очистить_экран()
    console.print(Panel(f"🔮 РЕЖИМ АКТИВИРОВАН: {custom_role[:50]}...", style="bold cyan"))
    console.print("[dim]Для выхода в меню модуля введите /exit[/dim]\n")

    while True:
        user_input = Prompt.ask("[bold cyan]User >>[/bold cyan] ").strip()
        if user_input.lower() == '/exit':
            break
        if not user_input:
            continue

        with console.status("[bold magenta]ИИ обрабатывает запрос в заданной роли...[/bold magenta]"):
            try:
                response = ollama.chat(model=MODEL_NAME, messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": user_input}
                ])
                reply = Фильтровать_мысли(response['message']['content'])
                console.print(f"\n[bold magenta]🤖 ОТВЕТ КРОНОСА:[/bold magenta]\n{reply}\n")
            except Exception as e:
                console.print(f"[bold red]❌ Ошибка связи с ядром: {e}[/bold red]")

def Главное_меню():
    while True:
        Очистить_экран()
        banner = """
   🧠 KRONOS CUSTOMIZABLE MENTOR
        """
        console.print(Panel(banner.strip(), style="bold magenta", expand=False))
        console.print("  [1] 🔮 Задать роль для ИИ и начать диалог")
        console.print("  [2] 🏋️  Запустить калькулятор рабочих весов (Python)")
        console.print("  [0] 🚪 Выход в Главный Хаб")
        
        choice = Prompt.ask("\n[bold white]Выберите действие[/bold white]", choices=["1", "2", "0"])
        
        if choice == "1":
            Динамическая_сессия_ИИ()
        elif choice == "2":
            Запустить_калькулятор_весов()
        elif choice == "0":
            break

if __name__ == "__main__":
    Главное_меню()