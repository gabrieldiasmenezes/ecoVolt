ESTABLISHMENT_POWER = 11
RESIDENTIAL_POWER = 7
LIMIT_SIMULATION = 25

ROYALTY_RATE = 0.10
CO2_FACTOR = 0.233
KWH_PER_100KM = 15

PRICE_GASOLINE_PER_LITER = 6.20   # R$ por litro simulado
KM_PER_LITER = 12                  # consumo médio carro a gasolina
KWH_PER_100KM = 15   

DLM_CIRCUIT_BREAKER_LIMIT_KW = 5.0  # consumo médio elétrico

ROYALTY_RATE = 0.10  # 10% padrão

CRITICAL_POWER_THRESHOLD = 0   # carregador em uso mas com potência zero = anomalia

CURRENT_FIRMWARE = "2.4.1"
LATEST_FIRMWARE  = "2.5.0"

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


CHARGE_MODES={
    1: {
        "nome": "Prioridade Solar (Eco) ☀",
        "descricao": "Carrega apenas com excedente solar — custo zero",
        "potencia_kw": 3.5,
        "tarifa_override": 0.0
    },
    2: {
        "nome": "FV + Bateria 🔋",
        "descricao": "Solar + bateria da casa — evita rede elétrica",
        "potencia_kw": 5.0,
        "tarifa_override": 1.00
    },
    3: {
        "nome": "Carga Rápida (Fast) ⚡",
        "descricao": "Potência máxima — rede + solar + bateria",
        "potencia_kw": 7.0,
        "tarifa_override": None   
    }
}

OFF_PEAK_WINDOWS = [
    {"janela": "22h – 00h", "desconto": "30%", "hora_inicio": 22},
    {"janela": "00h – 06h", "desconto": "35%", "hora_inicio": 0},
]

FARE_LABELS = {
    "base":                "Tarifa Base (comum)",
    "premium":             "Tarifa Premium",
    "horario_pico":        "Tarifa Horário de Pico",
    "cortesia_solar":      "Cortesia Solar",
    "inicio_horario_pico": "Início do Horário de Pico (hora)",
    "fim_horario_pico":    "Fim do Horário de Pico (hora)"
}