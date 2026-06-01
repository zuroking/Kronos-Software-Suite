import math
import random
import string
import datetime

def calculator():
    print("\n=== CALCULATOR by Kronos English ===")
    a = float(input("First number: "))
    b = float(input("Second number: "))
    print("Addition:", a + b)
    print("Subtraction:", a - b)
    print("Multiplication:", a * b)
    if b != 0:
        print("Division:", a / b)
        print("Remainder:", a % b)
    else:
        print("Cannot divide by zero!")
    print("Power a^b:", a ** b)
    if a >= 0:
        print("Square root of a:", math.sqrt(a))

def guess_number():
    print("\n=== GUESS THE NUMBER by Kronos English ===")
    number = random.randint(1, 100)
    attempts = 0
    while True:
        try:
            guess = int(input("Enter a number from 1 to 100: "))
            attempts += 1
            if guess < number:
                print("Too small!")
            elif guess > number:
                print("Too big!")
            else:
                print(f"You guessed it in {attempts} attempts!")
                break
        except ValueError:
            print("Please enter a whole number!")

def temperature_converter():
    print("\n=== TEMPERATURE CONVERTER by Kronos English ===")
    print("1. Celsius → Fahrenheit and Kelvin")
    print("2. Fahrenheit → Celsius and Kelvin")
    print("3. Kelvin → Celsius and Fahrenheit")
    choice = input("Choice: ")
    temp = float(input("Enter temperature: "))
    if choice == "1":
        print(f"Fahrenheit: {temp * 9/5 + 32:.2f}")
        print(f"Kelvin: {temp + 273.15:.2f}")
    elif choice == "2":
        print(f"Celsius: {(temp - 32) * 5/9:.2f}")
        print(f"Kelvin: {(temp - 32) * 5/9 + 273.15:.2f}")
    elif choice == "3":
        print(f"Celsius: {temp - 273.15:.2f}")
        print(f"Fahrenheit: {(temp - 273.15) * 9/5 + 32:.2f}")

def currency_converter():
    print("\n=== CURRENCY CONVERTER by Kronos English ===")
    print("Rates are approximate — update manually")
    # Rates updated: 28.05.2026
    rates = {"KZT": 1, "USD": 481, "EUR": 556, "CNY": 70, "RUB": 6.7}
    print("Currencies: KZT, USD, EUR, CNY, RUB")
    from_cur = input("From currency: ").upper()
    to_cur = input("To currency: ").upper()
    amount = float(input("Amount: "))
    if from_cur in rates and to_cur in rates:
        result = amount * rates[from_cur] / rates[to_cur]
        print(f"{amount} {from_cur} = {result:.2f} {to_cur}")
    else:
        print("Unknown currency!")

def area_calculator():
    print("\n=== AREA CALCULATOR by Kronos English ===")
    print("1. Circle")
    print("2. Square")
    print("3. Rectangle")
    print("4. Triangle")
    choice = input("Choice: ")
    if choice == "1":
        r = float(input("Radius: "))
        print(f"Circle area: {math.pi * r ** 2:.2f}")
    elif choice == "2":
        a = float(input("Side: "))
        print(f"Square area: {a ** 2:.2f}")
    elif choice == "3":
        a = float(input("Length: "))
        b = float(input("Width: "))
        print(f"Rectangle area: {a * b:.2f}")
    elif choice == "4":
        a = float(input("Base: "))
        h = float(input("Height: "))
        print(f"Triangle area: {0.5 * a * h:.2f}")

def prime_numbers():
    print("\n=== PRIME NUMBERS by Kronos English ===")
    n = int(input("Find all prime numbers up to: "))
    primes = []
    for num in range(2, n + 1):
        is_prime = True
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
    print(f"Prime numbers up to {n}:", primes)
    print(f"Total: {len(primes)}")

def notepad():
    print("\n=== NOTEPAD by Kronos English ===")
    filename = input("File name (without extension): ") + ".txt"
    print("Type your text. Empty line = save and exit:")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Saved to {filename}!")

def password_generator():
    print("\n=== PASSWORD GENERATOR by Kronos English ===")
    length = int(input("Password length: "))
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    while True:
        password = "".join(random.choice(chars) for _ in range(length))
        print(f"Your password: {password}")
        again = input("Generate another? (yes/no): ")
        if again.lower() != "yes":
            break

def word_counter():
    print("\n=== WORD COUNTER by Kronos English ===")
    text = input("Enter text: ")
    words = len(text.split())
    letters = len([c for c in text if c.isalpha()])
    spaces = text.count(" ")
    print(f"Words: {words}")
    print(f"Letters: {letters}")
    print(f"Spaces: {spaces}")
    print(f"Total characters: {len(text)}")

def text_reverser():
    print("\n=== TEXT REVERSER by Kronos English ===")
    text = input("Enter text: ")
    print("Reversed:", text[::-1])
    print("Words reversed:", " ".join(text.split()[::-1]))

def rock_paper_scissors():
    print("\n=== ROCK-PAPER-SCISSORS by Kronos English ===")
    choices = ["rock", "scissors", "paper"]
    score_player = 0
    score_computer = 0
    while True:
        player = input("Your choice (rock/scissors/paper) or 'stop': ").lower()
        if player == "stop":
            break
        if player not in choices:
            print("Invalid choice!")
            continue
        computer = random.choice(choices)
        print(f"Computer chose: {computer}")
        if player == computer:
            print("Draw!")
        elif (player == "rock" and computer == "scissors") or \
             (player == "scissors" and computer == "paper") or \
             (player == "paper" and computer == "rock"):
            print("You win!")
            score_player += 1
        else:
            print("Computer wins!")
            score_computer += 1
    print(f"Final score — You: {score_player} | Computer: {score_computer}")

def quiz():
    print("\n=== QUIZ by Kronos English ===")
    questions = [
        ("How many planets are in the Solar System?", ["6", "7", "8", "9"], "8"),
        ("What is the capital of Kazakhstan?", ["Almaty", "Astana", "Shymkent", "Aktobe"], "Astana"),
        ("What is 2^10?", ["512", "1024", "2048", "256"], "1024"),
        ("Who created the theory of relativity?", ["Newton", "Einstein", "Bohr", "Planck"], "Einstein"),
        ("What does AI stand for?", ["Auto Intelligence", "Artificial Intelligence", "Advanced Interface", "Auto Interface"], "Artificial Intelligence"),
    ]
    score = 0
    for q, options, answer in questions:
        print(f"\n{q}")
        for i, opt in enumerate(options, 1):
            print(f"  {i}. {opt}")
        user = input("Your answer: ")
        if user == answer or (user.isdigit() and options[int(user)-1] == answer):
            print("Correct! ✓")
            score += 1
        else:
            print(f"Wrong. Correct answer: {answer}")
    print(f"\nResult: {score}/{len(questions)}")

def card_guess():
    print("\n=== GUESS THE CARD by Kronos English ===")
    suits = ["♠ Spades", "♥ Hearts", "♦ Diamonds", "♣ Clubs"]
    values = ["2","3","4","5","6","7","8","9","10","Jack","Queen","King","Ace"]
    card = f"{random.choice(values)} {random.choice(suits)}"
    attempts = 3
    print(f"I picked a card. You have {attempts} attempts!")
    for i in range(attempts):
        guess = input(f"Attempt {i+1} — enter card (e.g. Ace ♠ Spades): ")
        if guess.lower() == card.lower():
            print("You got it! 🎉")
            return
        else:
            print(f"Nope! Attempts left: {attempts - i - 1}")
    print(f"You didn't guess it. The card was: {card}")

def dice_roller():
    print("\n=== DICE ROLLER by Kronos English ===")
    sides = int(input("Number of sides (e.g. 6, 12, 20): "))
    count = int(input("How many times to roll: "))
    results = [random.randint(1, sides) for _ in range(count)]
    print(f"Results: {results}")
    print(f"Sum: {sum(results)}")
    print(f"Average: {sum(results)/len(results):.2f}")

def countdown_timer():
    import time
    print("\n=== COUNTDOWN TIMER by Kronos English ===")
    seconds = int(input("Enter number of seconds: "))
    print("Timer started!")
    for i in range(seconds, 0, -1):
        print(f"\r⏱ Time left: {i} sec   ", end="")
        time.sleep(1)
    print("\n🔔 Time's up!")

def day_of_week():
    print("\n=== DAY OF THE WEEK by Kronos English ===")
    date_str = input("Enter date (DD.MM.YYYY): ")
    try:
        date = datetime.datetime.strptime(date_str, "%d.%m.%Y")
        days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        print(f"{date_str} is a {days[date.weekday()]}")
    except ValueError:
        print("Invalid date format!")

def number_converter():
    print("\n=== NUMBER SYSTEM CONVERTER by Kronos English ===")
    print("1. Decimal → Binary, Octal, Hexadecimal")
    print("2. Binary → Decimal")
    print("3. Hexadecimal → Decimal")
    choice = input("Choice: ")
    if choice == "1":
        n = int(input("Enter number: "))
        print(f"Binary: {bin(n)[2:]}")
        print(f"Octal: {oct(n)[2:]}")
        print(f"Hexadecimal: {hex(n)[2:].upper()}")
    elif choice == "2":
        b = input("Binary number: ")
        print(f"Decimal: {int(b, 2)}")
    elif choice == "3":
        h = input("Hexadecimal number: ")
        print(f"Decimal: {int(h, 16)}")

def statistics():
    print("\n=== NUMBER STATISTICS by Kronos English ===")
    nums = list(map(float, input("Enter numbers separated by spaces: ").split()))
    print(f"Sum: {sum(nums)}")
    print(f"Average: {sum(nums)/len(nums):.2f}")
    print(f"Minimum: {min(nums)}")
    print(f"Maximum: {max(nums)}")
    nums_sorted = sorted(nums)
    mid = len(nums_sorted) // 2
    median = nums_sorted[mid] if len(nums_sorted) % 2 != 0 else (nums_sorted[mid-1] + nums_sorted[mid]) / 2
    print(f"Median: {median}")

def chatbot():
    print("\n=== KRONOS MINI CHATBOT by Kronos English ===")
    print("Hello! I'm Kronos. Type 'bye' to exit.")
    responses = {
        "hello": "Hello! How are you?",
        "hi": "Hey! How can I help?",
        "how are you": "Great, thanks! Ready to help.",
        "who are you": "I'm Kronos — an AI created by Kronos. One day I'll be better than GPT!",
        "what can you do": "Not much yet, but soon I'll be able to do everything!",
        "help": "I can answer simple questions. Ask away!",
        "bye": "Goodbye! 👋",
    }
    while True:
        user = input("You: ").lower()
        if user == "bye":
            print("Kronos: Goodbye! 👋")
            break
        response = responses.get(user, "Interesting question! I'm still learning. Try asking something else.")
        print(f"Kronos: {response}")

def fact_of_day():
    print("\n=== FACT OF THE DAY by Kronos English ===")
    facts = [
        "Octopuses have three hearts and blue blood.",
        "Honey never spoils — edible honey was found in Egyptian tombs.",
        "Lightning strikes the Earth about 100 times per second.",
        "The human brain consumes about 20% of the body's energy.",
        "Python's first version was released in 1991.",
        "The Transformer architecture was invented in 2017.",
        "ChatGPT reached 1 million users in just 5 days.",
        "There are over 700 programming languages in the world.",
        "The first computer virus is considered to be Creeper (1971).",
        "Nanjing served as the capital of China multiple times in history.",
    ]
    print(f"💡 {random.choice(facts)}")

def main():
    tools = {
        "1":  ("Calculator by Kronos English", calculator),
        "2":  ("Guess the Number by Kronos English", guess_number),
        "3":  ("Temperature Converter by Kronos English", temperature_converter),
        "4":  ("Currency Converter by Kronos English", currency_converter),
        "5":  ("Area Calculator by Kronos English", area_calculator),
        "6":  ("Prime Numbers by Kronos English", prime_numbers),
        "7":  ("Notepad by Kronos English", notepad),
        "8":  ("Password Generator by Kronos English", password_generator),
        "9":  ("Word Counter by Kronos English", word_counter),
        "10": ("Text Reverser by Kronos English", text_reverser),
        "11": ("Rock-Paper-Scissors by Kronos English", rock_paper_scissors),
        "12": ("Quiz by Kronos English", quiz),
        "13": ("Guess the Card by Kronos English", card_guess),
        "14": ("Dice Roller by Kronos English", dice_roller),
        "15": ("Countdown Timer by Kronos English", countdown_timer),
        "16": ("Day of the Week by Kronos English", day_of_week),
        "17": ("Number System Converter by Kronos English", number_converter),
        "18": ("Number Statistics by Kronos English", statistics),
        "19": ("Kronos Mini Chatbot by Kronos English", chatbot),
        "20": ("Fact of the Day by Kronos English", fact_of_day),
    }

    while True:
        print("\n" + "=" * 40)
        print("     KRONOS TOOLKIT v1.0 by Kronos English")
        print("     Date: 28.05.2026")
        print("     More tools coming in future updates!")
        print("=" * 40)
        for key, (name, _) in tools.items():
            print(f"  {key:>2}. {name}")
        print("   0. Exit")
        print("=" * 40)

        choice = input("Choose a tool: ")

        if choice == "0":
            print("\nGoodbye! — Kronos Toolkit by Kronos English")
            input("Press Enter to close...")
            break
        elif choice in tools:
            tools[choice][1]()
            input("\n↩ Press Enter to return to menu...")
        else:
            print("Invalid choice!")

main()