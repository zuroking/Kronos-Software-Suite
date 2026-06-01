import random
import string
print("Password Generator by Kronos English!")
print("I can help you generate a strong and secure password!")
print("Every password I generate will be unique, random and won't be contained in any dictionary!")
length = int(input("Enter the length of the password: "))
characters = string.ascii_letters + string.digits + string.punctuation
password = ''.join(random.choice(characters) for i in range(length))
print("Your generated password: ", password)
again = input("Generate another one? (yes/no): ")
while again.lower() == "yes":
    length = int(input("Enter the length of the password: "))
    password = ''.join(random.choice(characters) for i in range(length))
    print("Your generated password: ", password)
else:
    print("Thank you for using the Password Generator! Stay safe online!")

input("\nPress Enter to close...")