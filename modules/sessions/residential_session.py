

from modules.sessions.features.residential.end_session import end_residential_session
from modules.sessions.features.residential.start_session import start_residential_session


def residential_session(user, action):
    if action == 'iniciar':
        start_residential_session(user)
    elif action == 'encerrar':
        end_residential_session(user)


