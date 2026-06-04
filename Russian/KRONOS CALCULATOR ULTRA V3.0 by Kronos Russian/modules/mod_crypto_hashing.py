# modules/mod_crypto_hashing.py
import hashlib
import secrets
import base64
from kronos_core import Colors

METADATA = {
    "id": 13,
    "category": "ИНСТРУМЕНТЫ",
    "name": "Криптография (Сеть Фейстеля с визуализацией и PBKDF2)"
}

class AdvancedCrypto:
    @staticmethod
    def _feistel_round(right: bytes, subkey: bytes) -> bytes:
        hasher = hashlib.sha256()
        hasher.update(right + subkey)
        digest = hasher.digest()
        return digest[:len(right)]

    @classmethod
    def encrypt_feistel_visual(cls, text: str, key: str, ui_callback, rounds: int = 4) -> str:
        data = text.encode('utf-8')
        
        pad_len = 2 - (len(data) % 2)
        data += bytes([pad_len]) * pad_len
        
        mid = len(data) // 2
        left, right = data[:mid], data[mid:]
        
        master_hash = hashlib.sha256(key.encode('utf-8')).digest()
        subkeys = [master_hash[i::rounds][:16] for i in range(rounds)]
        
        ui_callback(f"\n{Colors.GRAY}[START]{Colors.RESET} Исходные блоки (байты):")
        ui_callback(f"  L0: {left.hex()} | R0: {right.hex()}")
        
        for i in range(rounds):
            f_res = cls._feistel_round(right, subkeys[i])
            new_left = right
            new_right = bytes(a ^ b for a, b in zip(left, f_res))
            
            left, right = new_left, new_right
            
            ui_callback(f"\n{Colors.CYAN}[РАУНД {i+1}]{Colors.RESET}")
            ui_callback(f"  • Раундовый ключ K{i+1}: {subkeys[i].hex()[:16]}...")
            ui_callback(f"  • Текущее состояние: L{i+1}={left.hex()} | R{i+1}={right.hex()}")
            
        cipher_bytes = right + left
        return base64.b64encode(cipher_bytes).decode('utf-8')

    @classmethod
    def decrypt_feistel_visual(cls, cipher_b64: str, key: str, ui_callback, rounds: int = 4) -> str:
        try:
            data = base64.b64decode(cipher_b64)
        except Exception:
            raise ValueError("Некорректный формат Base64 шифроблока.")
            
        if len(data) % 2 != 0:
            raise ValueError("Неверная длина шифроблока (должна быть четной).")
            
        mid = len(data) // 2
        left, right = data[:mid], data[mid:]
        
        master_hash = hashlib.sha256(key.encode('utf-8')).digest()
        subkeys = [master_hash[i::rounds][:16] for i in range(rounds)]
        
        ui_callback(f"\n{Colors.GRAY}[START]{Colors.RESET} Входные блоки шифра:")
        ui_callback(f"  L_cipher: {left.hex()} | R_cipher: {right.hex()}")
        
        for i in reversed(range(rounds)):
            new_right = left
            f_res = cls._feistel_round(left, subkeys[i])
            new_left = bytes(a ^ b for a, b in zip(right, f_res))
            
            left, right = new_left, new_right
            
            ui_callback(f"\n{Colors.MAGENTA}[ОБРАТНЫЙ РАУНД {i+1}]{Colors.RESET}")
            ui_callback(f"  • Восстановление через K{i+1}: {subkeys[i].hex()[:16]}...")
            ui_callback(f"  • Состояние: L={left.hex()} | R={right.hex()}")
            
        decrypted = left + right
        
        pad_len = decrypted[-1]
        if pad_len > 2 or pad_len < 1:
            raise ValueError("Критическая ошибка дешифрования: неверный ключ или поврежденные данные.")
            
        if decrypted[-pad_len:] != bytes([pad_len]) * pad_len:
            raise ValueError("Критическая ошибка дешифрования: целостность паддинга нарушена. Неверный ключ!")

        try:
            return decrypted[:-pad_len].decode('utf-8')
        except UnicodeDecodeError:
            raise ValueError("Ошибка декодирования UTF-8. Скорее всего, введен неверный мастер-ключ.")


class KronosPlugin:
    def __init__(self, app) -> None:
        self.app = app

    def execute(self) -> None:
        self.app.ui.print_smart(f"{Colors.BOLD}{Colors.CYAN}--- КРИПТОГРАФИЧЕСКИЙ КОМПЛЕКС ULTRA V3.0 ---{Colors.RESET}")
        print(" Выберите криптосистему:")
        print("  [1] Шифрование Сетью Фейстеля (С пошаговыми логами раундов)")
        print("  [2] Расшифрование Сети Фейстеля")
        print("  [3] Безопасное хеширование паролей (PBKDF2-SHA256)")
        
        choice = self.app.ui.get_input("Действие: ", int, lambda x: 1 <= x <= 3)
        log_cb = self.app.ui.print_smart
        
        try:
            if choice == 1:
                text = self.app.ui.get_input("Введи секретный текст: ", str)
                key = self.app.ui.get_input("Введи мастер-ключ (пароль): ", str)
                
                res = AdvancedCrypto.encrypt_feistel_visual(text, key, log_cb)
                
                self.app.ui.print_smart(f"\n{Colors.BOLD}{Colors.GREEN}[ИТОГОВЫЙ ШИФРОТЕКСТ BASE64]:{Colors.RESET}")
                self.app.ui.print_smart(f"  {Colors.BRIGHT_GREEN}{res}{Colors.RESET}")
                self.app.history.add("Крипто", "Feistel Encryption", "Успешно")
                
            elif choice == 2:
                cipher_b64 = self.app.ui.get_input("Введи шифротекст Base64: ", str)
                key = self.app.ui.get_input("Введи мастер-ключ: ", str)
                
                res = AdvancedCrypto.decrypt_feistel_visual(cipher_b64, key, log_cb)
                
                self.app.ui.print_smart(f"\n{Colors.BOLD}{Colors.GREEN}[РАСШИФРОВАННЫЕ ДАННЫЕ]:{Colors.RESET}")
                self.app.ui.print_smart(f"  {Colors.YELLOW}{res}{Colors.RESET}")
                self.app.history.add("Крипто", "Feistel Decryption", "Успешно")
                
            elif choice == 3:
                mode = self.app.ui.get_input("1 - Сгенерировать хеш, 2 - Верифицировать пароль: ", int, lambda x: x in (1, 2))
                if mode == 1:
                    pwd = self.app.ui.get_input("Введите пароль для базы данных: ", str)
                    salt = secrets.token_hex(16)
                    key = hashlib.pbkdf2_hmac('sha256', pwd.encode('utf-8'), salt.encode('utf-8'), 100000).hex()
                    
                    self.app.ui.print_smart(f"\n{Colors.GREEN}[БЕЗОПАСНЫЙ PBKDF2 ХЕШ СГЕНЕРИРОВАН]:{Colors.RESET}")
                    print(f"  • Соль (хранить открыто): {Colors.YELLOW}{salt}{Colors.RESET}")
                    print(f"  • Хеш (сохранить в БД):    {Colors.BRIGHT_CYAN}{key}{Colors.RESET}")
                else:
                    pwd = self.app.ui.get_input("Введите пароль для проверки: ", str)
                    salt = self.app.ui.get_input("Введите соль: ", str)
                    key = self.app.ui.get_input("Введите хеш из БД: ", str)
                    
                    new_key = hashlib.pbkdf2_hmac('sha256', pwd.encode('utf-8'), salt.encode('utf-8'), 100000).hex()
                    if secrets.compare_digest(new_key, key):
                        self.app.ui.print_smart(f"\n{Colors.BOLD}{Colors.GREEN}[ВЕРИФИКАЦИЯ ПРОЙДЕНА] Доступ разрешен.{Colors.RESET}")
                    else:
                        self.app.ui.print_error("Пароль не совпадает. Доступ заблокирован.")
                        
        except Exception as e:
            self.app.ui.print_error(f"Криптографический сбой: {e}")