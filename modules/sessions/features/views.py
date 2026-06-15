from utils.system import reset_terminal
from utils.ui import enter, footer, header, session_card
from utils.validation.common_validation import validate_int_value


def get_active_session(sessions):

    active_sessions = [s for s in sessions if s.get('status') == 'ativa']

    reset_terminal()
    header("SESSÕES ATIVAS")

    if not active_sessions:
        print("\nNenhuma sessão ativa no momento.")
    else:
        for i, session in enumerate(active_sessions):
            session_card(session, mode="list")

            if i < len(active_sessions) - 1:
                print("\n" + "-" * 40)

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
            session_card(session, mode="detail")

            if i < len(finished) - 1:
                print("\n" + "-" * 40)

    footer()  

def get_session_detail(sessions):

    reset_terminal()
    header("DETALHES DE UMA SESSÃO")

    all_ids = [s.get('id') for s in sessions]
    print(f"\nIDs disponíveis: {all_ids}")
    while True:
        session_id= validate_int_value("\nDigite o ID da sessão: ")

        session = next((s for s in sessions if s.get('id') == session_id), None)

        if not session:
            print(f"\nSessão #{session_id} não encontrada.")
            continue

        session_card(session, mode="detail")
        footer()  
        break