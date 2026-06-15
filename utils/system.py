import os
import time

from utils.validation.common_validation import validate_int_value

def reset_terminal():
    os.system("cls")

def load(text):
    print(text, end="")

    for _ in range(0):
        time.sleep(0.5)
        print(".", end="", flush=True)

    print()

def choose_soc_target(vehicle):
    current = vehicle['nivel_bateria']
    min_target = current + 10

    print(f"\nNível atual:  {current}%")
    print(f"Mínimo permitido: {min_target}%  (mínimo 10% acima do atual)")
    print(f"Máximo permitido: 100%\n")

    while True:
        target = validate_int_value(
            f"Meta de carga ({min_target}–100)%: "
        )

        if target < min_target:
            print(f"Mínimo {min_target}% (10% acima do atual).")
            continue

        if target > 100:
            print("Não pode ultrapassar 100%.")
            continue

        return target