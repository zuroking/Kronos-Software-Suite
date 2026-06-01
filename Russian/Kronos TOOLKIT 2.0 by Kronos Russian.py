import datetime
import math
import random
import secrets
import string
import time


APP_NAME = "KRONOS TOOLKIT"
APP_VERSION = "2.0"
AUTHOR = "Kronos Russian"
DATE = "06.06.2026"


def pause():
    input("\nНажмите Enter, чтобы вернуться в меню...")


def read_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Введите правильное число.")


def read_int(prompt, minimum=None, maximum=None):
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Введите целое число.")
            continue

        if minimum is not None and value < minimum:
            print(f"Число должно быть не меньше {minimum}.")
            continue
        if maximum is not None and value > maximum:
            print(f"Число должно быть не больше {maximum}.")
            continue
        return value


def read_choice(prompt, choices):
    choices = {str(choice) for choice in choices}
    while True:
        value = input(prompt).strip()
        if value in choices:
            return value
        print("Неверный выбор. Попробуйте снова.")


def print_title(title):
    print(f"\n=== {title} от {AUTHOR} ===")


def calculator():
    print_title("УМНЫЙ КАЛЬКУЛЯТОР")
    print("1. Основные операции")
    print("2. Дополнительные операции")
    choice = read_choice("Выбор: ", ["1", "2"])

    if choice == "1":
        a = read_float("Первое число: ")
        b = read_float("Второе число: ")

        print(f"Сложение: {a + b}")
        print(f"Вычитание: {a - b}")
        print(f"Умножение: {a * b}")

        if b == 0:
            print("Деление: нельзя делить на ноль")
            print("Остаток: нельзя делить на ноль")
        else:
            print(f"Деление: {a / b}")
            print(f"Остаток: {a % b}")

        print(f"Степень a^b: {a ** b}")
    else:
        a = read_float("Число: ")

        if a >= 0:
            print(f"Квадратный корень: {math.sqrt(a)}")
        else:
            print("Квадратный корень недоступен для отрицательного числа")

        print(f"Модуль числа: {abs(a)}")
        print(f"Округление: {round(a)}")

        if a > 0:
            print(f"Натуральный логарифм: {math.log(a):.4f}")


def guess_number():
    print_title("УГАДАЙ ЧИСЛО")
    low = read_int("Минимальное число: ")
    high = read_int("Максимальное число: ", low + 1)
    number = random.randint(low, high)
    attempts = 0

    print(f"Я загадал число от {low} до {high}.")

    while True:
        guess = read_int("Ваш вариант: ", low, high)
        attempts += 1

        if guess < number:
            print("Слишком маленькое.")
        elif guess > number:
            print("Слишком большое.")
        else:
            print(f"Вы угадали за {attempts} попыток!")
            break


def temperature_converter():
    print_title("КОНВЕРТЕР ТЕМПЕРАТУРЫ")
    print("1. Цельсий в Фаренгейт и Кельвин")
    print("2. Фаренгейт в Цельсий и Кельвин")
    print("3. Кельвин в Цельсий и Фаренгейт")
    choice = read_choice("Выбор: ", ["1", "2", "3"])
    temp = read_float("Введите температуру: ")

    if choice == "1":
        print(f"Фаренгейт: {temp * 9 / 5 + 32:.2f}")
        print(f"Кельвин: {temp + 273.15:.2f}")
    elif choice == "2":
        celsius = (temp - 32) * 5 / 9
        print(f"Цельсий: {celsius:.2f}")
        print(f"Кельвин: {celsius + 273.15:.2f}")
    else:
        celsius = temp - 273.15
        print(f"Цельсий: {celsius:.2f}")
        print(f"Фаренгейт: {celsius * 9 / 5 + 32:.2f}")


def currency_converter():
    print_title("КОНВЕРТЕР ВАЛЮТ")
    print("Курсы примерные. При необходимости обновите вручную.")
    rates = {"KZT": 1, "USD": 481, "EUR": 556, "CNY": 70, "RUB": 6.7}

    print("Валюты:", ", ".join(rates))
    from_cur = input("Из валюты: ").upper().strip()
    to_cur = input("В валюту: ").upper().strip()
    amount = read_float("Сумма: ")

    if from_cur in rates and to_cur in rates:
        result = amount * rates[from_cur] / rates[to_cur]
        print(f"{amount:.2f} {from_cur} = {result:.2f} {to_cur}")
    else:
        print("Неизвестная валюта.")


def area_calculator():
    print_title("ПЛОЩАДЬ И ОБЪЕМ")
    print("1. Площадь круга")
    print("2. Площадь квадрата")
    print("3. Площадь прямоугольника")
    print("4. Площадь треугольника")
    print("5. Объем куба")
    print("6. Объем цилиндра")
    choice = read_choice("Выбор: ", ["1", "2", "3", "4", "5", "6"])

    if choice == "1":
        r = read_float("Радиус: ")
        print(f"Площадь круга: {math.pi * r ** 2:.2f}")
    elif choice == "2":
        a = read_float("Сторона: ")
        print(f"Площадь квадрата: {a ** 2:.2f}")
    elif choice == "3":
        a = read_float("Длина: ")
        b = read_float("Ширина: ")
        print(f"Площадь прямоугольника: {a * b:.2f}")
    elif choice == "4":
        a = read_float("Основание: ")
        h = read_float("Высота: ")
        print(f"Площадь треугольника: {0.5 * a * h:.2f}")
    elif choice == "5":
        a = read_float("Сторона: ")
        print(f"Объем куба: {a ** 3:.2f}")
    else:
        r = read_float("Радиус: ")
        h = read_float("Высота: ")
        print(f"Объем цилиндра: {math.pi * r ** 2 * h:.2f}")


def prime_numbers():
    print_title("ПРОСТЫЕ ЧИСЛА")
    n = read_int("Найти простые числа до: ", 2)
    primes = []

    for num in range(2, n + 1):
        is_prime = True
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)

    print(f"Простые числа до {n}: {primes}")
    print(f"Всего: {len(primes)}")


def notepad():
    print_title("БЛОКНОТ")
    filename = input("Имя файла без расширения: ").strip() or "kronos_note"
    filename = f"{filename}.txt"

    print("Введите текст. Пустая строка = сохранить и выйти.")
    lines = []

    while True:
        line = input()
        if line == "":
            break
        lines.append(line)

    with open(filename, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))

    print(f"Сохранено в файл {filename}.")


def password_generator():
    print_title("ГЕНЕРАТОР ПАРОЛЕЙ")
    length = read_int("Длина пароля: ", 4, 128)
    use_symbols = input("Использовать символы? (да/нет): ").lower().strip() == "да"

    chars = string.ascii_letters + string.digits
    if use_symbols:
        chars += "!@#$%^&*()-_=+[]{}"

    while True:
        password = "".join(secrets.choice(chars) for _ in range(length))
        print(f"Ваш пароль: {password}")

        again = input("Сгенерировать еще? (да/нет): ").lower().strip()
        if again != "да":
            break


def word_counter():
    print_title("СЧЕТЧИК СЛОВ")
    text = input("Введите текст: ")

    words = text.split()
    letters = sum(1 for char in text if char.isalpha())
    digits = sum(1 for char in text if char.isdigit())
    spaces = text.count(" ")

    print(f"Слова: {len(words)}")
    print(f"Буквы: {letters}")
    print(f"Цифры: {digits}")
    print(f"Пробелы: {spaces}")
    print(f"Всего символов: {len(text)}")


def text_tools():
    print_title("ИНСТРУМЕНТЫ ДЛЯ ТЕКСТА")
    text = input("Введите текст: ")

    print(f"Наоборот: {text[::-1]}")
    print(f"Слова наоборот: {' '.join(text.split()[::-1])}")
    print(f"ВЕРХНИЙ РЕГИСТР: {text.upper()}")
    print(f"нижний регистр: {text.lower()}")
    print(f"Каждое Слово С Большой Буквы: {text.title()}")


def rock_paper_scissors():
    print_title("КАМЕНЬ-НОЖНИЦЫ-БУМАГА")
    choices = ["камень", "ножницы", "бумага"]
    score_player = 0
    score_computer = 0

    while True:
        player = input("Ваш выбор (камень/ножницы/бумага) или стоп: ").lower().strip()

        if player == "стоп":
            break
        if player not in choices:
            print("Неверный выбор.")
            continue

        computer = random.choice(choices)
        print(f"Компьютер выбрал: {computer}")

        if player == computer:
            print("Ничья.")
        elif (
            player == "камень" and computer == "ножницы"
            or player == "ножницы" and computer == "бумага"
            or player == "бумага" and computer == "камень"
        ):
            print("Вы победили!")
            score_player += 1
        else:
            print("Компьютер победил!")
            score_computer += 1

    print(f"Финальный счет - Вы: {score_player} | Компьютер: {score_computer}")


def quiz():
    print_title("ВИКТОРИНА")
    questions = [
        ("Сколько планет в Солнечной системе?", ["6", "7", "8", "9"], "8"),
        ("Столица Казахстана?", ["Алматы", "Астана", "Шымкент", "Актобе"], "Астана"),
        ("Сколько будет 2^10?", ["512", "1024", "2048", "256"], "1024"),
        ("Кто создал теорию относительности?", ["Ньютон", "Эйнштейн", "Бор", "Планк"], "Эйнштейн"),
        ("Что означает AI?", ["Авто Интеллект", "Искусственный интеллект", "Интерфейс", "Авто Интерфейс"], "Искусственный интеллект"),
        ("На каком языке написан этот toolkit?", ["Java", "Python", "C++", "HTML"], "Python"),
        ("Самый большой океан?", ["Атлантический", "Индийский", "Тихий", "Северный Ледовитый"], "Тихий"),
    ]

    random.shuffle(questions)
    score = 0

    for question, options, answer in questions:
        print(f"\n{question}")
        for index, option in enumerate(options, 1):
            print(f"  {index}. {option}")

        user = input("Ваш ответ: ").strip()

        if user.isdigit() and 1 <= int(user) <= len(options):
            user_answer = options[int(user) - 1]
        else:
            user_answer = user

        if user_answer.lower() == answer.lower():
            print("Правильно!")
            score += 1
        else:
            print(f"Неверно. Правильный ответ: {answer}")

    print(f"\nРезультат: {score}/{len(questions)}")


def card_guess():
    print_title("УГАДАЙ КАРТУ")
    suits = ["пики", "червы", "бубны", "трефы"]
    values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "валет", "дама", "король", "туз"]

    card_value = random.choice(values)
    card_suit = random.choice(suits)
    attempts = 3

    print(f"Я выбрал карту. У вас {attempts} попытки.")
    print("Пример ответа: туз пики")

    for attempt in range(1, attempts + 1):
        guess = input(f"Попытка {attempt}: ").lower().strip()

        if guess == f"{card_value} {card_suit}":
            print("Вы угадали!")
            return

        print(f"Нет. Осталось попыток: {attempts - attempt}")

    print(f"Карта была: {card_value} {card_suit}")


def dice_roller():
    print_title("БРОСОК КУБИКА")
    sides = read_int("Количество сторон: ", 2)
    count = read_int("Сколько раз бросить: ", 1, 100)

    results = [random.randint(1, sides) for _ in range(count)]

    print(f"Результаты: {results}")
    print(f"Сумма: {sum(results)}")
    print(f"Среднее: {sum(results) / len(results):.2f}")


def countdown_timer():
    print_title("ТАЙМЕР")
    seconds = read_int("Введите количество секунд: ", 1)

    print("Таймер запущен.")
    for remaining in range(seconds, 0, -1):
        print(f"\rОсталось: {remaining} сек   ", end="")
        time.sleep(1)

    print("\nВремя вышло!")


def day_of_week():
    print_title("ДЕНЬ НЕДЕЛИ")
    date_str = input("Введите дату (ДД.ММ.ГГГГ): ").strip()

    try:
        date = datetime.datetime.strptime(date_str, "%d.%m.%Y")
    except ValueError:
        print("Неверный формат даты.")
        return

    days = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]
    print(f"{date_str} - это {days[date.weekday()]}")


def number_converter():
    print_title("КОНВЕРТЕР СИСТЕМ СЧИСЛЕНИЯ")
    print("1. Десятичное в двоичное, восьмеричное, шестнадцатеричное")
    print("2. Двоичное в десятичное")
    print("3. Восьмеричное в десятичное")
    print("4. Шестнадцатеричное в десятичное")
    choice = read_choice("Выбор: ", ["1", "2", "3", "4"])

    try:
        if choice == "1":
            number = read_int("Введите десятичное число: ")
            print(f"Двоичное: {bin(number)[2:]}")
            print(f"Восьмеричное: {oct(number)[2:]}")
            print(f"Шестнадцатеричное: {hex(number)[2:].upper()}")
        elif choice == "2":
            print(f"Десятичное: {int(input('Двоичное число: '), 2)}")
        elif choice == "3":
            print(f"Десятичное: {int(input('Восьмеричное число: '), 8)}")
        else:
            print(f"Десятичное: {int(input('Шестнадцатеричное число: '), 16)}")
    except ValueError:
        print("Неверное число для выбранной системы.")


def statistics_tool():
    print_title("СТАТИСТИКА ЧИСЕЛ")

    try:
        nums = [float(item) for item in input("Введите числа через пробел: ").split()]
    except ValueError:
        print("Введите только числа.")
        return

    if not nums:
        print("Числа не введены.")
        return

    nums_sorted = sorted(nums)
    mid = len(nums_sorted) // 2
    median = nums_sorted[mid] if len(nums_sorted) % 2 else (nums_sorted[mid - 1] + nums_sorted[mid]) / 2

    print(f"Сумма: {sum(nums)}")
    print(f"Среднее: {sum(nums) / len(nums):.2f}")
    print(f"Минимум: {min(nums)}")
    print(f"Максимум: {max(nums)}")
    print(f"Медиана: {median}")


def chatbot():
    print_title("МИНИ ЧАТ-БОТ KRONOS")
    print("Привет! Я Kronos. Напишите 'пока', чтобы выйти.")

    responses = {
        "привет": "Привет! Как дела?",
        "здравствуй": "Здравствуйте! Чем могу помочь?",
        "как дела": "Отлично! Готов помогать.",
        "кто ты": "Я Kronos, мини-помощник от Kronos.",
        "что ты умеешь": "Я могу запускать инструменты, играть, считать и помогать с простыми задачами.",
        "помощь": "Попробуйте спросить: привет, кто ты, что ты умеешь, время, дата, монета.",
        "время": lambda: f"Текущее время: {datetime.datetime.now().strftime('%H:%M:%S')}",
        "дата": lambda: f"Текущая дата: {datetime.datetime.now().strftime('%d.%m.%Y')}",
        "монета": lambda: f"Монета: {random.choice(['орел', 'решка'])}",
    }

    while True:
        user = input("Вы: ").lower().strip()

        if user == "пока":
            print("Kronos: До свидания!")
            break

        response = responses.get(user, "Интересный вопрос. Я еще учусь.")
        if callable(response):
            response = response()

        print(f"Kronos: {response}")


def fact_of_day():
    print_title("ФАКТ ДНЯ")
    facts = [
        "Первая версия Python вышла в 1991 году.",
        "Архитектура Transformer была представлена в 2017 году.",
        "Одним из первых компьютерных вирусов считается Creeper 1971 года.",
        "В високосном году 366 дней.",
        "Международная космическая станция движется со скоростью около 28000 км/ч.",
        "Первое электронное письмо было отправлено в 1971 году.",
        "Ноль является четным числом.",
        "Казахстан - самая большая страна в мире без выхода к океану.",
        "Тихий океан - самый большой океан на Земле.",
        "Двоичный код использует только две цифры: 0 и 1.",
    ]

    print(random.choice(facts))


def coin_flipper():
    print_title("МОНЕТКА")
    count = read_int("Сколько раз подбросить монету: ", 1, 1000)

    results = [random.choice(["Орел", "Решка"]) for _ in range(count)]

    print(f"Орел: {results.count('Орел')}")
    print(f"Решка: {results.count('Решка')}")

    if count <= 50:
        print(f"Результаты: {results}")


def bmi_calculator():
    print_title("КАЛЬКУЛЯТОР ИМТ")
    weight = read_float("Вес в кг: ")
    height_cm = read_float("Рост в см: ")

    if height_cm <= 0:
        print("Рост должен быть больше нуля.")
        return

    bmi = weight / ((height_cm / 100) ** 2)

    print(f"ИМТ: {bmi:.2f}")

    if bmi < 18.5:
        print("Категория: недостаточный вес")
    elif bmi < 25:
        print("Категория: нормальный вес")
    elif bmi < 30:
        print("Категория: лишний вес")
    else:
        print("Категория: ожирение")


def age_calculator():
    print_title("КАЛЬКУЛЯТОР ВОЗРАСТА")
    birth_str = input("Введите дату рождения (ДД.ММ.ГГГГ): ").strip()

    try:
        birth_date = datetime.datetime.strptime(birth_str, "%d.%m.%Y").date()
    except ValueError:
        print("Неверный формат даты.")
        return

    today = datetime.date.today()

    if birth_date > today:
        print("Дата рождения не может быть в будущем.")
        return

    years = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    days = (today - birth_date).days

    print(f"Возраст: {years} лет")
    print(f"Прожито дней: {days}")


def todo_list():
    print_title("СПИСОК ДЕЛ")
    tasks = []

    while True:
        print("\n1. Добавить задачу")
        print("2. Показать задачи")
        print("3. Удалить задачу")
        print("0. Выйти из списка дел")
        choice = read_choice("Выбор: ", ["1", "2", "3", "0"])

        if choice == "0":
            break

        if choice == "1":
            task = input("Новая задача: ").strip()
            if task:
                tasks.append(task)
                print("Задача добавлена.")

        elif choice == "2":
            if not tasks:
                print("Задач пока нет.")
            else:
                for index, task in enumerate(tasks, 1):
                    print(f"{index}. {task}")

        else:
            if not tasks:
                print("Нет задач для удаления.")
                continue

            index = read_int("Номер задачи для удаления: ", 1, len(tasks))
            removed = tasks.pop(index - 1)
            print(f"Удалено: {removed}")


def random_name_picker():
    print_title("СЛУЧАЙНЫЙ ВЫБОР ИМЕНИ")
    names = [name.strip() for name in input("Введите имена через запятую: ").split(",") if name.strip()]

    if not names:
        print("Имена не введены.")
        return

    print(f"Выбранное имя: {random.choice(names)}")


def morse_code_translator():
    print_title("ПЕРЕВОДЧИК В АЗБУКУ МОРЗЕ")

    morse = {
        "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.",
        "G": "--.", "H": "....", "I": "..", "J": ".---", "K": "-.-", "L": ".-..",
        "M": "--", "N": "-.", "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.",
        "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--", "X": "-..-",
        "Y": "-.--", "Z": "--..", "0": "-----", "1": ".----", "2": "..---",
        "3": "...--", "4": "....-", "5": ".....", "6": "-....", "7": "--...",
        "8": "---..", "9": "----.",
        "А": ".-", "Б": "-...", "В": ".--", "Г": "--.", "Д": "-..", "Е": ".",
        "Ж": "...-", "З": "--..", "И": "..", "Й": ".---", "К": "-.-", "Л": ".-..",
        "М": "--", "Н": "-.", "О": "---", "П": ".--.", "Р": ".-.", "С": "...",
        "Т": "-", "У": "..-", "Ф": "..-.", "Х": "....", "Ц": "-.-.", "Ч": "---.",
        "Ш": "----", "Щ": "--.-", "Ы": "-.--", "Ь": "-..-", "Э": "..-..",
        "Ю": "..--", "Я": ".-.-",
    }

    text = input("Введите текст: ").upper()
    translated = []

    for char in text:
        if char == " ":
            translated.append("/")
        elif char in morse:
            translated.append(morse[char])

    print("Морзе:", " ".join(translated))


def multiplication_table():
    print_title("ТАБЛИЦА УМНОЖЕНИЯ")
    number = read_int("Число: ")
    limit = read_int("До какого числа: ", 1, 100)

    for i in range(1, limit + 1):
        print(f"{number} x {i} = {number * i}")


def show_menu(tools):
    print("\n" + "=" * 64)
    print(f"    {APP_NAME} v{APP_VERSION} от {AUTHOR}")
    print("   Коллекция полезных инструментов и игр")
    print("   Создано для обучения и развлечения от Kronos Russian при поддержке Codex 5.5")
    print(f"    Дата: {DATE}")
    print("=" * 64)

    current_category = None

    for key, tool in tools.items():
        category, name, _ = tool

        if category != current_category:
            current_category = category
            print(f"\n[{category}]")

        print(f"  {key:>2}. {name}")

    print("\n   0. Выход")
    print("=" * 54)


def main():
    tools = {
        "1": ("Математика", "Умный калькулятор", calculator),
        "2": ("Математика", "Площадь и объем", area_calculator),
        "3": ("Математика", "Простые числа", prime_numbers),
        "4": ("Математика", "Статистика чисел", statistics_tool),
        "5": ("Математика", "Конвертер систем счисления", number_converter),
        "6": ("Математика", "Таблица умножения", multiplication_table),

        "7": ("Конвертеры", "Конвертер температуры", temperature_converter),
        "8": ("Конвертеры", "Конвертер валют", currency_converter),

        "9": ("Текст", "Блокнот", notepad),
        "10": ("Текст", "Счетчик слов", word_counter),
        "11": ("Текст", "Инструменты для текста", text_tools),
        "12": ("Текст", "Переводчик в азбуку Морзе", morse_code_translator),

        "13": ("Игры", "Угадай число", guess_number),
        "14": ("Игры", "Камень-ножницы-бумага", rock_paper_scissors),
        "15": ("Игры", "Викторина", quiz),
        "16": ("Игры", "Угадай карту", card_guess),
        "17": ("Игры", "Бросок кубика", dice_roller),
        "18": ("Игры", "Монетка", coin_flipper),

        "19": ("Жизнь", "Таймер", countdown_timer),
        "20": ("Жизнь", "День недели", day_of_week),
        "21": ("Жизнь", "Калькулятор возраста", age_calculator),
        "22": ("Жизнь", "Калькулятор ИМТ", bmi_calculator),
        "23": ("Жизнь", "Список дел", todo_list),

        "24": ("Разное", "Мини чат-бот Kronos", chatbot),
        "25": ("Разное", "Факт дня", fact_of_day),
        "26": ("Разное", "Случайный выбор имени", random_name_picker),
    }

    while True:
        show_menu(tools)
        choice = input("Выберите инструмент: ").strip()

        if choice == "0":
            print(f"\nДо свидания! {APP_NAME} v{APP_VERSION} от {AUTHOR}.")
            break

        if choice in tools:
            tools[choice][2]()
            pause()
        else:
            print("Неверный выбор.")


if __name__ == "__main__":
    main()