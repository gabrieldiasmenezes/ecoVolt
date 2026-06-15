from database.database import fares
from database.settings import FARE_LABELS
from utils.system import reset_terminal, load
from utils.ui import enter, header, error_option
from utils.validation.common_validation import validate_float_value, validate_int_value



def tariff_manager():
    while True:
        reset_terminal()
        header("AJUSTE GLOBAL DE TARIFAS")

        print("\nTarifas atuais:\n")
        items = list(FARE_LABELS.items())
        for i, (key, label) in enumerate(items):
            unit = "h" if "horario" in key and key != "horario_pico" else "R$/kWh" if "inicio" not in key and "fim" not in key else "h"
            print(f"  [{i+1}] {label:<35} {fares[key]} {unit}")

        options = validate_int_value("\n1 - Alterar tarifa\n2 - Restaurar padrões\n0 - Voltar\n\nOpção: ")

        match options:
            case 1:
                edit_fare(items)
            case 2:
                restore_defaults()
            case 0:
                break
            case _:
                error_option()


def edit_fare(items):
    while True:
        reset_terminal()
        header("ALTERAR TARIFA")

        for i, (key, label) in enumerate(items):
            print(f"  [{i+1}] {label}")

        option = validate_int_value("\nEscolha a tarifa (0 para voltar): ")
        if option == 0:
            return
        if option < 1 or option > len(items):
            error_option()
            continue
        break

    key, label = items[option - 1]
    current = fares[key]

    print(f"\nTarifa:  {label}")
    print(f"Atual:   {current}")

    if "horario" in key and "pico" not in key.replace("horario_pico", ""):
        while True:
            new_val = validate_int_value("Novo valor (hora 0–23): ")
            if not 0 <= new_val <= 23:
                print("Hora inválida.")
                continue
            break
    else:
        new_val = validate_float_value("Novo valor (R$/kWh): ")

    load(f"\nAplicando nova tarifa globalmente")
    fares[key] = round(new_val, 2)

    print(f"\n✅ {label} atualizada: {current} → {fares[key]}")
    print("Alteração aplicada a todos os estabelecimentos.")
    enter()


def restore_defaults():
    defaults = {
        "base": 4.26,
        "premium": 5.11,
        "horario_pico": 4.90,
        "cortesia_solar": 1.00,
        "inicio_horario_pico": 18,
        "fim_horario_pico": 21
    }
    for key, val in defaults.items():
        fares[key] = val

    load("\nRestaurando tarifas padrão")
    print("\n✅ Todas as tarifas restauradas para os valores padrão.")
    enter()