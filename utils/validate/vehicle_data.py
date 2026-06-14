import re
from database.database import vehicles

def validate_plate(plate):
    clean_plate = plate.strip().upper()
    # Formato antigo: ABC1234 ou novo Mercosul: ABC1D23
    padrao_antigo = r'^[A-Z]{3}\d{4}$'
    padrao_mercosul = r'^[A-Z]{3}\d[A-Z]\d{2}$'
    
    if not re.fullmatch(padrao_antigo, clean_plate) and not re.fullmatch(padrao_mercosul, clean_plate):
        print("Placa inválida! Use o formato ABC1234 ou ABC1D23.")
        return False
    
    for v in vehicles:
        if v.get('placa', '').upper() == clean_plate:
            print("Esta placa já está cadastrada!")
            return False
    
    return True


def validate_battery_kwh(value):
    try:
        kwh = float(value)
        if kwh < 10 or kwh > 200:
            print("Capacidade inválida! Informe um valor entre 10 e 200 kWh.")
            return False
        return True
    except ValueError:
        print("Digite apenas números.")
        return False


def validate_battery_level(value):
    try:
        level = int(value)
        if level < 0 or level > 100:
            print("Nível inválido! Informe um valor entre 0 e 100.")
            return False
        return True
    except ValueError:
        print("Digite apenas números.")
        return False