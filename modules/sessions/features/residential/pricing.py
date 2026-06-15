from datetime import datetime
from database.database import fares


def calculate_price(chosen_mode, power_kw, vehicle, soc_target):
    kwh_to_charge = round((soc_target - vehicle['nivel_bateria']) / 100 * vehicle['bateria_kwh'], 2)
    minutes = round(kwh_to_charge / power_kw * 60)

    hora = datetime.now().hour
    is_peak = fares['inicio_horario_pico'] <= hora < fares['fim_horario_pico']
    is_off_peak = hora >= 22 or hora < 6

    if chosen_mode['tarifa_override'] is not None:
        tarifa = chosen_mode['tarifa_override']
        motivo = chosen_mode['nome']

    elif is_off_peak:
        tarifa = round(fares['base'] * 0.7, 2)
        motivo = "Tarifa reduzida (madrugada)"

    elif is_peak:
        tarifa = fares['horario_pico']
        motivo = "Horário de pico"

    else:
        tarifa = fares['base']
        motivo = "Tarifa base"

    total = round(kwh_to_charge * tarifa, 2)

    return {
        "kwh": kwh_to_charge,
        "minutes": minutes,
        "tarifa": tarifa,
        "motivo": motivo,
        "total": total
    }