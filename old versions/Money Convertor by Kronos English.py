print("Money Convertor by Kronos English")
print("I can help you convert money between different currencies!")
print("Just tell me which one you want to convert from and which one you want to convert to, and I'll do the rest!")
print("Currencies: KZT, USD, EUR, CNY, RUB")

rates = {
    "KZT": 1,
    "USD": 481,
    "EUR": 556,
    "CNY": 70,
    "RUB": 6.7
}

while True:
    from_cur = input("\nFrom which currency: ").upper()
    to_cur = input("To which currency: ").upper()

    if from_cur not in rates:
        print("Invalid currency! Please try again.")
        continue
    if to_cur not in rates:
        print("Invalid currency! Please try again.")
        continue

    amount = float(input("Enter the amount: "))
    result = amount * rates[from_cur] / rates[to_cur]
    print(f"{amount} {from_cur} = {result:.2f} {to_cur}")

    again = input("\nConvert again? (yes/no): ")
    if again.lower() != "yes":
        break

print("Thank you for using the currency converter by Kronos English!")
print("We hope we were helpful to you!")
print("Goodbye!")
input("\nPress Enter to close...")