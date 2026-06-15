

from modules.vehicles.register_vehicle import register_vehicle
from modules.vehicles.update_vehicle import update_battery
from utils.helpers import get_user_vehicle
from utils.system import reset_terminal
from utils.ui import error_option, header
from utils.validation.common_validation import validate_int_value

MENU="""
1 - Cadastrar Veículo
2 - Atualizar Nível de Bateria
0 - Voltar

Opção: """ 

REGISTER="""
1 - Cadastrar Veículo
0 - Voltar

Opção: """

def vehicle_manager(user):

    while True:
        reset_terminal()
        header("MEUS VEÍCULOS")

        vehicle = get_user_vehicle(user['id'])

        if vehicle:
            print(f"\nVeículo cadastrado:")
            print(f"  Modelo:   {vehicle['modelo']}")
            print(f"  Placa:    {vehicle['placa']}")
            print(f"  Bateria:  {vehicle['nivel_bateria']}% ({vehicle['bateria_kwh']} kWh)")
            print()

        option = validate_int_value(MENU if vehicle else REGISTER)

        match option:
            case 1:
                register_vehicle(user)

            case 2 if vehicle:
                update_battery(vehicle)

            case 0:
                break

            case _:
                error_option()
                continue

def prompt_register_if_no_vehicle(user):
    """Chamado quando o usuário tenta iniciar recarga sem veículo."""
    reset_terminal()
    header("VEÍCULO NÃO ENCONTRADO")

    print("\nVocê não possui um veículo cadastrado.")
    print("É necessário cadastrar um veículo para iniciar uma recarga.\n")

    option = validate_int_value("1 - Cadastrar agora\n0 - Voltar\n\nOpção: ")
    if option == 1:
        register_vehicle(user)