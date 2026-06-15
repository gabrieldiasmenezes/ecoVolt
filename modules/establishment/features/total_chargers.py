from database.settings import ESTABLISHMENT_POWER
from utils.system import load
from utils.ui import header
from utils.validation.common_validation import validate_int_value

def verify_integer(text):
    while True:
        value=validate_int_value(text)
        if value<=0:
            print('Valor tem que ser maior que 0!')
            continue
        return value
    
def get_total_chargers():
    demand_kw= verify_integer("Informe a demanda contratada (kW): ")
    max_chargers=demand_kw // ESTABLISHMENT_POWER

    if max_chargers < 1:
        max_chargers = 1

    header("DIMENSIONAMENTO DO SISTEMA")
    print(f"Demanda contratada: {demand_kw} kW")
    print(f"Potência por carregador: {ESTABLISHMENT_POWER} kW")
    print(f"Carregadores máximos suportados: {max_chargers}")

    while True:
        contractors= verify_integer("Informe a demanda contratada (kW): ")

        if contractors > max_chargers:
            print(
                f"Não é possível instalar {contractors} carregadores. "
                f"Máximo suportado: {max_chargers}"
            )
            continue
        load('Calculando informações')
        print("\nCarregadores aprovados com sucesso!")
        return demand_kw,contractors
