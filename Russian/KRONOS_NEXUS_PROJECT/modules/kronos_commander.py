# ⚡ KRONOS AI NEXUS: COMMANDER MODE

import os
import sys
import subprocess
import webbrowser
import ollama
from rich.console import Console
from rich.panel import Panel

console = Console()
MODEL_NAME = os.environ.get("KRONOS_MODEL", "qwen2.5:3b")

COMMANDER_PROMPT = (
    "Ты — исполнительный модуль KRONOS COMMANDER для ОС Windows. "
    "Твоя задача — переводить текстовые команды пользователя в системные действия. "
    "Ты должен вернуть ответ СТРОГО в одном из трех форматов, без лишних слов, здорований и пояснений:\n\n"
    "1) Если пользователя просит открыть сайт: URL:[адрес сайта] (например, URL:https://github.com)\n"
    "2) Если нужно запустить программу через CMD: CMD:[команда] (например, CMD:notepad.exe или CMD:calc.exe)\n"
    "3) Если команда непонятна или опасна: ERROR:[сообщение об ошибке]\n\n"
    "Примеры соответствия:\n"
    "- 'открой блокнот' -> CMD:notepad.exe\n"
    "- 'запусти калькулятор' -> CMD:calc.exe\n"
    "- 'открой гугл' -> URL:https://google.com\n"
    "- 'покажи код проекта' -> CMD:code .\n"
    "Будь точен. Не пиши ничего, кроме указанного шаблона."
)

def Выполнить_системное_действие(ai_response):
    """Парсит ответ от ИИ и превращает его в реальное действие в Windows"""
    ai_response = ai_response.strip()
    
    if ai_response.startswith("URL:"):
        url = ai_response.replace("URL:", "").strip()
        console.print(f"[bold green]🌐 Открываю веб-ресурс:[/bold green] {url}")
        webbrowser.open(url)
        
    elif ai_response.startswith("CMD:"):
        cmd = ai_response.replace("CMD:", "").strip()
        console.print(f"[bold cyan]💻 Выполняю системную команду:[/bold cyan] {cmd}")
        subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
    elif ai_response.startswith("ERROR:"):
        error_msg = ai_response.replace("ERROR:", "").strip()
        console.print(f"[bold red]❌ Отказ системы:[/bold red] {error_msg}")
        
    else:
        console.print(f"[bold yellow]⚠️ Ядро вернуло неформатированный текст. Попытка прямого анализа...[/bold yellow]")
        if "блокнот" in ai_response.lower():
            subprocess.Popen("notepad.exe", shell=True)
        elif "калькулятор" in ai_response.lower():
            subprocess.Popen("calc.exe", shell=True)
        else:
            console.print("[red]Не удалось распознать системный паттерн.[/red]")

def Запустить_командира():
    console.clear()
    banner = """
    💻 KRONOS OS COMMANDER MODE ACTIVATED
    """
    console.print(Panel(banner.strip(), style="bold cyan", expand=False))
    console.print("[dim]Доступ к ядру ОС Windows открыт. Команда [red]/exit[/red] — возврат в Хаб.[/dim]\n")

    while True:
        user_input = console.input("[bold red]KRONOS // Напиши команду » [/bold red]").strip()

        if user_input.lower() == '/exit':
            break
        if not user_input:
            continue

        messages = [
            {"role": "system", "content": COMMANDER_PROMPT},
            {"role": "user", "content": f"Голосовая/текстовая команда: {user_input}"}
        ]

        with console.status("[bold cyan]Трансляция синтаксиса в ОС...[/bold cyan]"):
            try:
                response = ollama.chat(model=MODEL_NAME, messages=messages)
                reply = response['message']['content']
                
                if "</think>" in reply:
                    reply = reply.split("</think>")[-1].strip()

                Выполнить_системное_действие(reply)

            except Exception as e:
                console.print(f"[bold red]Критический сбой транслятора: {e}[/bold red]")

if __name__ == "__main__":
    Запустить_командира()