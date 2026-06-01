print("Text reserve by Kronos English")
print("I can help you reverse any text you want!")
text = input("Enter text: ")
print("Reserved text: " + text[::-1])
again = input("Generate another one? (yes/no): ")
while again.lower() == "yes":
    text = input("Enter text: ")
    print("Reserved text: " + text[::-1])
    again = input("Generate another one? (yes/no): ")
    if again.lower() != "yes":
        break