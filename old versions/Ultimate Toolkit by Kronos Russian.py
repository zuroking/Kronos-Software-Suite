import math
import random
import string
import datetime

def calculator():
    print("\n=== КАЛЬКУЛЯТОР by Kronos Russian ===")
    a = float(input("Первое число: "))
    b = float(input("Второе число: "))
    print("Сложение:", a + b)
    print("Вычитание:", a - b)
    print("Умножение:", a * b)
    if b != 0:
        print("Деление:", a / b)
        print("Остаток:", a % b)
    else:
        print("На ноль делить нельзя!")
    print("Степень a^b:", a ** b)
    if a >= 0:
        print("Корень из a:", math.sqrt(a))

def guess_number():
    print("\n=== УГАДАЙ ЧИСЛО by Kronos Russian ===")
    number = random.randint(1, 100)
    attempts = 0
    while True:
        try:
            guess = int(input("Введите число от 1 до 100: "))
            attempts += 1
            if guess < number:
                print("Слишком маленькое!")
            elif guess > number:
                print("Слишком большое!")
            else:
                print(f"Угадал за {attempts} попыток!")
                break
        except ValueError:
            print("Введи целое число!")

def temperature_converter():
    print("\n=== КОНВЕРТЕР ТЕМПЕРАТУР by Kronos Russian ===")
    print("1. Цельсий → Фаренгейт и Кельвин")
    print("2. Фаренгейт → Цельсий и Кельвин")
    print("3. Кельвин → Цельсий и Фаренгейт")
    choice = input("Выбор: ")
    temp = float(input("Введите температуру: "))
    if choice == "1":
        print(f"Фаренгейт: {temp * 9/5 + 32:.2f}")
        print(f"Кельвин: {temp + 273.15:.2f}")
    elif choice == "2":
        print(f"Цельсий: {(temp - 32) * 5/9:.2f}")
        print(f"Кельвин: {(temp - 32) * 5/9 + 273.15:.2f}")
    elif choice == "3":
        print(f"Цельсий: {temp - 273.15:.2f}")
        print(f"Фаренгейт: {(temp - 273.15) * 9/5 + 32:.2f}")

def currency_converter():
    print("\n=== КОНВЕРТЕР ВАЛЮТ by Kronos Russian ===")
    print("Курсы приблизительные — обновляй вручную")
    rates = {"KZT": 1, "USD": 481, "EUR": 556, "CNY": 70, "RUB": 6.7}
    print("Валюты: KZT, USD, EUR, CNY, RUB")
    from_cur = input("Из какой валюты: ").upper()
    to_cur = input("В какую валюту: ").upper()
    amount = float(input("Сумма: "))
    if from_cur in rates and to_cur in rates:
        result = amount * rates[from_cur] / rates[to_cur]
        print(f"{amount} {from_cur} = {result:.2f} {to_cur}")
    else:
        print("Неизвестная валюта!")

def area_calculator():
    print("\n=== КАЛЬКУЛЯТОР ПЛОЩАДИ by Kronos Russian ===")
    print("1. Круг")
    print("2. Квадрат")
    print("3. Прямоугольник")
    print("4. Треугольник")
    choice = input("Выбор: ")
    if choice == "1":
        r = float(input("Радиус: "))
        print(f"Площадь круга: {math.pi * r ** 2:.2f}")
    elif choice == "2":
        a = float(input("Сторона: "))
        print(f"Площадь квадрата: {a ** 2:.2f}")
    elif choice == "3":
        a = float(input("Длина: "))
        b = float(input("Ширина: "))
        print(f"Площадь прямоугольника: {a * b:.2f}")
    elif choice == "4":
        a = float(input("Основание: "))
        h = float(input("Высота: "))
        print(f"Площадь треугольника: {0.5 * a * h:.2f}")

def prime_numbers():
    print("\n=== ПРОСТЫЕ ЧИСЛА ===")
    n = int(input("Найти все простые числа до: "))
    primes = []
    for num in range(2, n + 1):
        is_prime = True
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
    print(f"Простые числа до {n}:", primes)
    print(f"Всего: {len(primes)}")

def notepad():
    print("\n=== БЛОКНОТ ===")
    filename = input("Имя файла (без расширения): ") + ".txt"
    print("Введи текст (пустая строка = сохранить и выйти):")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Сохранено в {filename}!")

def password_generator():
    print("\n=== ГЕНЕРАТОР ПАРОЛЕЙ by Kronos Russian ===")
    length = int(input("Длина пароля: "))
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    password = "".join(random.choice(chars) for _ in range(length))
    print(f"Твой пароль: {password}")

def word_counter():
    print("\n=== СЧЁТЧИК СЛОВ ===")
    text = input("Введи текст: ")
    words = len(text.split())
    letters = len([c for c in text if c.isalpha()])
    spaces = text.count(" ")
    print(f"Слов: {words}")
    print(f"Букв: {letters}")
    print(f"Пробелов: {spaces}")
    print(f"Символов всего: {len(text)}")

def text_reverser():
    print("\n=== ПЕРЕВОРОТ ТЕКСТА by Kronos Russian ===")
    text = input("Введи текст: ")
    print("Перевёрнутый:", text[::-1])
    print("Слова задом наперёд:", " ".join(text.split()[::-1]))

def rock_paper_scissors():
    print("\n=== КАМЕНЬ-НОЖНИЦЫ-БУМАГА ===")
    choices = ["камень", "ножницы", "бумага"]
    score_player = 0
    score_computer = 0
    while True:
        player = input("Твой выбор (камень/ножницы/бумага) или 'стоп': ").lower()
        if player == "стоп":
            break
        if player not in choices:
            print("Неверный выбор!")
            continue
        computer = random.choice(choices)
        print(f"Компьютер выбрал: {computer}")
        if player == computer:
            print("Ничья!")
        elif (player == "камень" and computer == "ножницы") or \
             (player == "ножницы" and computer == "бумага") or \
             (player == "бумага" and computer == "камень"):
            print("Ты победил!")
            score_player += 1
        else:
            print("Компьютер победил!")
            score_computer += 1
    print(f"Итог — Ты: {score_player} | Компьютер: {score_computer}")

def quiz():
    print("\n=== ВИКТОРИНА by Kronos Russian ===")
    questions = [
        ("Сколько планет в Солнечной системе?", ["6", "7", "8", "9"], "8"),
        ("Как называется столица Казахстана?", ["Алматы", "Астана", "Шымкент", "Актобе"], "Астана"),
        ("Сколько будет 2^10?", ["512", "1024", "2048", "256"], "1024"),
        ("Кто создал теорию относительности?", ["Ньютон", "Эйнштейн", "Бор", "Планк"], "Эйнштейн"),
        ("Что означает AI?", ["Auto Intelligence", "Artificial Intelligence", "Advanced Interface", "Auto Interface"], "Artificial Intelligence"),
    ]
    score = 0
    for q, options, answer in questions:
        print(f"\n{q}")
        for i, opt in enumerate(options, 1):
            print(f"  {i}. {opt}")
        user = input("Твой ответ: ")
        if user == answer or (user.isdigit() and options[int(user)-1] == answer):
            print("Правильно! ✓")
            score += 1
        else:
            print(f"Неверно. Правильный ответ: {answer}")
    print(f"\nРезультат: {score}/{len(questions)}")

def card_guess():
    print("\n=== УГАДАЙ КАРТУ by Kronos Russian ===")
    suits = ["♠ Пики", "♥ Червы", "♦ Бубны", "♣ Трефы"]
    values = ["2","3","4","5","6","7","8","9","10","Валет","Дама","Король","Туз"]
    card = f"{random.choice(values)} {random.choice(suits)}"
    attempts = 3
    print(f"Я загадал карту. У тебя {attempts} попытки!")
    for i in range(attempts):
        guess = input(f"Попытка {i+1} — введи карту (например: Туз ♠ Пики): ")
        if guess.lower() == card.lower():
            print("Угадал! 🎉")
            return
        else:
            print(f"Нет! Осталось попыток: {attempts - i - 1}")
    print(f"Не угадал. Карта была: {card}")

def dice_roller():
    print("\n=== БРОСОК КУБИКА by Kronos Russian ===")
    sides = int(input("Кубик с количеством граней (например 6, 12, 20): "))
    count = int(input("Сколько раз бросить: "))
    results = [random.randint(1, sides) for _ in range(count)]
    print(f"Результаты: {results}")
    print(f"Сумма: {sum(results)}")
    print(f"Среднее: {sum(results)/len(results):.2f}")

def countdown_timer():
    import time
    print("\n=== ТАЙМЕР by Kronos Russian ===")
    seconds = int(input("Введи количество секунд: "))
    print("Таймер запущен!")
    for i in range(seconds, 0, -1):
        print(f"\r⏱ Осталось: {i} сек   ", end="")
        time.sleep(1)
    print("\n🔔 Время вышло!")

def day_of_week():
    print("\n=== ДЕНЬ НЕДЕЛИ by Kronos Russian ===")
    date_str = input("Введи дату (ДД.ММ.ГГГГ): ")
    try:
        date = datetime.datetime.strptime(date_str, "%d.%m.%Y")
        days = ["Понедельник","Вторник","Среда","Четверг","Пятница","Суббота","Воскресенье"]
        print(f"{date_str} — это {days[date.weekday()]}")
    except ValueError:
        print("Неверный формат даты!")

def number_converter():
    print("\n=== КОНВЕРТЕР СИСТЕМ СЧИСЛЕНИЯ by Kronos Russian ===")
    print("1. Десятичное → Двоичное, Восьмеричное, Шестнадцатеричное")
    print("2. Двоичное → Десятичное")
    print("3. Шестнадцатеричное → Десятичное")
    choice = input("Выбор: ")
    if choice == "1":
        n = int(input("Введи число: "))
        print(f"Двоичное: {bin(n)[2:]}")
        print(f"Восьмеричное: {oct(n)[2:]}")
        print(f"Шестнадцатеричное: {hex(n)[2:].upper()}")
    elif choice == "2":
        b = input("Двоичное число: ")
        print(f"Десятичное: {int(b, 2)}")
    elif choice == "3":
        h = input("Шестнадцатеричное число: ")
        print(f"Десятичное: {int(h, 16)}")

def statistics():
    print("\n=== СТАТИСТИКА ЧИСЕЛ by Kronos Russian ===")
    nums = list(map(float, input("Введи числа через пробел: ").split()))
    print(f"Сумма: {sum(nums)}")
    print(f"Среднее: {sum(nums)/len(nums):.2f}")
    print(f"Минимум: {min(nums)}")
    print(f"Максимум: {max(nums)}")
    nums_sorted = sorted(nums)
    mid = len(nums_sorted) // 2
    median = nums_sorted[mid] if len(nums_sorted) % 2 != 0 else (nums_sorted[mid-1] + nums_sorted[mid]) / 2
    print(f"Медиана: {median}")

def chatbot():
    print("\n=== KRONOS МИНИ ЧАТ-БОТ by Kronos Russian ===")
    print("Привет! Я Kronos. Напиши 'пока' чтобы выйти.")
    responses = {
        "привет": "Привет! Как дела?",
        "как дела": "Отлично, спасибо! Готов помочь.",
        "кто ты": "Я Kronos — AI созданный ZuroCode. Однажды стану лучше GPT!",
        "что умеешь": "Пока немного, но скоро буду уметь всё!",
        "помощь": "Я могу отвечать на простые вопросы. Спрашивай!",
        "пока": "До свидания! 👋",
    }
    while True:
        user = input("Ты: ").lower()
        if user == "пока":
            print("Kronos: До свидания! 👋")
            break
        response = responses.get(user, "Интересный вопрос! Я ещё учусь. Спроси что-нибудь другое.")
        print(f"Kronos: {response}")

def fact_of_day():
    print("\n=== ФАКТ ДНЯ by Kronos Russian ===")
    facts = [
        "Осьминоги имеют три сердца и голубую кровь.",
        "Мёд никогда не портится — в гробницах фараонов находили съедобный мёд.",
        "Молния ударяет в землю около 100 раз в секунду.",
        "Человеческий мозг потребляет около 20% всей энергии тела.",
        "В Python первая версия вышла в 1991 году.",
        "Трансформеры — архитектура нейросетей — были изобретены в 2017 году.",
        "ChatGPT набрал 1 миллион пользователей за 5 дней.",
        "В мире более 700 языков программирования.",
        "Первым компьютерным вирусом считается Creeper (1971).",
        "Нанкин был столицей Китая несколько раз в истории.",
    ]
    print(f"💡 {random.choice(facts)}")

def main():
    tools = {
        "1":  ("Калькулятор by Kronos Russian", calculator),
        "2":  ("Угадай число by Kronos Russian", guess_number),
        "3":  ("Конвертер температур by Kronos Russian", temperature_converter),
        "4":  ("Конвертер валют by Kronos Russian", currency_converter),
        "5":  ("Калькулятор площади by Kronos Russian", area_calculator),
        "6":  ("Простые числа by Kronos Russian", prime_numbers),
        "7":  ("Блокнот by Kronos Russian", notepad),
        "8":  ("Генератор паролей by Kronos Russian", password_generator),
        "9":  ("Счётчик слов by Kronos Russian", word_counter),
        "10": ("Переворот текста by Kronos Russian", text_reverser),
        "11": ("Камень-ножницы-бумага by Kronos Russian", rock_paper_scissors),
        "12": ("Викторина by Kronos Russian", quiz),
        "13": ("Угадай карту by Kronos Russian", card_guess),
        "14": ("Бросок кубика by Kronos Russian", dice_roller),
        "15": ("Таймер by Kronos Russian", countdown_timer),
        "16": ("День недели by Kronos Russian", day_of_week),
        "17": ("Конвертер систем счисления by Kronos Russian", number_converter),
        "18": ("Статистика чисел by Kronos Russian", statistics),
        "19": ("Kronos мини чат-бот by Kronos Russian", chatbot),
        "20": ("Факт дня by Kronos Russian", fact_of_day),
    }

    while True:
        print("\n" + "=" * 40)
        print("     KRONOS TOOLKIT v1.0 by Kronos Russian")
        print("     Дата: 28.05.2026")
        print("     Будет обновлён в будущем с новыми инструментами!")
        print("=" * 40)
        for key, (name, _) in tools.items():
            print(f"  {key:>2}. {name}")
        print("   0. Выход")
        print("=" * 40)

        choice = input("Выбери инструмент: ")

        if choice == "0":
            print("\nДо свидания! — Kronos Toolkit by Kronos Russian")
            input("Нажми Enter для закрытия...")
            break
        elif choice in tools:
            tools[choice][1]()
            input("\n↩ Нажми Enter чтобы вернуться в меню...")
        else:
            print("Неверный выбор!")

main()