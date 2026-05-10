import random

VALID_CAR_MODELS = [
    "Tesla Model 3",
    "Tesla Model S",
    "Nissan Leaf",
    "BMW i3",
    "Chevrolet Bolt",
    "Hyundai Kona Electric",
    "Volkswagen ID.4"
]

def validate_car_model(model):
    """
    Valida se o modelo do carro está na lista de veículos elétricos suportados.
    """
    return model.strip().title() in VALID_CAR_MODELS

def get_home_battery_telemetry():
    """
    Gera telemetria de bateria residencial simulada.
    """
    current_level = random.randint(10, 50)
    target_level = random.randint(80, 100)
    return {"current": current_level, "target": target_level}

def calculate_home_economy_savings():
    """
    Calcula economia mensal simulada comparando custo de eletricidade e gasolina.
    """
    monthly_kwh = 30
    electricity_cost = monthly_kwh * 0.80
    gasoline_cost = (200 / 100) * 8 * 5
    savings = gasoline_cost - electricity_cost
    return max(savings, 0)