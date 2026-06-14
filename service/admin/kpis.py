from database.database import establishments, establishment_chargers, residencial_charger, sessions, users
from utils.system import reset_terminal
from utils.ui import header


def kpis_dashboard():
    reset_terminal()
    header("KPIs — DISPONIBILIDADE DA REDE")

    # Carregadores
    all_chargers = establishment_chargers + residencial_charger
    total = len(all_chargers)
    online = len([c for c in all_chargers if c['status'] != 'manutencao'])
    in_use = len([c for c in all_chargers if c['status'] == 'em_uso'])
    free = len([c for c in all_chargers if c['status'] == 'livre'])
    maintenance = len([c for c in all_chargers if c['status'] == 'manutencao'])
    availability_rate = round(online / total * 100, 1) if total else 0

    # Sessões
    active_sessions = [s for s in sessions if s['status'] == 'ativa']
    finished_sessions = [s for s in sessions if s['status'] == 'finalizada']
    total_revenue = sum(s['valor'] for s in sessions)
    total_energy = sum(s['energia_kwh'] for s in sessions)
    total_power_now = sum(s['potencia_kw'] for s in active_sessions)

    # Usuários
    active_users = len([u for u in users if u['status'] == 'ativo'])
    commercial_users = len([u for u in users if u.get('perfil') == 'cliente_comercial'])
    residential_users = len([u for u in users if u.get('perfil') == 'cliente_residencial'])

    header("SAÚDE DA FROTA")

    bar_fill = int((availability_rate / 100) * 20)
    bar = "█" * bar_fill + "░" * (20 - bar_fill)
    health = "✅ BOA" if availability_rate >= 75 else "⚠ AVISO" if availability_rate >= 50 else "❌ CRÍTICA"

    print(f"\nDisponibilidade:  [{bar}] {availability_rate}%  {health}")
    print(f"\nTotal carregadores:  {total}")
    print(f"  Online:            {online}")
    print(f"  Em uso:            {in_use}")
    print(f"  Livres:            {free}")
    print(f"  Manutenção:        {maintenance}")

    header("OPERAÇÃO EM TEMPO REAL")
    print(f"\nSessões ativas:      {len(active_sessions)}")
    print(f"Potência em uso:     {total_power_now} kW")
    print(f"Sessões finalizadas: {len(finished_sessions)}")
    print(f"Energia distribuída: {total_energy:.1f} kWh")
    print(f"Faturamento total:   R$ {total_revenue:.2f}")

    header("USUÁRIOS")

    print(f"\nUsuários ativos:     {active_users}")
    print(f"  Comerciais:        {commercial_users}")
    print(f"  Residenciais:      {residential_users}")

    header("ESTABELECIMENTOS")
    
    for est in establishments:
        chargers_est = [c for c in establishment_chargers if c['estabelecimento_id'] == est['id']]
        in_use_est = len([c for c in chargers_est if c['status'] == 'em_uso'])
        print(f"\n  {est['nome']}")
        print(f"  Carregadores: {len(chargers_est)}  |  Em uso: {in_use_est}")
        print(f"  Faturamento:  R$ {est['faturamento']:.2f}")
        print(f"  Energia:      {est['energia_total_distribuida_kwh']} kWh")

    print("\n" + "=" * 40)
    input("\nAperte Enter para voltar...")