import random
import string
print("Генератор паролей от Kronos Russian")
length = int(input("Введите длину пароля: "))
characters = string.ascii_letters + string.digits + string.punctuation
password = ''.join(random.choice(characters) for i in range(length))
print("Ваш сгенерированный пароль: ", password)
again = input("Сгенерировать еще один? (yes/no): ")
while again.lower() == "yes":
    length = int(input("Введите длину пароля: "))
    password = ''.join(random.choice(characters) for i in range(length))
    print("Ваш сгенерированный пароль: ", password)
else:
    print("Спасибо за использование Генератора паролей! Будьте осторожны в интернете!")

input("\nНажмите Enter для закрытия...")