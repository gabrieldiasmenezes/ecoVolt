from database.database import vehicles
from utils.helpers import get_user_vehicle
from utils.system import reset_terminal, load
from utils.ui import enter, header, error_option
from utils.validate.mutual_data import validate_option
import utils.validate.vehicle_data as ve

KNOWN_MODELS = {
    1: {"fabricante": "BYD",     "modelo": "BYD Dolphin",    "bateria_kwh": 44},
    2: {"fabricante": "BYD",     "modelo": "BYD Seal",       "bateria_kwh": 82},
    3: {"fabricante": "Volvo",   "modelo": "Volvo EX30",     "bateria_kwh": 51},
    4: {"fabricante": "Tesla",   "modelo": "Tesla Model 3",  "bateria_kwh": 60},
    5: {"fabricante": "Tesla",   "modelo": "Tesla Model Y",  "bateria_kwh": 75},
    6: {"fabricante": "Fiat",    "modelo": "Fiat Fastback",  "bateria_kwh": 54},
    7: {"fabricante": "Outro",   "modelo": "Outro",          "bateria_kwh": None},
}



def vehicle_manager(user):
    while True:
        reset_terminal()
        header("MEUS VEÍCULOS")

        vehicle = get_user_vehicle(user)

        if vehicle:
            print(f"\nVeículo cadastrado:")
            print(f"  Modelo:   {vehicle['modelo']}")
            print(f"  Placa:    {vehicle['placa']}")
            print(f"  Bateria:  {vehicle['nivel_bateria']}%  ({vehicle['bateria_kwh']} kWh)")
            print()

        options = validate_option("""
1 - Cadastrar Veículo
2 - Atualizar Nível de Bateria
0 - Voltar

Opção: """ if vehicle else """
1 - Cadastrar Veículo
0 - Voltar

Opção: """)

        match options:
            case 1:
                register_vehicle(user)
            case 2 if vehicle:
                update_battery(vehicle)
            case 0:
                break
            case _:
                error_option()


def register_vehicle(user):
    reset_terminal()
    header("CADASTRAR VEÍCULO")

    existing = get_user_vehicle(user)
    if existing:
        print(f"\nVocê já possui um veículo cadastrado ({existing['modelo']}).")
        print("Remova-o antes de cadastrar outro.")
        enter()
        return

    print("\nModelos disponíveis:\n")
    for key, car in KNOWN_MODELS.items():
        kwh = f"{car['bateria_kwh']} kWh" if car['bateria_kwh'] else "informar manualmente"
        print(f"  [{key}] {car['modelo']}  ({kwh})")

    option = validate_option("\nEscolha o modelo (0 para voltar): ")
    if option == 0:
        return
    if option not in KNOWN_MODELS:
        error_option()
        return

    chosen = KNOWN_MODELS[option]
    fabricante = chosen['fabricante']
    modelo = chosen['modelo']

    # Modelo personalizado
    if option == 7:
        fabricante = input("Fabricante: ").strip()
        modelo = input("Modelo: ").strip()
        if not fabricante or not modelo:
            print("Fabricante e modelo são obrigatórios.")
            enter()
            return

    # Capacidade da bateria
    if chosen['bateria_kwh']:
        bateria_kwh = chosen['bateria_kwh']
    else:
        while True:
            raw = input("Capacidade da bateria (kWh): ").strip()
            if ve.validate_battery_kwh(raw):
                bateria_kwh = float(raw)
                break

    # Placa
    while True:
        plate = input("Placa do veículo (ex: ABC1D23): ").strip()
        if ve.validate_plate(plate):
            break

    # Nível de bateria atual
    while True:
        raw = input("Nível de bateria atual (%): ").strip()
        if ve.validate_battery_level(raw):
            nivel = int(raw)
            break

    new_vehicle = {
        "id": max(v['id'] for v in vehicles) + 1 if vehicles else 1,
        "usuario_id": user['id'],
        "modelo": modelo,
        "fabricante": fabricante,
        "placa": plate.upper(),
        "bateria_kwh": bateria_kwh,
        "nivel_bateria": nivel
    }

    vehicles.append(new_vehicle)
    load("Cadastrando veículo")

    reset_terminal()
    header("VEÍCULO CADASTRADO")
    print(f"\n✅ {modelo} cadastrado com sucesso!")
    print(f"\nPlaca:    {new_vehicle['placa']}")
    print(f"Bateria:  {nivel}%  ({bateria_kwh} kWh)")
    print("\n" + "=" * 40)
    enter()


def update_battery(vehicle):
    reset_terminal()
    header("ATUALIZAR BATERIA")

    print(f"\nVeículo: {vehicle['modelo']}")
    print(f"Nível atual: {vehicle['nivel_bateria']}%\n")

    while True:
        raw = input("Novo nível de bateria (%): ").strip()
        if ve.validate_battery_level(raw):
            vehicle['nivel_bateria'] = int(raw)
            break

    print(f"\n✅ Bateria atualizada para {vehicle['nivel_bateria']}%")
    enter()


def prompt_register_if_no_vehicle(user):
    """Chamado quando o usuário tenta iniciar recarga sem veículo."""
    reset_terminal()
    header("VEÍCULO NÃO ENCONTRADO")

    print("\nVocê não possui um veículo cadastrado.")
    print("É necessário cadastrar um veículo para iniciar uma recarga.\n")

    option = validate_option("1 - Cadastrar agora\n0 - Voltar\n\nOpção: ")
    if option == 1:
        register_vehicle(user)