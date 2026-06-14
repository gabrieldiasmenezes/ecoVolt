from service.sessions.session_queries import get_active_session, get_session_detail, get_session_history
from utils.system import reset_terminal
from utils.ui import error_option, header
from utils.validate.mutual_data import validate_option


def session_summary(sessions):
    active = [s for s in sessions if s.get('status') == 'ativa']
    finished = [s for s in sessions if s.get('status') == 'finalizada']
    energy_in_use = sum(s.get('potencia_kw', 0) for s in active)
    revenue = sum(s.get('valor', 0) for s in sessions)

    print("=" * 40)
    print("        CENTRO DE SESSÕES")
    print("=" * 40)
    print(f"\nSessões Ativas:      {len(active)}")
    print(f"Sessões Finalizadas: {len(finished)}")
    print(f"\nEnergia em Uso:      {energy_in_use} kW")
    print(f"Receita Gerada:      R$ {revenue:.2f}")
    print("\n" + "=" * 40)


def rechard_sessions(sessions):
    while True:
        reset_terminal()
        session_summary(sessions)
        header('SESSÕES DE RECARGA')

        options = validate_option("""
1 - Sessões Ativas
2 - Histórico de Sessões
3 - Detalhes de uma Sessão
0 - Voltar

Opção: """)

        match options:
            case 1:
                get_active_session(sessions)
            case 2:
                get_session_history(sessions)
            case 3:
                get_session_detail(sessions)
            case 0:
                break
            case _:
                error_option()