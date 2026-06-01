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
    print("   Генератор паролей от Kronos Russian!")
    print("   Генерируйте надежные пароли для всех ваших аккаунтов.")
    print("   Поддерживает Английский, Русский, греческий, арабский, китайский, японский символы и знаки.")
    print("   Генерируй надёжные пароли с Kronos Russian!")
    print("   Kronos Russian не хранит ваши сгенерированные пароли и не имеет доступа к ним. Ваша кибербезопасность — наш приоритет!")
    print("=" * 50)

    while True:
        print("\nВыбери алфавиты для пароля:")
        print("1. Английский (abc...ABC)")
        print("2. Цифры (0-9)")
        print("3. Символы (!@#$...)")
        print("4. Русский (абв...АБВ)")
        print("5. Греческий (αβγ...ΑΒΓ)")
        print("6. Арабский (ابت...)")
        print("7. Китайский (的一是...)")
        print("8. Японский (あいう...アイウ)")
        print("9. Все сразу!")
        print("0. Выход")

        choice = input("\nВыбери (можно несколько, например 1234): ")

        if choice == "0":
            print("\nДо свидания! — Генератор паролей V2 от Kronos Russian.")
            input("\nНажми Enter для закрытия...")
            break

        if choice == "9":
            charset = ENGLISH + DIGITS + SYMBOLS + RUSSIAN + GREEK + ARABIC + CHINESE + JAPANESE
        else:
            charset = build_charset(choice)

        if not charset:
            print("❌ Выбери хотя бы один алфавит!")
            continue

        try:
            length = int(input("Длина пароля: "))
            if length < 4:
                print("❌ Минимальная длина — 4 символа!")
                continue
        except ValueError:
            print("❌ Введи число!")
            continue

        try:
            count = int(input("Сколько паролей сгенерировать (1-10): "))
            count = max(1, min(10, count))
        except ValueError:
            print("❌ Введи число!")
            continue

        print(f"\n{'=' * 50}")
        print(f"Сгенерированные пароли:")
        print(f"{'=' * 50}")
        for i in range(count):
            password = "".join(random.choice(charset) for _ in range(length))
            print(f"{i+1}. {password}")
        print(f"{'=' * 50}")

        again = input("\nСгенерировать ещё? (да/нет): ")
        if again.lower() != "да":
            print("\nДо свидания! — Генератор паролей V2 от Kronos Russian.")
            input("\nНажми Enter для закрытия...")
            break

main()