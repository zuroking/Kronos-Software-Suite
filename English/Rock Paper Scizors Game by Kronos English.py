print("Rock Paper Scissors Game!")
print("I can help you play the classic game of rock, paper, scissors against the computer itself!")
print("Game by Kronos English")
import random
while True:
    user_input = input("Choose rock, paper, or scissors (or 'exit' to quit): ").lower()
    if user_input == 'exit':
        print("Thank you for playing!")
        break
    elif user_input not in ['rock', 'paper', 'scissors']:
        print("Invalid input. Please choose rock, paper, or scissors.")
        continue

    options = ['rock', 'paper', 'scissors']
    computer_choice = random.choice(options)
    print(f"Computer chose: {computer_choice}")

    if user_input == computer_choice:
        print("It's a tie!")
    elif (user_input == 'rock' and computer_choice == 'scissors') or (user_input == 'scissors' and computer_choice == 'paper') or (user_input == 'paper' and computer_choice == 'rock'):
        print("You win!")
    else:
        print("You lose!")