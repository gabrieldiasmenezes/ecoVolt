from database.database import POTENCIA_ESTABELECIMENTO
from utils.system import load, reset_terminal
from utils.ui import enter, error_option, header
from utils.validate.mutual_data import validate_option


LIMITE_SIMULACAO_KW = 25 

def status_demand(establishment, chargers):
    max_demand = establishment['demanda_maxima_kw']
    total_power = sum(c['potencia_atual'] for c in chargers)
    available = max_demand - total_power
    safety_margin = max_demand * 0.1

    premium_chargers = [c for c in chargers if c.get('reservado_premium')]
    common_chargers  = [c for c in chargers if not c.get('reservado_premium')]

    reset_terminal()
    header("CONTROLE DE DEMANDA — DLM")

    print(f"\nDemanda Máxima:   {max_demand} kW")
    print(f"Potência em Uso:  {total_power} kW")
    print(f"Disponível:       {available} kW")
    print(f"Margem Segurança: {safety_margin:.1f} kW")

    bar_fill = int((total_power / max_demand) * 20)
    bar = "█" * bar_fill + "░" * (20 - bar_fill)
    pct = int(total_power / max_demand * 100)
    print(f"\nCarga: [{bar}] {pct}%")

    if total_power >= max_demand - safety_margin:
        print("\n⚠  ALERTA: Demanda próxima do limite!")
        print("   DLM ativo — sessões comuns podem ser reduzidas.")

    print("\n--- Distribuição por Prioridade ---")

    print(f"\n🔶 PREMIUM")
    for c in premium_chargers:
        print(f"   Carregador #{c['numero']} → {c['potencia_atual']} kW (prioridade máxima garantida)")

    print(f"\n🔷 COMUM")
    for c in common_chargers:
        status_label = c['status'].upper()
        print(f"   Carregador #{c['numero']} → {c['potencia_atual']} kW  [{status_label}]")

    print("\n" + "=" * 40)
    enter()


def simulate_overload(chargers):
    premium_chargers = [c for c in chargers if c.get('reservado_premium')]
    common_chargers  = [c for c in chargers if not c.get('reservado_premium') and c['status'] != 'manutencao']

    simulated_power = len([c for c in chargers if c['status'] != 'manutencao']) * POTENCIA_ESTABELECIMENTO

    premium_power = len(premium_chargers) * POTENCIA_ESTABELECIMENTO
    remainder = LIMITE_SIMULACAO_KW - premium_power
    new_power_per_common = round(remainder / len(common_chargers), 1) if common_chargers else 0

    reset_terminal()
    header("SIMULAÇÃO DE SOBRECARGA — DLM")

    print(f"\nCenário: todos os carregadores ativos a plena carga")
    print(f"Potência simulada:  {simulated_power} kW")
    print(f"Limite contratado:  {LIMITE_SIMULACAO_KW} kW")
    print(f"\n⚠  SOBRECARGA DETECTADA! (+{simulated_power - LIMITE_SIMULACAO_KW} kW)")
    print("\nDLM iniciando redistribuição...\n")

    for c in premium_chargers:
        print(f"  ✅ Carregador #{c['numero']} (Premium) → {POTENCIA_ESTABELECIMENTO} kW mantidos")

    for c in common_chargers:
        reduction = round(POTENCIA_ESTABELECIMENTO - new_power_per_common, 1)
        print(f"  🔽 Carregador #{c['numero']} (Comum)   → reduzido para {new_power_per_common} kW  (−{reduction} kW)")

    new_total = round(premium_power + new_power_per_common * len(common_chargers), 1)
    print(f"\nNova carga total: {new_total} kW ✅")
    print("Sistema estabilizado dentro do limite.")
    print("\n" + "=" * 40)
    enter()

def demand_control(establishment, chargers):
    while True:
        reset_terminal()
        header('CONTROLE DE DEMANDA')
        options = validate_option("""
1 - Status de Demanda Atual
2 - Simular Sobrecarga (DLM)
0 - Voltar

Opção: """)

        match options:
            case 1:
                load("Analisando carga atual")
                status_demand(establishment, chargers)
            case 2:
                load("Simulando cenário de sobrecarga")
                simulate_overload(chargers)
            case 0:
                break
            case _:
                error_option()