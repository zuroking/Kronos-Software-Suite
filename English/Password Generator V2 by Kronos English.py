import random
import string

# Алфавиты
ENGLISH = string.ascii_letters
DIGITS = string.digits
SYMBOLS = "!@#$%^&*()_+-=[]{}|;:,.<>?"
RUSSIAN = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
GREEK = "αβγδεζηθικλμνξοπρστυφχψωΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ"
ARABIC = "ابتثجحخدذرزسشصضطظعغفقكلمنهوي"
CHINESE = "的一是在不了有和人这中大为上个国我以要他时来用们生到作地于出就分对成会可主发年动同工也能下过子说产种面而方后多定行学法所民得经十三之进着等部度家电力里如水化高自二理起小物现实加量都两体制机当使点从业本去把性好应开它合还因由其些然前外天政四日那社义事平形相全表间样与关各重新线内数正心力理头场始边世定间入要"
JAPANESE = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんアイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン"

def build_charset(choices):
    charset = ""
    if "1" in choices:
        charset += ENGLISH
    if "2" in choices:
        charset += DIGITS
    if "3" in choices:
        charset += SYMBOLS
    if "4" in choices:
        charset += RUSSIAN
    if "5" in choices:
        charset += GREEK
    if "6" in choices:
        charset += ARABIC
    if "7" in choices:
        charset += CHINESE
    if "8" in choices:
        charset += JAPANESE
    return charset

def main():
    print("=" * 50)
    print("   PASSWORD GENERATOR V2 by Kronos English.")
    print("   Multi-alphabet password generator")
    print("   Supports English, Russian, Greek, Arabic, Chinese, Japanese characters and symbols.")
    print("   Create strong and unique passwords with ease!")
    print("   Kronos English does not store or share your generated passwords. Your security is our priority!")
    print("=" * 50)

    while True:
        print("\nChoose alphabets for the password:")
        print("1. English (abc...ABC)")
        print("2. Digits (0-9)")
        print("3. Symbols (!@#$...)")
        print("4. Русский (абв...АБВ)")
        print("5. Греческий (αβγ...ΑΒΓ)")
        print("6. Арабский (ابت...)")
        print("7. Китайский (的一是...)")
        print("8. Японский (あいう...アイウ)")
        print("9. Все сразу!")
        print("0. Выход")

        choice = input("\nChoose (you can choose multiple, e.g., 1234): ")

        if choice == "0":
            print("\nGoodbye! — Password Generator V2 by Kronos English.")
            input("\nPress Enter to close...")
            break

        if choice == "9":
            charset = ENGLISH + DIGITS + SYMBOLS + RUSSIAN + GREEK + ARABIC + CHINESE + JAPANESE
        else:
            charset = build_charset(choice)

        if not charset:
            print("❌ Choose at least one alphabet!")
            continue

        try:
            length = int(input("Password length: "))
            if length < 4:
                print("❌ Minimum length is 4 characters!")
                continue
        except ValueError:
            print("❌ Enter a number!")
            continue

        count = int(input("How many passwords to generate (1-10): "))
        count = max(1, min(10, count))

        print(f"\n{'=' * 50}")
        print(f"Generated passwords:")
        print(f"{'=' * 50}")
        for i in range(count):
            password = "".join(random.choice(charset) for _ in range(length))
            print(f"{i+1}. {password}")
        print(f"{'=' * 50}")

        again = input("\nGenerate more passwords? (yes/no): ")
        if again.lower() != "yes":
            print("\nGoodbye! — Password Generator V2 by Kronos English.")
            input("\nPress Enter to close...")
            break

main()