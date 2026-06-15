from database.settings import ESTABLISHMENT_POWER,LIMIT_SIMULATION
from utils.helpers import active_chargers, current_power_usage, split_chargers
from utils.system import load, reset_terminal
from utils.ui import (enter,error_option,header,progress_bar,)
from utils.validation.common_validation import validate_int_value

# ==========================
# STATUS DE DEMANDA
# ==========================

def status_demand(establishment, chargers):

    max_demand = establishment["demanda_maxima_kw"]
    power_in_use = current_power_usage(chargers)

    available_power = max_demand - power_in_use
    safety_margin = max_demand * 0.10

    premium_chargers, common_chargers = split_chargers(chargers)

    bar, pct = progress_bar(power_in_use,max_demand)

    reset_terminal()
    header("CONTROLE DE DEMANDA — DLM")

    print(f"\nDemanda Máxima:   {max_demand} kW")
    print(f"Potência em Uso:  {power_in_use} kW")
    print(f"Disponível:       {available_power} kW")
    print(f"Margem Segurança: {safety_margin:.1f} kW")

    print(f"\nCarga: [{bar}] {pct}%")

    if power_in_use >= max_demand - safety_margin:
        print("\n⚠ ALERTA: Demanda próxima do limite!")
        print("DLM ativo — sessões comuns podem ser reduzidas.")

    print("\n--- DISTRIBUIÇÃO POR PRIORIDADE ---")

    print("\n🔶 PREMIUM")
    for charger in premium_chargers:
        print(
            f"Carregador #{charger['numero']} "
            f"→ {charger['potencia_atual']} kW"
        )

    print("\n🔷 COMUM")
    for charger in common_chargers:
        print(
            f"Carregador #{charger['numero']} "
            f"→ {charger['potencia_atual']} kW "
            f"[{charger['status'].upper()}]"
        )

    enter()


# ==========================
# SIMULAÇÃO DE SOBRECARGA
# ==========================

def simulate_overload(chargers):

    premium_chargers, common_chargers = split_chargers(chargers)

    common_chargers = [
        charger
        for charger in common_chargers
        if charger["status"] != "manutencao"
    ]

    working_chargers = active_chargers(chargers)

    simulated_power = (len(working_chargers)* ESTABLISHMENT_POWER)

    premium_power = (len(premium_chargers)* ESTABLISHMENT_POWER)

    available_for_common = (LIMIT_SIMULATION- premium_power)

    power_per_common = (
        round(available_for_common/ len(common_chargers),1)
        if common_chargers
        else 0
    )

    reset_terminal()
    header("SIMULAÇÃO DE SOBRECARGA — DLM")

    print("\nCenário: todos os carregadores ativos")

    print(
        f"\nPotência simulada: "
        f"{simulated_power} kW"
    )

    print(
        f"Limite contratado: "
        f"{LIMIT_SIMULATION} kW"
    )

    overload = (simulated_power- LIMIT_SIMULATION)

    print(
        f"\n⚠ SOBRECARGA DETECTADA! "
        f"(+{overload} kW)"
    )

    print("\nDLM iniciando redistribuição...\n")

    for charger in premium_chargers:
        print(
            f"✅ Carregador #{charger['numero']} "
            f"(Premium) → "
            f"{ESTABLISHMENT_POWER} kW mantidos"
        )

    for charger in common_chargers:

        reduction = round(ESTABLISHMENT_POWER- power_per_common,1)

        print(
            f"🔽 Carregador #{charger['numero']} "
            f"(Comum) → "
            f"{power_per_common} kW "
            f"(−{reduction} kW)"
        )

    new_total = round(
        premium_power
        + power_per_common * len(common_chargers),
        1
    )

    print(f"\nNova carga total: {new_total} kW ✅")
    print("Sistema estabilizado dentro do limite.")

    enter()


# ==========================
# MENU
# ==========================

MENU="""
1 - Status de Demanda Atual
2 - Simular Sobrecarga (DLM)
0 - Voltar

Opção: """
def demand_control(establishment, chargers):

    while True:
        reset_terminal()
        header("CONTROLE DE DEMANDA")
        option = validate_int_value(MENU)
        match option:
            case 1:
                load("Analisando carga atual")
                status_demand(
                    establishment,
                    chargers
                )
            case 2:
                load("Simulando cenário de sobrecarga")
                simulate_overload(chargers)
            case 0:
                break

            case _:
                error_option()