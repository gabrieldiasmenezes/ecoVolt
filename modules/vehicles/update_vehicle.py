

from utils.system import reset_terminal
from utils.ui import enter, header
from utils.validation.common_validation import get_valid_input
from utils.validation.vehicle_validation import validate_battery_level


def update_battery(vehicle):

    reset_terminal()
    header("ATUALIZAR BATERIA")

    print(f"\nVeículo: {vehicle['modelo']}")
    print(f"Nível atual: {vehicle['nivel_bateria']}%")

    vehicle["nivel_bateria"] = int(
        get_valid_input(
            "Novo nível (%): ",
            validate_battery_level
        )
    )

    print(f"\n✅ Atualizado para {vehicle['nivel_bateria']}%")
    enter()