from database.database import establishments,establishment_chargers,sessions

def get_data_establishment(id):
    establishment = {}
    for est in establishments:
        if id == est['id_dono']:
            establishment = est
            break 

    if not establishment:
        return {"establishment": {}, "chargers": [], "sessions": []}

    chargers = []
    for charger in establishment_chargers:
        if establishment['id'] == charger['estabelecimento_id']:
            chargers.append(charger)
            
    allowed_charger_ids = [charger['id'] for charger in chargers]

    session_list = []
    for session in sessions:
        if session['carregador_id'] in allowed_charger_ids:
            session_list.append(session)
            
    return {
        "establishment": establishment,
        "chargers": chargers,
        "sessions": session_list
    }