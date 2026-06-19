from menu import menu

def hello():
    return "Hello!"

def goodbye():
    return "Goodbye!"

result = menu(hello=hello, goodbye=goodbye)
print(result)

