import os
import sys
import ollama
import time
import re
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()
MODEL_NAME = os.environ.get("KRONOS_MODEL", "qwen2.5:3b")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "data"))
OUTPUT_DIR = os.path.join(DATA_DIR, "generated_reports")

PLANNER_PROMPT = (
    "Ты — ИИ-Планировщик экосистемы KRONOS. Твоя задача — составить подробный план "
    "для глубокой статьи на тему пользователя. Выдай СТРОГО нумерованный список из 3-4 глав. "
    "Не пиши никаких вступлений. ОТВЕЧАЙ СТРОГО НА РУССКОМ ЯЗЫКЕ. Пример вывода:\n"
    "1. Введение в технологию\n2. Исторические вехи\n3. Современные вызовы"
)

WRITER_PROMPT = (
    "Ты — ИИ-Писатель KRONOS. Напиши глубокий, детальный и академически точный текст "
    "для конкретной главы статьи. Используй факты, термины и Markdown-разметку. "
    "ОТВЕЧАЙ СТРОГО НА РУССКОМ ЯЗЫКЕ. Не лей воду, выдавай сразу текст главы."
)

CRITIC_PROMPT = (
    "Ты — ИИ-Критик и Главный Редактор KRONOS. Перед тобой готовая статья. "
    "Твоя задача — провести рефакторинг текста. "
    "1) ОТВЕЧАЙ СТРОГО НА РУССКОМ ЯЗЫКЕ.\n"
    "2) Вырежи очевидные галлюцинации, бред, выдуманные исторические факты или нарушенную логику.\n"
    "3) Сделай текст монолитным, красивым и профессиональным. Сохрани структуру Markdown."
)

def Проверить_директорию():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def Очистить_имя_файла(filename):
    keepcharacters = (' ', '.', '_', '-')
    return "".join(c for c in filename if c.isalnum() or c in keepcharacters).rstrip()

def Фильтровать_мысли(text):
    """Удаляет теги рассуждений DeepSeek, если они есть"""
    if "</think>" in text:
        return text.split("</think>")[-1].strip()
    return text.strip()

def Запустить_генератор():
    Проверить_директорию()
    
    console.clear()
    banner = """
 📝 KRONOS MULTI-STEP DATA GENERATOR
    """
    console.print(Panel(banner.strip(), style="bold magenta", expand=False))
    console.print("[dim]Режим: Конвейерная многошаговая генерация лонгридов с ИИ-цензурой.[/dim]\n")

    topic = Prompt.ask("[bold yellow]Введите одну глобальную тему для статьи (или /exit)[/bold yellow]").strip()
    
    if topic.lower() == '/exit' or not topic:
        return

    console.print(f"\n[bold cyan]🚀 Запуск многошагового процесса для темы: '{topic}'[/bold cyan]\n")

    with console.status("[bold yellow]Фаза 1: Разработка архитектуры и плана статьи...[/bold yellow]"):
        try:
            response = ollama.chat(model=MODEL_NAME, messages=[
                {"role": "system", "content": PLANNER_PROMPT},
                {"role": "user", "content": f"Создай план для статьи: {topic}"}
            ])
            raw_plan = Фильтровать_мысли(response['message']['content'])
            chapters = [line.strip() for line in raw_plan.split('\n') if line.strip() and re.match(r'^\d+', line.strip())]
        except Exception as e:
            console.print(f"[red]Ошибка на фазе планирования: {e}[/red]")
            return

    if not chapters:
        console.print("[bold red]❌ ИИ не смог построить четкий план. Попробуйте еще раз.[/bold red]")
        input("\nНажмите Enter...")
        return

    console.print("[green]✔ Архитектура статьи успешно построена. План утвержден:[/green]")
    for ch in chapters:
        console.print(f"  [dim]— {ch}[/dim]")
    console.print("")

    full_article_draft = f"# {topic.upper()}\n\n"
    
    for i, chapter in enumerate(chapters, 1):
        with console.status(f"[bold code]Фаза 2: Пишем главу {i}/{len(chapters)} ({chapter})...[/bold code]"):
            try:
                response = ollama.chat(model=MODEL_NAME, messages=[
                    {"role": "system", "content": WRITER_PROMPT},
                    {"role": "user", "content": f"Тема статьи: {topic}. Напиши подробное содержание для главы: {chapter}"}
                ])
                chapter_content = Фильтровать_мысли(response['message']['content'])
                full_article_draft += f"## {chapter}\n\n{chapter_content}\n\n"
                console.print(f"[green]✔ Глава {i} успешно сгенерирована.[/green]")
            except Exception as e:
                console.print(f"[red]Ошибка при написании главы {i}: {e}[/red]")

    console.print("\n[bold orange3]⚡ Фаза 3: Передача черновика ИИ-Критику на проверку галлюцинаций...[/bold orange3]")
    
    with console.status("[bold orange3]Критик KRONOS чистит текст и проверяет факты...[/bold orange3]"):
        try:
            final_response = ollama.chat(model=MODEL_NAME, messages=[
                {"role": "system", "content": CRITIC_PROMPT},
                {"role": "user", "content": f"Отредактируй этот черновик статьи:\n\n{full_article_draft}"}
            ])
            polished_article = Фильтровать_мысли(final_response['message']['content'])
        except Exception as e:
            console.print(f"[bold red]Сбой фазы критики: {e}. Сохраняем черновой вариант.[/bold red]")
            polished_article = full_article_draft

    safe_filename = Очистить_имя_файла(topic)
    file_path = os.path.join(OUTPUT_DIR, f"{safe_filename}.md")
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(polished_article)

    console.print(f"\n[bold green]✅ МОДЕРНИЗИРОВАННАЯ СТАТЬЯ УСПЕШНО СОХРАНЕНА![/bold green]")
    console.print(f"Путь к файлу: [cyan]data/generated_reports/{safe_filename}.md[/cyan]\n")
    
    input("\nНажмите Enter для возврата в Главный Хаб...")

if __name__ == "__main__":
    Запустить_генератор()