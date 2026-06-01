rates = {
    "KZT": 1,
    "USD": 481,
    "EUR": 556,
    "RUB": 6.7,
    "CNY": 70,
    "GBP": 638,
    "JPY": 3.2,
    "AED": 131,
    "KRW": 0.36,
    "INR": 5.8,
    "CAD": 355,
    "AUD": 312,
    "CHF": 578,
    "SEK": 48,
    "NOK": 46,
    "DKK": 75,
    "SGD": 374,
    "HKD": 62,
    "MXN": 25,
    "BRL": 88,
    "ZAR": 27,
    "TRY": 14,
    "PLN": 128,
    "THB": 14,
    "MYR": 111,
    "IDR": 0.030,
    "PHP": 8.5,
    "CZK": 23,
    "HUF": 1.35,
    "NZD": 289,
}

def show_currencies():
    print("\nAvailable currencies:")
    currencies = list(rates.keys())
    for i in range(0, len(currencies), 5):
        print("  " + "  ".join(currencies[i:i+5]))

def main():
    print("=" * 45)
    print("   MONEY CONVERTOR V2 by Kronos English")
    print("   30 currencies from around the world")
    print("   Rates updated: 28.05.2026")
    print("=" * 45)

    while True:
        show_currencies()

        print("\n1. Convert one currency to another")
        print("2. Convert to ALL currencies at once")
        print("0. Exit")

        choice = input("\nChoice: ")

        if choice == "1":
            from_cur = input("From currency: ").upper()
            to_cur = input("To currency: ").upper()

            if from_cur not in rates:
                print(f"❌ Unknown currency: {from_cur}")
                continue
            if to_cur not in rates:
                print(f"❌ Unknown currency: {to_cur}")
                continue

            try:
                amount = float(input("Amount: "))
            except ValueError:
                print("❌ Enter a number!")
                continue

            result = amount * rates[from_cur] / rates[to_cur]
            print(f"\n✅ {amount} {from_cur} = {result:.2f} {to_cur}")

        elif choice == "2":
            from_cur = input("From currency: ").upper()

            if from_cur not in rates:
                print(f"❌ Unknown currency: {from_cur}")
                continue

            try:
                amount = float(input("Amount: "))
            except ValueError:
                print("❌ Enter a number!")
                continue

            print(f"\n{amount} {from_cur} in all currencies:")
            print("-" * 35)
            for cur, rate in rates.items():
                if cur != from_cur:
                    result = amount * rates[from_cur] / rate
                    print(f"  {cur:<6} = {result:>12.2f}")

        elif choice == "0":
            print("\nGoodbye! — Money Convertor V2 by Kronos")
            input("\nPress Enter to close...")
            break

        else:
            print("❌ Invalid choice!")

        again = input("\nConvert again? (yes/no): ")
        if again.lower() != "yes":
            print("\nGoodbye! — Money Convertor V2 by Kronos")
            input("\nPress Enter to close...")
            break

main()