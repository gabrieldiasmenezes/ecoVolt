from database.database import users, vehicles,sessions,residencial_charger

def get_user_name(user_id):
    for u in users:
        if u['id'] == user_id:
            return u['nome']
    return "Desconhecido"


def get_vehicle_model(vehicle_id):
    for v in vehicles:
        if v['id'] == vehicle_id:
            return v['modelo']
    return "Desconhecido"

def get_user_vehicle(user):
    for v in vehicles:
        if v['usuario_id'] == user['id']:
            return v
    return None


def get_user_active_session(user):
    for s in sessions:
        if s['usuario_id'] == user['id'] and s['status'] == 'ativa':
            return s
    return None

def get_user_charger(user):
    for c in residencial_charger:
        if c['usuario_id'] == user['id']:
            return c
    return None

