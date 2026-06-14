from utils.helpers import get_user_name, get_vehicle_model
from utils.system import reset_terminal
from utils.ui import enter, header


def get_active_session(sessions):
    active_sessions = [s for s in sessions if s.get('status') == 'ativa']

    reset_terminal()
    header("SESSÕES ATIVAS")

    if not active_sessions:
        print("\nNenhuma sessão ativa no momento.")
    else:
        print()
        for i, session in enumerate(active_sessions):
            tipo = 'Premium' if session['tipo'] == 'premium' else 'Comum'
            print(f"ID: {session['id']}")
            print(f"Cliente:    {get_user_name(session['usuario_id'])}")
            print(f"Veículo:    {get_vehicle_model(session['veiculo_id'])}")
            print(f"Carregador: {session['carregador_id']}")
            print(f"Tipo:       {tipo}")
            print(f"Potência:   {session['potencia_kw']} kW")

            if i < len(active_sessions) - 1:
                print("\n" + "-" * 40 + "\n")

    print("\n" + "=" * 40)
    print(f"Total de Sessões Ativas: {len(active_sessions)}")
    enter()


def get_session_history(sessions):
    finished = [s for s in sessions if s.get('status') == 'finalizada']

    reset_terminal()
    header("HISTÓRICO DE SESSÕES")

    if not finished:
        print("\nNenhuma sessão finalizada encontrada.")
    else:
        for i, session in enumerate(finished):
            print(f"\nSessão #{session['id']}\n")
            print(f"Cliente:\n{get_user_name(session['usuario_id'])}\n")
            print(f"Veículo:\n{get_vehicle_model(session['veiculo_id'])}\n")
            print(f"Energia:\n{session['energia_kwh']} kWh\n")
            print(f"Valor:\nR$ {session['valor']:.2f}\n")
            print(f"Início:\n{session['inicio']}\n")
            print(f"Fim:\n{session['fim']}")

            if i < len(finished) - 1:
                print("\n" + "-" * 40)

    print("\n" + "=" * 40)
    enter()


def get_session_detail(sessions):
    reset_terminal()
    header("DETALHES DE UMA SESSÃO")


    all_ids = [s['id'] for s in sessions]
    print(f"\nIDs disponíveis: {all_ids}")

    try:
        session_id = int(input("\nDigite o ID da sessão: ").strip())
    except ValueError:
        print("\nID inválido.")
        input("Aperte Enter para voltar...")
        return

    session = next((s for s in sessions if s['id'] == session_id), None)

    if not session:
        print(f"\nSessão #{session_id} não encontrada.")
        enter()
        return

    tipo = 'Premium' if session['tipo'] == 'premium' else 'Comum'
    status_label = 'ATIVA' if session['status'] == 'ativa' else 'FINALIZADA'

    print(f"\nID: {session['id']}\n")
    print(f"Cliente:    {get_user_name(session['usuario_id'])}")
    print(f"Veículo:    {get_vehicle_model(session['veiculo_id'])}")
    print(f"Carregador: {session['carregador_id']}")
    print(f"\nTipo:       {tipo}")
    print(f"\nPotência:\n{session['potencia_kw']} kW")
    print(f"\nEnergia:\n{session['energia_kwh']} kWh")
    print(f"\nTarifa:\nR$ {session['tarifa_kwh']:.2f}/kWh")
    print(f"\nValor:\nR$ {session['valor']:.2f}")
    print(f"\nInício:\n{session['inicio']}")
    print(f"\nFim:\n{session['fim'] if session['fim'] else '—'}")
    print(f"\nStatus:\n{status_label}")
    print("\n" + "=" * 40)
    enter()