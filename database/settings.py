ESTABLISHMENT_POWER = 11
RESIDENTIAL_POWER = 7
LIMIT_SIMULATION = 25
ROYALTY_RATE = 0.10
CO2_FACTOR = 0.233
KWH_PER_100KM = 15

LINE_SEPARATOR='─' * 38


CHARGER_STATUS = {
    "em_uso":    "🟢 Em uso",
    "livre":     "🔵 Livre",
    "manutencao":"🔴 Manutenção"
}

ICON_TYPE = {
    "premium": "🔶 Premium",
    "comum":   "🔷 Comum",
    "residencial": "🏠 Residencial"
}

SESSION_STATUS = {
    "ativa":      "🟢 Ativa",
    "finalizada": "✅ Finalizada"
}

OCPP_TYPE_ICON = {
    "BootNotification": "🔌",
    "StartTransaction":  "▶️",
    "StopTransaction":   "⏹️",
    "MeterValues":       "📊",
    "Heartbeat":         "💓"
}

KNOWN_MODELS = {
    1: {"fabricante": "BYD",     "modelo": "BYD Dolphin",    "bateria_kwh": 44},
    2: {"fabricante": "BYD",     "modelo": "BYD Seal",       "bateria_kwh": 82},
    3: {"fabricante": "Volvo",   "modelo": "Volvo EX30",     "bateria_kwh": 51},
    4: {"fabricante": "Tesla",   "modelo": "Tesla Model 3",  "bateria_kwh": 60},
    5: {"fabricante": "Tesla",   "modelo": "Tesla Model Y",  "bateria_kwh": 75},
    6: {"fabricante": "Fiat",    "modelo": "Fiat Fastback",  "bateria_kwh": 54},
    7: {"fabricante": "Outro",   "modelo": "Outro",          "bateria_kwh": None},
}

PAYMENT_METHODS = {
    1: "Cartão de Crédito",
    2: "Cartão de Débito",
    3: "Pix",
    4: "Carteira ChargeGrid"
}