from modules.sessions.features.comercial.charge_amount import choose_charge_amount
from modules.sessions.features.comercial.charger_select import select_charger
from modules.sessions.features.comercial.select_confirm import confirm_and_pay
from modules.sessions.features.comercial.session_create import create_session, end_session_flow
from modules.vehicles.vehicle_meneger import prompt_register_if_no_vehicle
from utils.helpers import get_user_active_session, get_user_vehicle
from utils.system import reset_terminal
from utils.ui import header, enter


def session_manager(user, action):
    if action == 'iniciar':
        _start_session(user)
    elif action == 'encerrar':
        end_session_flow(user)


def _start_session(user):
    reset_terminal()
    header("INICIAR RECARGA")

    active = get_user_active_session(user)
    if active:
        print(f"\nVocê já possui uma sessão ativa (ID #{active['id']}).")
        enter()
        return

    vehicle = get_user_vehicle(user['id'])
    if not vehicle:
        prompt_register_if_no_vehicle(user)
        return

    kwh_to_charge, charge_desc = choose_charge_amount(vehicle)
    if kwh_to_charge is None:
        return

    result = select_charger(kwh_to_charge, charge_desc)
    if result is None:
        return

    paid = confirm_and_pay(user, result, kwh_to_charge, charge_desc)
    if not paid:
        return

    create_session(user, vehicle, result, kwh_to_charge, charge_desc)