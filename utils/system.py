import os
import time

def reset_terminal():
    os.system("cls")

def load(text):
    print(text, end="")

    for _ in range(0):
        time.sleep(0.5)
        print(".", end="", flush=True)

    print()