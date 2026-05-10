from datetime import datetime

def get_fee_per_kwh():
    """
    Calcula o valor da tarifa baseando-se no horário atual do sistema.
    Aplica tarifação dinâmica (Horário de Pico vs. Horário Normal).
    """
    current_hour = datetime.now().hour
    if 18 <= current_hour <= 21:
        print(f"\n[!] Horário de Pico detectado ({current_hour}h). Tarifa: R$ 2,10/kWh")
        fee = 2.10
    else:
        print(f"\n[!] Horário Normal detectado ({current_hour}h). Tarifa: R$ 1,60/kWh")
        fee = 1.60
    return fee



