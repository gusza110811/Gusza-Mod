import os

windows = (os.name == "nt")

def clear():
    "Clear terminal"
    if windows:
        os.system("cls")
    else:
        os.system("clear")
def cls():"Equivalent to clear()";clear()


