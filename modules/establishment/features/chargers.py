from utils.ui import charger_card, enter, header

def chargers_service(chargers):
    header("CARREGADORES")

    for c in chargers:
        charger_card(c)

    enter()

