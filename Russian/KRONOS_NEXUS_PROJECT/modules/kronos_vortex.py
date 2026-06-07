# DATA VORTEX PARSER & SYNTHESIZER
import os
import sys
import ollama
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()
MODEL_NAME = os.environ.get("KRONOS_MODEL", "qwen2.5:3b")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "data"))
INPUT_FILE = os.path.join(DATA_DIR, "vortex_input.txt")
OUTPUT_DIR = os.path.join(DATA_DIR, "generated_reports")

VORTEX_PROMPT = (
    "Ты — аналитический модуль VORTEX PARSER. Вытащи из текста все важные "
    "исторические даты, года, технические термины и имена. "
    "ОТВЕЧАЙ СТРОГО НА РУССКОМ ЯЗЫКЕ. Пиши коротко, тезисно, без лишних вступлений."
)

SYNTHESIS_PROMPT = (
    "Ты — ГРАНД-СБОРЩИК экосистемы KRONOS. Перед тобой результаты анализа разных секторов одного документа. "
    "Твоя задача — объединить эти данные в один ультимативный отчет. "
    "ТРЕБОВАНИЯ:\n"
    "1) ОТВЕЧАЙ СТРОГО НА РУССКОМ ЯЗЫКЕ.\n"
    "2) Удали все повторяющиеся факты и имена.\n"
    "3) Создай единый хронологический таймлайн: отсортируй ВСЕ найденные даты и события по порядку (от самых ранних к 2026 году).\n"
    "4) Оформи отчет красиво через заголовки Markdown."
)

def Проверить_инфраструктуру_модуля():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def Нарезать_текст(text, chunk_size=3000, overlap=400):
    """Надежная нарезка с перекрытием, защищенная от бесконечных циклов"""
    chunks = []
    if not text:
        return chunks
        
    if len(text) <= chunk_size:
        return [text]
        
    start = 0
    step = chunk_size - overlap
    if step <= 0:
        step = chunk_size // 2

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += step
    return chunks

def Запустить_парсер():
    Проверить_инфраструктуру_модуля()
    
    console.clear()
    console.print(Panel("🌪️ KRONOS DATA VORTEX PARSER & SYNTHESIZER v2.1", style="bold blue", expand=False))
    
    if not os.path.exists(INPUT_FILE) or os.path.getsize(INPUT_FILE) == 0:
        console.print(f"[bold red]❌ Входной файл {INPUT_FILE} пуст или не найден![/bold red]")
        input("\nНажмите Enter для возврата в Хаб...")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        full_text = f.read()

    console.print(f"[green]✔ Файл успешно считан ({len(full_text)} символов).[/green]")
    
    sectors = Нарезать_текст(full_text)
    
    raw_reports_combined = ""
    
    console.print("[cyan]ФАЗА 1: Запуск первичного сбора фактов по секторам...[/cyan]\n")
    console.print(f"[dim]Всего выделено секторов для анализа: {len(sectors)}[/dim]\n")
    
    for index, sector in enumerate(sectors):
        with console.status(f"[bold blue]Анализ сектора {index + 1}/{len(sectors)}...[/bold blue]"):
            try:
                response = ollama.chat(model=MODEL_NAME, messages=[
                    {"role": "system", "content": VORTEX_PROMPT},
                    {"role": "user", "content": sector}
                ])
                reply = response['message']['content']
                if "</think>" in reply: 
                    reply = reply.split("</think>")[-1].strip()
                
                raw_reports_combined += f"\n--- Данные сектора {index + 1} ---\n{reply}\n"
                console.print(f"[dim]✔ Сектор {index + 1} успешно обработан.[/dim]")
            except Exception as e:
                console.print(f"[red]Ошибка сектора {index + 1}: {e}[/red]")

    if not raw_reports_combined.strip():
        console.print("[bold red]❌ Факты из секторов не были собраны. Синтез невозможен.[/bold red]")
        input("\nНажмите Enter для возврата в Хаб...")
        return

    console.print("\n[bold magenta]⚡ ФАЗА 2: Запуск Гранд-Сборщика KRONOS. Сжатие и сортировка...[/bold magenta]")
    
    with console.status("[bold magenta]ИИ выстраивает единый хронологический таймлайн...[/bold magenta]"):
        try:
            final_response = ollama.chat(model=MODEL_NAME, messages=[
                {"role": "system", "content": SYNTHESIS_PROMPT},
                {"role": "user", "content": f"Вот собранные сырые данные по секторам. Сделай из них чистый хронологический отчет:\n\n{raw_reports_combined}"}
            ])
            grand_report = final_response['message']['content']
            if "</think>" in grand_report: 
                grand_report = grand_report.split("</think>")[-1].strip()
        except Exception as e:
            console.print(f"[bold red]Критический сбой фазы синтеза: {e}[/bold red]")
            grand_report = "# Ошибка синтеза данных\n" + raw_reports_combined

    output_file_path = os.path.join(OUTPUT_DIR, "grand_report.md")
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(f"# УЛЬТИМАТИВНЫЙ ГРАНД-ОТЧЕТ KRONOS NEXUS\n")
        f.write(f"**Вычислительное ядро:** {MODEL_NAME}\n")
        f.write(f"────────────────────────────────────────────────────────────────\n\n")
        f.write(grand_report)

    console.print(f"\n[bold green]📊 МОНОЛИТНЫЙ ХРОНОЛОГИЧЕСКИЙ ОТЧЕТ СФОРМИРОВАН![/bold green]")
    console.print(f"Путь: [cyan]data/generated_reports/grand_report.md[/cyan]\n")
    
    console.print(Panel("[bold white]👁 ПРЕДВЫБОРНЫЙ ПРОСМОТР ЕДИНОГО ТАЙМЛАЙНА:[/bold white]", style="dim"))
    console.print(Markdown(grand_report[:1500] + "\n\n*...[Полный упорядоченный отчет сохранен на диск]...*"))
    
    input("\nНажмите Enter для возврата в Главный Хаб...")

if __name__ == "__main__":
    Запустить_парсер()