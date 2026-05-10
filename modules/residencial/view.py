import time
from modules.common.database import residencial_data
from modules.residencial.logic import validate_car_model

def setup_residential_user(name):
    """
    Faz o onboarding residencial: nome, modelo do carro e ID do carregador.
    """
    print(f"\n[SETUP] Bem-vindo, {name}! Vamos configurar seu painel residencial.")
    usuario = name

    while True:
        car_model = input("Digite o modelo do seu carro elétrico (ex.: Tesla Model 3): ").strip()
        if validate_car_model(car_model):
            break
        print("[!] Modelo inválido. Escolha um modelo elétrico válido.")
    
    charger_id = input("Digite o ID do seu carregador residencial: ").strip()

    residencial_data.update({
        "usuario": usuario,
        "modelo_carro": car_model,
        "id_carregador": charger_id,
        "configurado": True
    })
    print("[SISTEMA] Setup concluído! Dados salvos.")

def display_home_economy(savings):
    """
    Exibe o dashboard de economia: mostra economia mensal simulada vs. gasolina.
    """
    print("\n[DASHBOARD DE ECONOMIA]")
    print(f"Economia mensal estimada: R$ {savings:.2f}")
    print("Comparado ao custo de gasolina para distâncias equivalentes.")

def display_home_hardware_details():
    """
    Exibe informações técnicas do carregador residencial (status simulado).
    """
    print("\n[INFORMAÇÕES TÉCNICAS DO CARREGADOR]")
    print(f"ID do Carregador: {residencial_data.get('id_carregador', 'N/A')}")
    print("Status: Online e Funcional")
    print("Potência Máxima: 11kW")
    print("Última Manutenção: Simulada - OK")

def start_home_charging_simulation(battery_data):
    """
    Simula recarga residencial: exibe telemetria e barra de progresso simplificada.
    Foco em nível de bateria, sem complexidade de pagamentos.
    """
    print("\n[RECARGA RESIDENCIAL]")
    print(f"Nível Atual: {battery_data['current']}% | Meta: {battery_data['target']}%")
    
    for percent in range(battery_data['current'], battery_data['target'] + 1, 5):
        bar = "#" * (percent // 10) + "-" * ((100 - percent) // 10)
        print(f"Progresso: [{bar}] {percent}% Concluído", end="\r")
        time.sleep(0.5)  
    print("\n[SISTEMA] Recarga concluída!")