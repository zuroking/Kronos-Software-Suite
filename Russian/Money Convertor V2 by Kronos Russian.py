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
    print("\nДоступные валюты:")
    currencies = list(rates.keys())
    for i in range(0, len(currencies), 5):
        print("  " + "  ".join(currencies[i:i+5]))

def main():
    print("=" * 50)
    print("   Конвертор валют Kronos Russian")
    print("   30 разных валют со всего мира!")
    print("   Последняя дата обновления курса валют: 28.05.2026")
    print("=" * 50)

    while True:
        show_currencies()

        print("\n1. Конвертировать из одной валюты в другую")
        print("2. Конвертировать в ВСЕ валюты одновременно")
        print("0. Выход")

        choice = input("\nВыбор: ")

        if choice == "1":
            from_cur = input("Из какой валюты: ").upper()
            to_cur = input("В какую валюту: ").upper()

            if from_cur not in rates:
                print(f"❌ Неизвестная валюта: {from_cur}")
                continue
            if to_cur not in rates:
                print(f"❌ Неизвестная валюта: {to_cur}")
                continue

            try:
                amount = float(input("Сумма: "))
            except ValueError:
                print("❌ Введите число!")
                continue

            result = amount * rates[from_cur] / rates[to_cur]
            print(f"\n✅ {amount} {from_cur} = {result:.2f} {to_cur}")

        elif choice == "2":
            from_cur = input("Из какой валюты: ").upper()

            if from_cur not in rates:
                print(f"❌ Неизвестная валюта: {from_cur}")
                continue

            try:
                amount = float(input("Сумма: "))
            except ValueError:
                print("❌ Введите число!")
                continue

            print(f"\n{amount} {from_cur} в всех валютах:")
            print("-" * 35)
            for cur, rate in rates.items():
                if cur != from_cur:
                    result = amount * rates[from_cur] / rate
                    print(f"  {cur:<6} = {result:>12.2f}")

        elif choice == "0":
            print("\nGoodbye! — Конвертор валют V2 от Kronos Russian")
            input("\nНажмите Enter чтобы выйти...")
            break

        else:
            print("❌ Неправильный выбор!")

        again = input("\nКонвертировать ещё? (yes/no): ")
        if again.lower() != "yes":
            print("\nGoodbye! — Конвертор валют V2 от Kronos Russian")
            input("\nНажмите Enter чтобы выйти...")
            break

main()