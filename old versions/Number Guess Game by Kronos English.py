import random

number = random.randint(1, 100)
print("Welcome to the Number Guess Game by Kronos English!")
print("Guess the number from 1 to 100!")

while True:
    attempt = int(input("Enter a number: "))
    if attempt < number:
        print("Too small! Try again.")
    elif attempt > number:
        print("Too big! Try again.")
    else:
        print("Congratulations! You guessed the number!")
        input("\nPress Enter to close...")
        break