import random
import time

def main():
    print("=" * 50)
    print("   Game: Guess the number: Hardcore Edition by Kronos Russian")
    print("   Number from 1 to 1,000,000. Good luck...")
    print("=" * 50)

    while True:
        number = random.randint(1, 1_000_000)
        attempts = 0
        start_time = time.time()

        print("\nI have guessed a number from 1 to 1,000,000!")
        print("Try to guess it!\n")

        while True:
            try:
                guess = int(input("Your guess: "))
                attempts += 1

                if guess < 1 or guess > 1_000_000:
                    print("The number must be from 1 to 1,000,000!")
                    continue

                if guess < number:
                    diff = number - guess
                    if diff > 100_000:
                        print("Much more!")
                    elif diff > 10_000:
                        print("More!")
                    elif diff > 1_000:
                        print("A bit more!")
                    else:
                        print("Very close!")

                elif guess > number:
                    diff = guess - number
                    if diff > 100_000:
                        print("Much less!")
                    elif diff > 10_000:
                        print("Less!")
                    elif diff > 1_000:
                        print("A bit less!")
                    else:
                        print("Very close!")

                else:
                    end_time = time.time()
                    elapsed = round(end_time - start_time, 2)
                    print(f"\nYou guessed it in {attempts} attempts and {elapsed} seconds!")
                    if attempts <= 20:
                        print("Legend!")
                    elif attempts <= 40:
                        print("Not bad!")
                    else:
                        print("Keep practicing!")
                    break

            except ValueError:
                print("Enter a whole number!")

        again = input("\nPlay again? (yes/no): ")
        if again.lower() != "yes":
            print("\nGoodbye! — Hardcore Guess by Kronos Russian")
            input("\nPress Enter to close...")
            break

main()