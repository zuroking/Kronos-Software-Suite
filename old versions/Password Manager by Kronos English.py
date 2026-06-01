import os
import json
import cryptography
from cryptography.fernet import Fernet

print("=" * 50)
print("   Password Manager by Kronos English")
print("Welcome to the Password Manager by Kronos English!")
print("This tool allows you to securely store and manage your passwords.")
print("Please follow the prompts to add, retrieve, or delete your passwords.")
print("Your passwords will be encrypted and stored securely on your device.")
print("Kronos English does not have access to your passwords. Your privacy is our priority!")
print("Let's get started!")
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
    print("1. Add password")
    print("2. Get password")
    print("3. Delete password")
    print("0. Exit")
    print("=" * 40)

    choice = input("Choice: ")

    if choice == "1":
        service = input("Site/App name: ")
        password = input("Password: ")
        manager.add_password(service, password)
        print(f"✅ Password for {service} saved!")

    elif choice == "2":
        service = input("Site/App name: ")
        result = manager.get_password(service)
        if result:
            print(f"🔑 Password for {service}: {result}")
        else:
            print("❌ Not found!")

    elif choice == "3":
        service = input("Site/App name: ")
        manager.delete_password(service)
        print(f"🗑️ {service} deleted!")

    elif choice == "0":
        print("Goodbye! — Kronos Password Manager")
        input("\nPress Enter to close...")
        break

    else:
        print("Invalid choice!")