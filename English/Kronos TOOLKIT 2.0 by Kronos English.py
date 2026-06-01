import datetime
import math
import random
import secrets
import string
import time


APP_NAME = "KRONOS TOOLKIT"
APP_VERSION = "2.0"
AUTHOR = "Kronos English"
DATE = "06.06.2026"


def pause():
    input("\nPress Enter to return to menu...")


def read_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")


def read_int(prompt, minimum=None, maximum=None):
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Please enter a whole number.")
            continue

        if minimum is not None and value < minimum:
            print(f"Number must be at least {minimum}.")
            continue
        if maximum is not None and value > maximum:
            print(f"Number must be at most {maximum}.")
            continue
        return value


def read_choice(prompt, choices):
    choices = {str(choice) for choice in choices}
    while True:
        value = input(prompt).strip()
        if value in choices:
            return value
        print("Invalid choice. Try again.")


def print_title(title):
    print(f"\n=== {title} by {AUTHOR} ===")


def calculator():
    print_title("SMART CALCULATOR")
    print("1. Basic operations")
    print("2. Advanced operations")
    choice = read_choice("Choice: ", ["1", "2"])

    if choice == "1":
        a = read_float("First number: ")
        b = read_float("Second number: ")
        print(f"Addition: {a + b}")
        print(f"Subtraction: {a - b}")
        print(f"Multiplication: {a * b}")
        if b == 0:
            print("Division: cannot divide by zero")
            print("Remainder: cannot divide by zero")
        else:
            print(f"Division: {a / b}")
            print(f"Remainder: {a % b}")
        print(f"Power a^b: {a ** b}")
    else:
        a = read_float("Number: ")
        if a >= 0:
            print(f"Square root: {math.sqrt(a)}")
        else:
            print("Square root: not available for negative numbers")
        print(f"Absolute value: {abs(a)}")
        print(f"Rounded: {round(a)}")
        if a > 0:
            print(f"Natural log: {math.log(a):.4f}")


def guess_number():
    print_title("GUESS THE NUMBER")
    low = read_int("Minimum number: ")
    high = read_int("Maximum number: ", low + 1)
    number = random.randint(low, high)
    attempts = 0

    print(f"I picked a number from {low} to {high}.")
    while True:
        guess = read_int("Your guess: ", low, high)
        attempts += 1
        if guess < number:
            print("Too small.")
        elif guess > number:
            print("Too big.")
        else:
            print(f"You guessed it in {attempts} attempts!")
            break


def temperature_converter():
    print_title("TEMPERATURE CONVERTER")
    print("1. Celsius to Fahrenheit and Kelvin")
    print("2. Fahrenheit to Celsius and Kelvin")
    print("3. Kelvin to Celsius and Fahrenheit")
    choice = read_choice("Choice: ", ["1", "2", "3"])
    temp = read_float("Enter temperature: ")

    if choice == "1":
        print(f"Fahrenheit: {temp * 9 / 5 + 32:.2f}")
        print(f"Kelvin: {temp + 273.15:.2f}")
    elif choice == "2":
        celsius = (temp - 32) * 5 / 9
        print(f"Celsius: {celsius:.2f}")
        print(f"Kelvin: {celsius + 273.15:.2f}")
    else:
        celsius = temp - 273.15
        print(f"Celsius: {celsius:.2f}")
        print(f"Fahrenheit: {celsius * 9 / 5 + 32:.2f}")


def currency_converter():
    print_title("CURRENCY CONVERTER")
    print("Rates are approximate. Update manually when needed.")
    rates = {"KZT": 1, "USD": 481, "EUR": 556, "CNY": 70, "RUB": 6.7}
    print("Currencies:", ", ".join(rates))

    from_cur = input("From currency: ").upper().strip()
    to_cur = input("To currency: ").upper().strip()
    amount = read_float("Amount: ")

    if from_cur in rates and to_cur in rates:
        result = amount * rates[from_cur] / rates[to_cur]
        print(f"{amount:.2f} {from_cur} = {result:.2f} {to_cur}")
    else:
        print("Unknown currency.")


def area_calculator():
    print_title("AREA AND VOLUME CALCULATOR")
    print("1. Circle area")
    print("2. Square area")
    print("3. Rectangle area")
    print("4. Triangle area")
    print("5. Cube volume")
    print("6. Cylinder volume")
    choice = read_choice("Choice: ", ["1", "2", "3", "4", "5", "6"])

    if choice == "1":
        r = read_float("Radius: ")
        print(f"Circle area: {math.pi * r ** 2:.2f}")
    elif choice == "2":
        a = read_float("Side: ")
        print(f"Square area: {a ** 2:.2f}")
    elif choice == "3":
        a = read_float("Length: ")
        b = read_float("Width: ")
        print(f"Rectangle area: {a * b:.2f}")
    elif choice == "4":
        a = read_float("Base: ")
        h = read_float("Height: ")
        print(f"Triangle area: {0.5 * a * h:.2f}")
    elif choice == "5":
        a = read_float("Side: ")
        print(f"Cube volume: {a ** 3:.2f}")
    else:
        r = read_float("Radius: ")
        h = read_float("Height: ")
        print(f"Cylinder volume: {math.pi * r ** 2 * h:.2f}")


def prime_numbers():
    print_title("PRIME NUMBERS")
    n = read_int("Find all prime numbers up to: ", 2)
    primes = []
    for num in range(2, n + 1):
        is_prime = True
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
    print(f"Prime numbers up to {n}: {primes}")
    print(f"Total: {len(primes)}")


def notepad():
    print_title("NOTEPAD")
    filename = input("File name without extension: ").strip() or "kronos_note"
    filename = f"{filename}.txt"
    print("Type your text. Empty line = save and exit.")

    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)

    with open(filename, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))
    print(f"Saved to {filename}.")


def password_generator():
    print_title("SECURE PASSWORD GENERATOR")
    length = read_int("Password length: ", 4, 128)
    use_symbols = input("Use symbols? (yes/no): ").lower().strip() == "yes"
    chars = string.ascii_letters + string.digits
    if use_symbols:
        chars += "!@#$%^&*()-_=+[]{}"

    while True:
        password = "".join(secrets.choice(chars) for _ in range(length))
        print(f"Your password: {password}")
        again = input("Generate another? (yes/no): ").lower().strip()
        if again != "yes":
            break


def word_counter():
    print_title("WORD COUNTER")
    text = input("Enter text: ")
    words = text.split()
    letters = sum(1 for char in text if char.isalpha())
    digits = sum(1 for char in text if char.isdigit())
    spaces = text.count(" ")
    print(f"Words: {len(words)}")
    print(f"Letters: {letters}")
    print(f"Digits: {digits}")
    print(f"Spaces: {spaces}")
    print(f"Total characters: {len(text)}")


def text_reverser():
    print_title("TEXT TOOLS")
    text = input("Enter text: ")
    print(f"Reversed: {text[::-1]}")
    print(f"Words reversed: {' '.join(text.split()[::-1])}")
    print(f"UPPERCASE: {text.upper()}")
    print(f"lowercase: {text.lower()}")
    print(f"Title Case: {text.title()}")


def rock_paper_scissors():
    print_title("ROCK-PAPER-SCISSORS")
    choices = ["rock", "scissors", "paper"]
    score_player = 0
    score_computer = 0

    while True:
        player = input("Your choice (rock/scissors/paper) or stop: ").lower().strip()
        if player == "stop":
            break
        if player not in choices:
            print("Invalid choice.")
            continue

        computer = random.choice(choices)
        print(f"Computer chose: {computer}")
        if player == computer:
            print("Draw.")
        elif (player == "rock" and computer == "scissors") or (
            player == "scissors" and computer == "paper"
        ) or (player == "paper" and computer == "rock"):
            print("You win!")
            score_player += 1
        else:
            print("Computer wins!")
            score_computer += 1

    print(f"Final score - You: {score_player} | Computer: {score_computer}")


def quiz():
    print_title("QUIZ")
    questions = [
        ("How many planets are in the Solar System?", ["6", "7", "8", "9"], "8"),
        ("What is the capital of Kazakhstan?", ["Almaty", "Astana", "Shymkent", "Aktobe"], "Astana"),
        ("What is 2^10?", ["512", "1024", "2048", "256"], "1024"),
        ("Who created the theory of relativity?", ["Newton", "Einstein", "Bohr", "Planck"], "Einstein"),
        ("What does AI stand for?", ["Auto Intelligence", "Artificial Intelligence", "Advanced Interface", "Auto Interface"], "Artificial Intelligence"),
        ("Which language is this toolkit written in?", ["Java", "Python", "C++", "HTML"], "Python"),
        ("What is the largest ocean?", ["Atlantic", "Indian", "Pacific", "Arctic"], "Pacific"),
    ]

    random.shuffle(questions)
    score = 0
    for question, options, answer in questions:
        print(f"\n{question}")
        for index, option in enumerate(options, 1):
            print(f"  {index}. {option}")

        user = input("Your answer: ").strip()
        if user.isdigit() and 1 <= int(user) <= len(options):
            user_answer = options[int(user) - 1]
        else:
            user_answer = user

        if user_answer.lower() == answer.lower():
            print("Correct!")
            score += 1
        else:
            print(f"Wrong. Correct answer: {answer}")

    print(f"\nResult: {score}/{len(questions)}")


def card_guess():
    print_title("GUESS THE CARD")
    suits = ["Spades", "Hearts", "Diamonds", "Clubs"]
    values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
    card_value = random.choice(values)
    card_suit = random.choice(suits)
    attempts = 3

    print(f"I picked a card. You have {attempts} attempts.")
    print("Example answer: Ace Spades")
    for attempt in range(1, attempts + 1):
        guess = input(f"Attempt {attempt}: ").lower().strip()
        if guess == f"{card_value} {card_suit}".lower():
            print("You got it!")
            return
        print(f"No. Attempts left: {attempts - attempt}")

    print(f"The card was: {card_value} {card_suit}")


def dice_roller():
    print_title("DICE ROLLER")
    sides = read_int("Number of sides: ", 2)
    count = read_int("How many times to roll: ", 1, 100)
    results = [random.randint(1, sides) for _ in range(count)]
    print(f"Results: {results}")
    print(f"Sum: {sum(results)}")
    print(f"Average: {sum(results) / len(results):.2f}")


def countdown_timer():
    print_title("COUNTDOWN TIMER")
    seconds = read_int("Enter number of seconds: ", 1)
    print("Timer started.")
    for remaining in range(seconds, 0, -1):
        print(f"\rTime left: {remaining} sec   ", end="")
        time.sleep(1)
    print("\nTime's up!")


def day_of_week():
    print_title("DAY OF THE WEEK")
    date_str = input("Enter date (DD.MM.YYYY): ").strip()
    try:
        date = datetime.datetime.strptime(date_str, "%d.%m.%Y")
    except ValueError:
        print("Invalid date format.")
        return

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    print(f"{date_str} is a {days[date.weekday()]}")


def number_converter():
    print_title("NUMBER SYSTEM CONVERTER")
    print("1. Decimal to Binary, Octal, Hexadecimal")
    print("2. Binary to Decimal")
    print("3. Octal to Decimal")
    print("4. Hexadecimal to Decimal")
    choice = read_choice("Choice: ", ["1", "2", "3", "4"])

    try:
        if choice == "1":
            number = read_int("Enter decimal number: ")
            print(f"Binary: {bin(number)[2:]}")
            print(f"Octal: {oct(number)[2:]}")
            print(f"Hexadecimal: {hex(number)[2:].upper()}")
        elif choice == "2":
            print(f"Decimal: {int(input('Binary number: '), 2)}")
        elif choice == "3":
            print(f"Decimal: {int(input('Octal number: '), 8)}")
        else:
            print(f"Decimal: {int(input('Hexadecimal number: '), 16)}")
    except ValueError:
        print("Invalid number for selected system.")


def statistics_tool():
    print_title("NUMBER STATISTICS")
    try:
        nums = [float(item) for item in input("Enter numbers separated by spaces: ").split()]
    except ValueError:
        print("Please enter only numbers.")
        return

    if not nums:
        print("No numbers entered.")
        return

    nums_sorted = sorted(nums)
    mid = len(nums_sorted) // 2
    median = nums_sorted[mid] if len(nums_sorted) % 2 else (nums_sorted[mid - 1] + nums_sorted[mid]) / 2
    print(f"Sum: {sum(nums)}")
    print(f"Average: {sum(nums) / len(nums):.2f}")
    print(f"Minimum: {min(nums)}")
    print(f"Maximum: {max(nums)}")
    print(f"Median: {median}")


def chatbot():
    print_title("KRONOS MINI CHATBOT")
    print("Hello! I'm Kronos. Type bye to exit.")
    responses = {
        "hello": "Hello! How are you?",
        "hi": "Hey! How can I help?",
        "how are you": "Great, thanks! Ready to help.",
        "who are you": "I'm Kronos, a mini assistant created by Kronos.",
        "what can you do": "I can run tools, play games, convert values, and help with simple tasks.",
        "help": "Try asking: hello, who are you, what can you do, time, date, coin.",
        "time": lambda: f"Current time: {datetime.datetime.now().strftime('%H:%M:%S')}",
        "date": lambda: f"Current date: {datetime.datetime.now().strftime('%d.%m.%Y')}",
        "coin": lambda: f"Coin toss: {random.choice(['heads', 'tails'])}",
    }

    while True:
        user = input("You: ").lower().strip()
        if user == "bye":
            print("Kronos: Goodbye!")
            break

        response = responses.get(user, "Interesting question. I'm still learning.")
        if callable(response):
            response = response()
        print(f"Kronos: {response}")


def fact_of_day():
    print_title("FACT OF THE DAY")
    facts = [
        "Python's first version was released in 1991.",
        "The Transformer architecture was introduced in 2017.",
        "The first computer virus is considered to be Creeper from 1971.",
        "A leap year has 366 days.",
        "The International Space Station travels at about 28,000 km/h.",
        "The first email was sent in 1971.",
        "Zero is an even number.",
        "Kazakhstan is the largest landlocked country in the world.",
        "The Pacific Ocean is the largest ocean on Earth.",
        "Binary code uses only two digits: 0 and 1.",
    ]
    print(random.choice(facts))


def coin_flipper():
    print_title("COIN FLIPPER")
    count = read_int("How many coins to flip: ", 1, 1000)
    results = [random.choice(["Heads", "Tails"]) for _ in range(count)]
    print(f"Heads: {results.count('Heads')}")
    print(f"Tails: {results.count('Tails')}")
    if count <= 50:
        print(f"Results: {results}")


def bmi_calculator():
    print_title("BMI CALCULATOR")
    weight = read_float("Weight in kg: ")
    height_cm = read_float("Height in cm: ")
    if height_cm <= 0:
        print("Height must be greater than zero.")
        return

    bmi = weight / ((height_cm / 100) ** 2)
    print(f"BMI: {bmi:.2f}")
    if bmi < 18.5:
        print("Category: underweight")
    elif bmi < 25:
        print("Category: normal")
    elif bmi < 30:
        print("Category: overweight")
    else:
        print("Category: obesity")


def age_calculator():
    print_title("AGE CALCULATOR")
    birth_str = input("Enter birth date (DD.MM.YYYY): ").strip()
    try:
        birth_date = datetime.datetime.strptime(birth_str, "%d.%m.%Y").date()
    except ValueError:
        print("Invalid date format.")
        return

    today = datetime.date.today()
    if birth_date > today:
        print("Birth date cannot be in the future.")
        return

    years = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    days = (today - birth_date).days
    print(f"Age: {years} years")
    print(f"Days lived: {days}")


def todo_list():
    print_title("TODO LIST")
    tasks = []
    while True:
        print("\n1. Add task")
        print("2. Show tasks")
        print("3. Remove task")
        print("0. Exit todo list")
        choice = read_choice("Choice: ", ["1", "2", "3", "0"])

        if choice == "0":
            break
        if choice == "1":
            task = input("New task: ").strip()
            if task:
                tasks.append(task)
                print("Task added.")
        elif choice == "2":
            if not tasks:
                print("No tasks yet.")
            for index, task in enumerate(tasks, 1):
                print(f"{index}. {task}")
        else:
            if not tasks:
                print("No tasks to remove.")
                continue
            index = read_int("Task number to remove: ", 1, len(tasks))
            removed = tasks.pop(index - 1)
            print(f"Removed: {removed}")


def random_student_picker():
    print_title("RANDOM NAME PICKER")
    names = [name.strip() for name in input("Enter names separated by commas: ").split(",") if name.strip()]
    if not names:
        print("No names entered.")
        return
    print(f"Chosen name: {random.choice(names)}")


def morse_code_translator():
    print_title("MORSE CODE TRANSLATOR")
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
    text = input("Enter text: ").upper()
    translated = []
    for char in text:
        if char == " ":
            translated.append("/")
        elif char in morse:
            translated.append(morse[char])

    print("Morse:", " ".join(translated))


def multiplication_table():
    print_title("MULTIPLICATION TABLE")
    number = read_int("Number: ")
    limit = read_int("Limit: ", 1, 100)
    for i in range(1, limit + 1):
        print(f"{number} x {i} = {number * i}")


def show_menu(tools):
    print("\n" + "=" * 64)
    print(f"    {APP_NAME} v{APP_VERSION} by {AUTHOR}")
    print("   A collection of useful tools and games")
    print("   Created for learning and fun by Kronos English with support of Codex 5.5")
    print(f"    Date: {DATE}")
    print("=" * 64)

    current_category = None
    for key, tool in tools.items():
        category, name, _ = tool
        if category != current_category:
            current_category = category
            print(f"\n[{category}]")
        print(f"  {key:>2}. {name}")

    print("\n   0. Exit")
    print("=" * 64)


def main():
    tools = {
        "1": ("Math", "Smart Calculator", calculator),
        "2": ("Math", "Area and Volume Calculator", area_calculator),
        "3": ("Math", "Prime Numbers", prime_numbers),
        "4": ("Math", "Number Statistics", statistics_tool),
        "5": ("Math", "Number System Converter", number_converter),
        "6": ("Math", "Multiplication Table", multiplication_table),
        "7": ("Converters", "Temperature Converter", temperature_converter),
        "8": ("Converters", "Currency Converter", currency_converter),
        "9": ("Text", "Notepad", notepad),
        "10": ("Text", "Word Counter", word_counter),
        "11": ("Text", "Text Tools", text_reverser),
        "12": ("Text", "Morse Code Translator", morse_code_translator),
        "13": ("Games", "Guess the Number", guess_number),
        "14": ("Games", "Rock-Paper-Scissors", rock_paper_scissors),
        "15": ("Games", "Quiz", quiz),
        "16": ("Games", "Guess the Card", card_guess),
        "17": ("Games", "Dice Roller", dice_roller),
        "18": ("Games", "Coin Flipper", coin_flipper),
        "19": ("Life", "Countdown Timer", countdown_timer),
        "20": ("Life", "Day of the Week", day_of_week),
        "21": ("Life", "Age Calculator", age_calculator),
        "22": ("Life", "BMI Calculator", bmi_calculator),
        "23": ("Life", "Todo List", todo_list),
        "24": ("Fun", "Kronos Mini Chatbot", chatbot),
        "25": ("Fun", "Fact of the Day", fact_of_day),
        "26": ("Fun", "Random Name Picker", random_student_picker),
    }

    while True:
        show_menu(tools)
        choice = input("Choose a tool: ").strip()

        if choice == "0":
            print(f"\nGoodbye from {APP_NAME} v{APP_VERSION} by {AUTHOR}.")
            break
        if choice in tools:
            tools[choice][2]()
            pause()
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()