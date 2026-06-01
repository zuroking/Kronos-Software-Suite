print("Конвертор валют от Kronos Russian")
print("Я могу помочь вам конвертировать деньги между различными валютами!")
print("Просто введите валюту, из которой вы хотите конвертировать, и валюту, в которую вы хотите конвертировать.")
print("Валюты: KZT, USD, EUR, CNY, RUB")

rates = {
    "KZT": 1,
    "USD": 481,
    "EUR": 556,
    "CNY": 70,
    "RUB": 6.7
}

while True:
    from_cur = input("\nИз какой валюты: ").upper()
    to_cur = input("В какую валюту: ").upper()

    if from_cur not in rates:
        print("Неверная валюта! Попробуй снова.")
        continue
    if to_cur not in rates:
        print("Неверная валюта! Попробуй снова.")
        continue

    amount = float(input("Введите сумму: "))
    result = amount * rates[from_cur] / rates[to_cur]
    print(f"{amount} {from_cur} = {result:.2f} {to_cur}")

    again = input("\nКонвертировать ещё? (да/нет): ")
    if again.lower() != "да":
        break

print("Спасибо за использование конвертора валют от Kronos Russian!")
print("Надеемся, мы были полезны для вас!")
print("До свидания!")
input("\nНажмите Enter для закрытия...")