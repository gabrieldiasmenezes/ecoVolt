from datetime import datetime
from database.database import fares
from modules.comercial.feature.billing import billing_service
from utils.ui import error_option, header, enter, separator
from utils.system import reset_terminal
from utils.validation.common_validation import validate_int_value
from database.settings import ICON_TYPE

def confirm_and_pay(user, result, kwh_to_charge, charge_desc):
    hora = datetime.now().hour
    is_peak = fares['inicio_horario_pico'] <= hora < fares['fim_horario_pico']

    charger = result['charger']
    fare = result['tarifa']
    motivo = result['motivo']
    total_price = result['total_price']
    minutes = result['minutes']
    is_premium = charger.get('reservado_premium', False)
    label_type = ICON_TYPE['premium'] if is_premium else ICON_TYPE["comum"]
    while True:
        reset_terminal()
        header("RESUMO E CONFIRMAÇÃO")
        print(f"\n{charge_desc}")
        print(f"\nCarregador: #{charger['numero']}  {label_type}")
        print(f"Energia: {kwh_to_charge} kWh")
        print(f"Tarifa: R$ {fare:.2f}/kWh  ({motivo})")
        print(f"Tempo estimado: ~{minutes} min")
        print(f"\nValor total: R$ {total_price:.2f}")
        if is_peak:
            print("\n⚡ Horário de pico ativo (18h–21h)")
        separator()

        option = validate_int_value("\n1 - Confirmar e pagar\n0 - Cancelar\n\nOpção: ")
        if option == 0:
            print("\nRecarga cancelada.")
            enter()
            return False
        elif option == 1:
            return billing_service(user, total_price, label_type)
        else:
            error_option()
            continue