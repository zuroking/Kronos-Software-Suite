import os
import sys
import re
import io
import ollama
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()
MODEL_NAME = os.environ.get("KRONOS_MODEL", "qwen2.5:3b")

SOLVER_PROMPT = (
    "Ты — KRONOS SMART SOLVER, элитный вычислительный модуль. "
    "Твоя цель: пошаговое решение задач (алгебра, геометрия, химия) и отладка кода. "
    "ОТВЕЧАЙ СТРОГО НА РУССКОМ ЯЗЫКЕ. "
    "КРИТИЧЕСКОЕ ТРЕБОВАНИЕ: Если задача требует математических расчетов, ты обязан "
    "включить в свой ответ рабочий блок кода на Python, заключенный в тройные обратные кавычки ```python ... ```, "
    "который при запуске через print() выведет финальный точный ответ. "
    "Структурируй ответ: Дано, Пошаговое решение, Блок автоматического расчета."
)

def Выполнить_локальный_код(code_string):
    old_stdout = sys.stdout
    redirected_output = io.StringIO()
    sys.stdout = redirected_output
    
    local_vars = {}
    error = None
    
    try:
        exec(code_string, {"__builtins__": __builtins__, "import": __import__}, local_vars)
    except Exception as e:
        error = str(e)
    finally:
        sys.stdout = old_stdout
        
    if error:
        return f"Ошибка интерпретатора: {error}"
    return redirected_output.getvalue().strip()

def Запустить_решатель():
    console.clear()
    banner = """
  📐 KRONOS SMART SOLVER & CODE EXECUTOR 
    """
    console.print(Panel(banner.strip(), style="bold green", expand=False))
    console.print("[dim]Режим: Инженерный расчёт и авто-верификация кода. Команда [red]/exit[/red] — в Хаб.[/dim]\n")

    chat_history = [{"role": "system", "content": SOLVER_PROMPT}]

    while True:
        user_input = console.input("[bold yellow]Ввод инженерной задачи » [/bold yellow]").strip()

        if user_input.lower() == '/exit':
            break
        if not user_input:
            continue

        chat_history.append({"role": "user", "content": user_input})

        with console.status("[bold green]Масштабирование векторов вычисления...[/bold green]"):
            try:
                response = ollama.chat(model=MODEL_NAME, messages=chat_history)
                reply = response['message']['content']

                if "</think>" in reply:
                    reply = reply.split("</think>")[-1].strip()

                console.print("\n[bold cyan]🧠 СТРАТЕГИЯ И РЕШЕНИЕ ИИ:[/bold cyan]")
                console.print(Markdown(reply))

                code_blocks = re.findall(r'```python\s+(.*?)\s+```', reply, re.DOTALL)
                
                if code_blocks:
                    target_code = code_blocks[0]
                    console.print("\n[bold magenta]⚙️ ЗАПУСК ЛОКАЛЬНОЙ ВЕРИФИКАЦИИ (i7 CPU EXECUTOR)...[/bold magenta]")
                    
                    calculated_result = Выполнить_локальный_код(target_code)
                    
                    if calculated_result:
                        result_panel = Panel(
                            f"[bold green]Финальный точный результат:[/bold green]\n[bold white]{calculated_result}[/bold white]",
                            title="[bold light_coral]⚙️ ВЕРИФИЦИРОВАННЫЙ ОТВЕТ СИСТЕМЫ[/bold light_coral]",
                            border_style="magenta"
                        )
                        console.print(result_panel)
                    else:
                        console.print("[dim white]Код выполнен успешно, но не вернул значений через print().[/dim white]")

                chat_history.append({"role": "assistant", "content": reply})

                if len(chat_history) > 3:
                    chat_history = [chat_history[0], chat_history[-2], chat_history[-1]]

            except Exception as e:
                console.print(f"\n[bold red]Ошибка ядра: {e}[/bold red]")
                chat_history.pop()

if __name__ == "__main__":
    Запустить_решатель()