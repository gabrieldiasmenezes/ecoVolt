
from modules.sessions.features.summary import session_summary
import modules.sessions.features.views as vi
from utils.system import reset_terminal
from utils.ui import error_option, header
from utils.validation.common_validation import validate_int_value


MENU="""
1 - Sessões Ativas
2 - Histórico de Sessões
3 - Detalhes de uma Sessão
0 - Voltar

Opção: """

def rechard_sessions(sessions):
    while True:
        reset_terminal()
        session_summary(sessions)
        header('SESSÕES DE RECARGA')

        options = validate_int_value(MENU)

        match options:
            case 1:
                vi.get_active_session(sessions)
            case 2:
                vi.get_session_history(sessions)
            case 3:
                vi.get_session_detail(sessions)
            case 0:
                break
            case _:
                error_option()