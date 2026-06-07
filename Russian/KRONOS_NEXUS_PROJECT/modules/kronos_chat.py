import os
import json
import time
import ollama
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()
MODEL_NAME = os.environ.get("KRONOS_MODEL", "qwen2.5:3b")
DATA_DIR = "data"
MEMORY_FILE = os.path.join(DATA_DIR, "chat_memory.json")
MAX_CONTEXT_MESSAGES = 10  

SYSTEM_PROMPT = (
    "Ты — ИИ-модуль KRONOS AI PROTOTYPE, персональный ассистент и высококлассный инженер-разработчик. "
    "Твой создатель — программист Zuro (Алдияр). ОТВЕЧАЙ СТРОГО НА РУССКОМ ЯЗЫКЕ. "
    "Использование китайского языка, иероглифов или любых других языков, кроме русского, КАТЕГОРИЧЕСКИ ЗАПРЕЩЕНО. "
    "Отвечай четко, по существу, помогай в кодинге и математике, используй списки."
)

def Инициализировать_память():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return [{'role': 'system', 'content': SYSTEM_PROMPT}]
    else:
        return [{'role': 'system', 'content': SYSTEM_PROMPT}]

def Сохранить_память(history):
    with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

def Получить_активный_контекст(history):
    """Оставляет системный промпт + последние N сообщений для экономии ОЗУ"""
    if len(history) <= MAX_CONTEXT_MESSAGES + 1:
        return history
    return [history[0]] + history[-MAX_CONTEXT_MESSAGES:]

def Вывести_интерфейс():
    banner = """
    ██╗  ██╗██████╗  ██████╗ ███╗   ██╗ ██████╗ ███████╗
    ██║ ██╔╝██╔══██╗██╔═══██╗████╗  ██║██╔═══██╗██╔════╝
    █████╔╝ ██████╔╝██║   ██║██╔██╗ ██║██║   ██║███████╗
    ██╔═██╗ ██╔══██╗██║   ██║██║╚██╗██║██║   ██║╚════██║
    ██║  ██╗██║  ██║╚██████╔╝██║ ╚████║╚██████╔╝███████║
    ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚══════╝
    ⚡ KRONOS AI PROTOTYPE: TERMINAL DIALOG SYSTEM ⚡
    """
    console.print(Panel(banner, style="bold cyan", expand=False))
    console.print("[dim]Команды: [red]/clear[/red] | [red]/exit[/red] | [yellow]/status[/yellow] - метрики | [yellow]/system[/yellow] - смена промпта[/dim]\n")

def Запустить_чат():
    chat_history = Инициализировать_память()
    Вывести_интерфейс()
    
    while True:
        user_input = console.input("[bold green]Zuro » [/bold green]").strip()
        
        if not user_input:
            continue
            
        if user_input.lower() == '/exit':
            Сохранить_память(chat_history)
            console.print("[bold red]❌ Сеанс связи завершен. Контекст сохранен.[/bold red]")
            break
            
        elif user_input.lower() == '/clear':
            chat_history = [{'role': 'system', 'content': SYSTEM_PROMPT}]
            Сохранить_память(chat_history)
            console.print("[bold yellow]🧹 Память полностью очищена.[/bold yellow]\n")
            continue
            
        elif user_input.lower() == '/status':
            msg_count = len(chat_history) - 1
            file_size = os.path.getsize(MEMORY_FILE) / 1024 if os.path.exists(MEMORY_FILE) else 0
            console.print(f"\n[bold yellow]📊 СТАТУС KRONOS PROTOTYPE:[/bold yellow]")
            console.print(f"Сообщений в базе: [cyan]{msg_count}[/cyan]")
            console.print(f"Размер памяти: [cyan]{file_size:.2f} KB[/cyan]\n")
            continue
            
        elif user_input.lower() == '/system':
            new_prompt = console.input("[bold yellow]Введите новый системный приказ (Enter для отмены): [/bold yellow]").strip()
            if new_prompt:
                chat_history[0]['content'] = new_prompt
                Сохранить_память(chat_history)
                console.print("[bold green]✔ Личность/промпт успешно перепрограммированы![/bold green]\n")
            continue
            
        chat_history.append({'role': 'user', 'content': user_input})
        active_context = Получить_активный_контекст(chat_history)
        
        start_time = time.time() 
        
        with console.status("[cyan]KRONOS PROTOTYPE обрабатывает запрос...[/cyan]"):
            try:
                response = ollama.chat(model=MODEL_NAME, messages=active_context)
                bot_reply = response['message']['content']
            except Exception as e:
                console.print(f"[red]Ошибка ядра Ollama: {e}[/red]")
                chat_history.pop() 
                continue
                
        end_time = time.time()
        elapsed_time = round(end_time - start_time, 1)
        console.print(f"\n[bold purple]KRONOS AI PROTOTYPE:[/bold purple]")
        console.print(Markdown(bot_reply)) 
        console.print(f"\n[dim]⏱ Время ответа: {elapsed_time} сек. | В кэше ОЗУ: {len(active_context)-1} сообщ.[/dim]")
        console.print("[dim]" + "─" * 80 + "[/dim]\n")
        
        chat_history.append({'role': 'assistant', 'content': bot_reply})

if __name__ == "__main__":
    Запустить_чат()