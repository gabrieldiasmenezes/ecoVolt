from database.settings import KWH_PER_100KM
from utils.system import choose_soc_target, reset_terminal
from utils.ui import header, error_option
from utils.validation.common_validation import validate_int_value,validate_float_value




def _charge_by_battery(vehicle):
    battery_current_pct = vehicle['nivel_bateria']
    battery_kwh = vehicle['bateria_kwh']
    target_pct = choose_soc_target(vehicle)
    

    kwh_to_charge = round((target_pct - battery_current_pct) / 100 * battery_kwh, 2)
    autonomy_after = round(target_pct / 100 * battery_kwh / KWH_PER_100KM * 100)
    description = f"Bateria: {battery_current_pct}% → {target_pct}%  (~{autonomy_after} km de autonomia)"

    return kwh_to_charge, description


def _charge_by_distance(vehicle):
    battery_current_pct = vehicle['nivel_bateria']
    battery_kwh = vehicle['bateria_kwh']
    battery_available = round(battery_kwh * battery_current_pct / 100, 2)
    autonomy_now = round(battery_available / KWH_PER_100KM * 100)

    print(f"\nAutonomia atual: ~{autonomy_now} km\n")

    while True:
        extra_km = validate_float_value("Quantos km extras deseja garantir?: ")

        kwh_needed_extra = round(extra_km * KWH_PER_100KM / 100, 2)
        kwh_total_needed = round(battery_available + kwh_needed_extra, 2)
        target_pct = round(kwh_total_needed / battery_kwh * 100)

        if target_pct > 100:
            max_extra = round((battery_kwh - battery_available) / KWH_PER_100KM * 100)
            print(f"Com a bateria cheia você consegue no máximo +{max_extra} km extras.")
            print(f"Informe um valor até {max_extra} km.")
            continue
        break


    kwh_to_charge = kwh_needed_extra
    autonomy_after = autonomy_now + int(extra_km)
    descricao = f"Distância extra: +{int(extra_km)} km  (autonomia total: ~{autonomy_after} km)"

    return kwh_to_charge, descricao


MENU="""
1 - Por nível de bateria desejado (%)
2 - Por distância desejada (km)
0 - Voltar

Opção: """

def choose_charge_amount(vehicle):
    while True:
        reset_terminal()
        header("QUANTO DESEJA CARREGAR?")

        battery_current_pct = vehicle['nivel_bateria']
        battery_kwh = vehicle['bateria_kwh']
        battery_available = round(battery_kwh * battery_current_pct / 100, 2)
        autonomy_now = round(battery_available / KWH_PER_100KM * 100)

        print(f"\nVeículo: {vehicle['modelo']}")
        print(f"Bateria atual: {battery_current_pct}%  ({battery_available} kWh)")
        print(f"Autonomia atual: ~{autonomy_now} km\n")

        option = validate_int_value(MENU)

        if option == 0:
            return None, None

        if option == 1:
            return _charge_by_battery(vehicle)
        elif option == 2:
            return _charge_by_distance(vehicle)
        else:
            error_option()
            continue
