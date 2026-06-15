from database.database import vehicles
from database.settings import KNOWN_MODELS

from utils.system import reset_terminal, load
from utils.ui import header, enter, error_option
from utils.helpers import get_user_vehicle
from utils.validation.common_validation import validate_int_value, get_valid_input
from utils.validation.vehicle_validation import (
    validate_plate,
    validate_battery_kwh,
    validate_battery_level,
    validate_vehicle_text
)



def get_vehicle_model():
    while True:
        print("\nModelos disponíveis:\n")

        for key, car in KNOWN_MODELS.items():
            kwh = (
                f"{car['bateria_kwh']} kWh"
                if car['bateria_kwh']
                else "informar manualmente"
            )
            print(f"  [{key}] {car['modelo']} ({kwh})")
        option = validate_int_value("\nEscolha o modelo (0 para voltar): ")

        if option == 0:
            return

        if option not in KNOWN_MODELS:
            error_option()
            continue
        break
    return option
def register_vehicle(user):

    reset_terminal()
    header("CADASTRAR VEÍCULO")


    if get_user_vehicle(user['id']):
        print("\nVocê já possui um veículo cadastrado.")
        enter()
        return
    
    model= get_vehicle_model()

    chosen = KNOWN_MODELS[model]

    fabricante = chosen["fabricante"]
    modelo = chosen["modelo"]

    if model == 7:
        fabricante = get_valid_input("Fabricante: ",validate_vehicle_text)
        modelo = get_valid_input("Modelo: ",validate_vehicle_text)

    if chosen["bateria_kwh"]:
        bateria_kwh = chosen["bateria_kwh"]
    else:
        bateria_kwh = float(
            get_valid_input(
                "Capacidade da bateria (kWh): ",
                validate_battery_kwh
            )
        )

    plate = get_valid_input(
        "Placa do veículo: ",
        validate_plate
    ).upper()

    nivel = int(
        get_valid_input(
            "Nível de bateria (%): ",
            validate_battery_level
        )
    )

    new_vehicle = {
        "id": (max(v["id"] for v in vehicles) + 1) if vehicles else 1,
        "usuario_id": user["id"],
        "modelo": modelo,
        "fabricante": fabricante,
        "placa": plate,
        "bateria_kwh": bateria_kwh,
        "nivel_bateria": nivel
    }

    vehicles.append(new_vehicle)

    load("Cadastrando veículo")

    reset_terminal()
    header("VEÍCULO CADASTRADO")

    print(f"\n✅ {modelo} cadastrado com sucesso!")
    print(f"Placa:   {plate}")
    print(f"Bateria: {nivel}% ({bateria_kwh} kWh)")

    enter()