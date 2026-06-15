import database.database as db


# ==========================
# BUSCAS GENÉRICAS
# ==========================

def find_item_by_field(items, field_value, field_name):
    for item in items:
        if item.get(field_name) == field_value:
            return item
    return {}


def find_list_item_by_field(items, field_value, field_name):
    result = []

    for item in items:
        if item.get(field_name) == field_value:
            result.append(item)

    return result


def field_exists(field, value):
    return any(
        user.get(field) == value
        for user in db.users
    )


# ==========================
# USUÁRIOS E VEÍCULOS
# ==========================

def get_user_name(user_id):
    user = find_item_by_field(
        db.users,
        user_id,
        "id"
    )

    return user.get(
        "nome",
        "Usuário não encontrado"
    )


def get_vehicle_model(vehicle_id):
    vehicle = find_item_by_field(
        db.vehicles,
        vehicle_id,
        "id"
    )

    return vehicle.get(
        "modelo",
        "Veículo não encontrado"
    )

def get_user_vehicle(user_id):
    vehicle= find_item_by_field(
        db.vehicles,
        user_id,
        "usuario_id"
    )
    return vehicle

def get_user_charger(user_id):
    charger= find_item_by_field(
        db.residencial_charger,
        user_id,
        "usuario_id"
    )
    return charger

def get_user_active_session(user):
    for s in db.sessions:
        if s['usuario_id'] == user['id'] and s['status'] == 'ativa':
            return s
    return None

def get_user_sessions(user_id):
    user = find_list_item_by_field(
        db.sessions,
        user_id,
        'usuario_id'
    )
    return user


# ==========================
# SESSÕES
# ==========================

def find_sessions_by_charger_ids(
    sessions,
    charger_ids
):
    result = []

    for session in sessions:
        if session["carregador_id"] in charger_ids:
            result.append(session)

    return result


def get_list_item_by_status(
    items,
    status
):
    return find_list_item_by_field(
        items,
        status,
        "status"
    )


# ==========================
# CARREGADORES
# ==========================

def split_chargers(chargers):
    premium = []
    common = []

    for charger in chargers:

        if charger.get(
            "reservado_premium"
        ):
            premium.append(charger)

        else:
            common.append(charger)

    return premium, common


def active_chargers(chargers):
    return [
        charger
        for charger in chargers
        if charger["status"] != "manutencao"
    ]


def current_power_usage(chargers):
    return sum(
        charger["potencia_atual"]
        for charger in chargers
    )


# ==========================
# ESTABELECIMENTOS
# ==========================

def get_establishment_data_by_id(
    establishment_id
):
    establishment = find_item_by_field(
        db.establishments,
        establishment_id,
        "id_dono"
    )

    chargers = find_list_item_by_field(
        db.establishment_chargers,
        establishment["id"],
        "estabelecimento_id"
    )

    charger_ids = [
        charger["id"]
        for charger in chargers
    ]

    sessions = find_sessions_by_charger_ids(
        db.sessions,
        charger_ids
    )

    return {
        "establishment": establishment,
        "chargers": chargers,
        "sessions": sessions
    }