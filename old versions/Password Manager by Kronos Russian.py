import os
import json
import cryptography
from cryptography.fernet import Fernet

print("=" * 50)
print("   Менеджер Паролей от Kronos Russian")
print("Добро пожаловать в Менеджер Паролей от Kronos Russian!")
print("Этот инструмент позволяет безопасно хранить и управлять вашими паролями.")
print("Пожалуйста, следуйте подсказкам, чтобы добавить, получить или удалить ваши пароли.")
print("Ваши пароли будут зашифрованы и сохранены безопасно на вашем устройстве.")
print("Kronos Russian не имеет доступа к вашим паролям. Ваша конфиденциальность - наш приоритет!")
print("Начнём!")
print("=" * 50)

class PasswordManager:
    def __init__(self, key_file='key.key', data_file='passwords.json'):
        self.key_file = key_file
        self.data_file = data_file
        self.key = self.load_key()
        self.fernet = Fernet(self.key)
        self.passwords = self.load_passwords()

    def load_key(self):
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as file:
                return file.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as file:
                file.write(key)
            return key

    def load_passwords(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                encrypted_data = json.load(file)
                decrypted_data = {k: self.fernet.decrypt(v.encode()).decode() for k, v in encrypted_data.items()}
                return decrypted_data
        else:
            return {}

    def save_passwords(self):
        encrypted_data = {k: self.fernet.encrypt(v.encode()).decode() for k, v in self.passwords.items()}
        with open(self.data_file, 'w') as file:
            json.dump(encrypted_data, file)

    def add_password(self, service, password):
        self.passwords[service] = password
        self.save_passwords()

    def get_password(self, service):
        return self.passwords.get(service, None)

    def delete_password(self, service):
        if service in self.passwords:
            del self.passwords[service]
            self.save_passwords()
    def list_services(self):
        return list(self.passwords.keys())

manager = PasswordManager()

while True:
    print("\n" + "=" * 40)
    print("1. Добавить пароль")
    print("2. Получить пароль")
    print("3. Удалить пароль")
    print("0. Выйти")
    print("=" * 40)

    choice = input("Выбор: ")

    if choice == "1":
        service = input("Название сайта/приложения для которого создаётся пароль: ")
        password = input("Пароль: ")
        manager.add_password(service, password)
        print(f"✅ Пароль для {service} сохранён!")

    elif choice == "2":
        service = input("Название сайта/приложения: ")
        result = manager.get_password(service)
        if result:
            print(f"🔑 Пароль для {service}: {result}")
        else:
            print("❌ Не найдено!")

    elif choice == "3":
        service = input("Название сайта/приложения: ")
        manager.delete_password(service)
        print(f"🗑️ {service} успешно удалён!")

    elif choice == "0":
        print("До свидания! - Менеджер паролей от Kronos Russian")
        input("\nНажмите Enter для выхода...")
        break

    else:
        print("Неправильный выбор!")