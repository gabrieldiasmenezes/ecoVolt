from database.database import fares
from utils.system import reset_terminal, load
from utils.ui import header, error_option
from utils.validate.mutual_data import validate_option

FARE_LABELS = {
    "base":                "Tarifa Base (comum)",
    "premium":             "Tarifa Premium",
    "horario_pico":        "Tarifa Horário de Pico",
    "cortesia_solar":      "Cortesia Solar",
    "inicio_horario_pico": "Início do Horário de Pico (hora)",
    "fim_horario_pico":    "Fim do Horário de Pico (hora)"
}


def tariff_manager():
    while True:
        reset_terminal()
        header("AJUSTE GLOBAL DE TARIFAS")

        print("\nTarifas atuais:\n")
        items = list(FARE_LABELS.items())
        for i, (key, label) in enumerate(items):
            unit = "h" if "horario" in key and key != "horario_pico" else "R$/kWh" if "inicio" not in key and "fim" not in key else "h"
            print(f"  [{i+1}] {label:<35} {fares[key]} {unit}")

        options = validate_option("\n1 - Alterar tarifa\n2 - Restaurar padrões\n0 - Voltar\n\nOpção: ")

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
    reset_terminal()
    header("ALTERAR TARIFA")

    for i, (key, label) in enumerate(items):
        print(f"  [{i+1}] {label}")

    option = validate_option("\nEscolha a tarifa (0 para voltar): ")
    if option == 0:
        return
    if option < 1 or option > len(items):
        error_option()
        return

    key, label = items[option - 1]
    current = fares[key]

    print(f"\nTarifa:  {label}")
    print(f"Atual:   {current}")

    try:
        if "horario" in key and "pico" not in key.replace("horario_pico", ""):
            new_val = int(input("Novo valor (hora 0–23): ").strip())
            if not 0 <= new_val <= 23:
                print("Hora inválida.")
                return
        else:
            new_val = float(input("Novo valor (R$/kWh): ").strip())
            if new_val < 0:
                print("Valor não pode ser negativo.")
                return
    except ValueError:
        print("Valor inválido.")
        input("\nAperte Enter para voltar...")
        return

    load(f"\nAplicando nova tarifa globalmente")
    fares[key] = round(new_val, 2)

    print(f"\n✅ {label} atualizada: {current} → {fares[key]}")
    print("Alteração aplicada a todos os estabelecimentos.")
    input("\nAperte Enter para voltar...")


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
    input("\nAperte Enter para voltar...")