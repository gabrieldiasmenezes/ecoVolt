from datetime import datetime
from database.database import establishment_chargers, fares
from modules.comercial.feature.pricing import calculate_fare
from utils.ui import header, error_option
from utils.system import reset_terminal
from utils.validation.common_validation import validate_int_value
from database.settings import ICON_TYPE

def estimate_time(kwh_to_charge, charger_power_kw):
    if charger_power_kw == 0:
        return 0
    return round((kwh_to_charge / charger_power_kw) * 60)

def select_charger(kwh_to_charge, charge_desc):
    available = [c for c in establishment_chargers if c['status'] == 'livre']
    if not available:
        print("\nNenhum carregador disponível no momento.")
        return None

    hour    = datetime.now().hour
    is_peak = fares['inicio_horario_pico'] <= hour < fares['fim_horario_pico']
    while True:
        reset_terminal()
        header("ESCOLHA O CARREGADOR")
        print(f"\n{charge_desc}")
        print(f"Energia a carregar: {kwh_to_charge} kWh\n")
        print("--- Carregadores Disponíveis ---\n")
    
        for i, c in enumerate(available):
            is_premium  = c.get('reservado_premium', False)
            fare, session_type, reason = calculate_fare(is_premium, is_peak, False)
            minutes     = estimate_time(kwh_to_charge, c['potencia_maxima'])
            total_price = round(kwh_to_charge * fare, 2)
            label_type  = ICON_TYPE['premium'] if is_premium else ICON_TYPE["comum"]

            print(f"[{i+1}] Carregador #{c['numero']}  {label_type}")
            print(f"Potência:  {c['potencia_maxima']} kW")
            print(f"Tarifa:R$ {fare:.2f}/kWh  ({reason})")
            print(f"Tempo est: ~{minutes} min")
            print(f" Total: R$ {total_price:.2f}")
            print()

        option = validate_int_value("Escolha um carregador (0 para voltar): ")
        if option == 0:
            return None
        if option < 1 or option > len(available):
            error_option()
            continue

        chosen= available[option - 1]
        is_premium = chosen.get('reservado_premium', False)
        fare, session_type, reason = calculate_fare(is_premium, is_peak, False)

        return {
            "charger":chosen,
            "tarifa":fare,
            "tipo_sessao": session_type,
            "motivo":reason,
            "total_price": round(kwh_to_charge * fare, 2),
            "minutes": estimate_time(kwh_to_charge, chosen['potencia_maxima'])
        }