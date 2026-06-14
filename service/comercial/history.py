from database.database import sessions, establishment_chargers
from utils.system import reset_terminal
from utils.ui import header

from utils.ui import error_option
from utils.validate.mutual_data import validate_option


def session_history(user):
    while True:
        reset_terminal()
        header("HISTÓRICO DE SESSÕES")

        user_sessions = [s for s in sessions if s['usuario_id'] == user['id']]
        finalizadas = [s for s in user_sessions if s['status'] == 'finalizada']
        ativas = [s for s in user_sessions if s['status'] == 'ativa']

        total_energia = sum(s['energia_kwh'] for s in finalizadas)
        total_gasto = sum(s['valor'] for s in finalizadas)
        co2_total = round(total_energia * 0.233, 2)

        print(f"\nSessões ativas:      {len(ativas)}")
        print(f"Sessões finalizadas: {len(finalizadas)}")
        print(f"Energia total:       {total_energia:.1f} kWh")
        print(f"Gasto total:         R$ {total_gasto:.2f}")
        print(f"CO₂ evitado:         {co2_total} kg")
        print()

        options = validate_option("""
1 - Ver Sessão Ativa
2 - Ver Sessões Finalizadas
0 - Voltar

Opção: """)

        match options:
            case 1:
                show_active(ativas)
            case 2:
                show_finished(finalizadas)
            case 0:
                break
            case _:
                error_option()


def show_active(ativas):
    reset_terminal()
    header("SESSÃO ATIVA")

    if not ativas:
        print("\nNenhuma sessão ativa no momento.")
        input("\nAperte Enter para voltar...")
        return

    s = ativas[0]
    charger = next((c for c in establishment_chargers if c['id'] == s['carregador_id']), None)
    tipo = "🔶 Premium" if s['tipo'] == 'premium' else "🔷 Comum"

    print(f"\nSessão #{s['id']}  {tipo}")
    print(f"Carregador: #{charger['numero'] if charger else s['carregador_id']}")
    print(f"Potência:   {s['potencia_kw']} kW")
    print(f"Tarifa:     R$ {s['tarifa_kwh']:.2f}/kWh")
    print(f"Início:     {s['inicio']}")
    print(f"Status:     EM ANDAMENTO")
    print("\n" + "=" * 40)
    input("\nAperte Enter para voltar...")


def show_finished(finalizadas):
    reset_terminal()
    header("SESSÕES FINALIZADAS")

    if not finalizadas:
        print("\nNenhuma sessão finalizada encontrada.")
        input("\nAperte Enter para voltar...")
        return

    for i, s in enumerate(finalizadas):
        tipo = "🔶 Premium" if s['tipo'] == 'premium' else "🔷 Comum"
        co2 = round(s['energia_kwh'] * 0.233, 2)
        print(f"\nSessão #{s['id']}  {tipo}")
        print(f"  Energia:  {s['energia_kwh']} kWh")
        print(f"  Valor:    R$ {s['valor']:.2f}")
        print(f"  CO₂:      {co2} kg evitados")
        print(f"  Início:   {s['inicio']}")
        print(f"  Fim:      {s['fim']}")
        if i < len(finalizadas) - 1:
            print("\n" + "-" * 40)

    print("\n" + "=" * 40)
    input("\nAperte Enter para voltar...")