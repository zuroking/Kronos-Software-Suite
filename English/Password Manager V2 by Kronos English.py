import os
import secrets
import string
import sqlite3
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet

DB_NAME = "kronos_passwords.db"

def get_crypto_key(master_password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000
    )
    return base64.urlsafe_b64encode(kdf.derive(master_password.encode()))

def encrypt_val(data: str, key: bytes) -> bytes:
    return Fernet(key).encrypt(data.encode())

def decrypt_val(encrypted_data: bytes, key: bytes) -> str:
    return Fernet(key).decrypt(encrypted_data).decode()

def generate_pass(length: int = 16) -> str:
    chars = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    while True:
        password = ''.join(secrets.choice(chars) for _ in range(length))
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and any(c.isdigit() for c in password)
                and any(c in "!@#$%^&*()-_=+" for c in password)):
            return password

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS credentials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service TEXT NOT NULL,
                username TEXT NOT NULL,
                password BLOB NOT NULL,
                salt BLOB NOT NULL
            )
        ''')
        conn.commit()

def save_password(service, username, raw_password, master_password):
    salt = os.urandom(16)
    key = get_crypto_key(master_password, salt)
    enc_password = encrypt_val(raw_password, key)
    
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO credentials (service, username, password, salt) VALUES (?, ?, ?, ?)",
            (service, username, enc_password, salt)
        )
        conn.commit()
    print(f"\n[+] Entry for {service} saved successfully.")

def view_passwords(master_password):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT service, username, password, salt FROM credentials")
        rows = cursor.fetchall()
    
    if not rows:
        print("\nDatabase is empty.")
        return

    print("\n" + "=" * 40)
    print("         STORED PASSWORDS")
    print("=" * 40)
    
    err = False
    for service, username, enc_password, salt in rows:
        try:
            key = get_crypto_key(master_password, salt)
            dec_password = decrypt_val(enc_password, key)
            print(f"Service: {service:<12} | Login: {username:<12} | Password: {dec_password}")
        except Exception:
            print(f"Service: {service:<12} | Login: {username:<12} | [Decryption Error]")
            err = True
            
    if err:
        print("\n[!] Error: Invalid master password.")
    print("=" * 40)

def main():
    init_db()
    print("--- KRONOS PASSWORD MANAGER V2 BY KRONOS RUSSIAN ---")
    
    master_pass = input("Enter master password: ").strip()
    if not master_pass:
        print("Error: Password cannot be empty.")
        return

    while True:
        print("\n1. Add account")
        print("2. Show passwords")
        print("3. Generate random password")
        print("4. Exit")
        
        step = input("\nAction: ").strip()
        
        if step == "1":
            service = input("Service: ").strip()
            username = input("Login: ").strip()
            
            print("Password (Press Enter for auto-generation):")
            user_pass = input("> ").strip()
            
            if not user_pass:
                user_pass = generate_pass()
                print(f"Generated password: {user_pass}")
                
            if service and username:
                save_password(service, username, user_pass, master_pass)
            else:
                print("Error: All fields must be filled.")
                
        elif step == "2":
            view_passwords(master_pass)
            
        elif step == "3":
            try:
                length = int(input("Password length (default 16): "))
            except ValueError:
                length = 16
            print(f"Password: {generate_pass(length)}")
            
        elif step == "4":
            print("Exiting.")
            break
        else:
            print("Invalid input.")

if __name__ == "__main__":
    main()