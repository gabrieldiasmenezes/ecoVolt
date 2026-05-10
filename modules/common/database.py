# database.py

# ==========================================
# SEÇÃO 1: CONFIGURAÇÕES GLOBAIS (ADMIN)
# ==========================================
system_settings = {
    "tarifa_base": 1.60,
    "tarifa_pico": 2.10,
    "comissao_goodwe": 0.10,
}

global_stats = {
    "total_dispositivos": 1540,
    "dispositivos_online": 1422,
    "total_energia_acumulada_mwh": 85.4,
    "receita_royalties_total": 0.0  # Calculado dinamicamente
}

# ==========================================
# SEÇÃO 2: DADOS DOS PARCEIROS (ESTABELECIMENTO)
# ==========================================
financial_mock = {
    "diario": 125.50,
    "semanal": 850.00,
    "mensal": 3400.00,
}

devices_mock = [
    {"id": "GW-001", "modelo": "7kW", "status": "Bom", "rendimento": 150.50, "ultima_manutencao": "2024-01-10"},
    {"id": "GW-002", "modelo": "22kW", "status": "Aviso", "rendimento": 450.75, "ultima_manutencao": "2023-12-05"},
    {"id": "GW-003", "modelo": "11kW", "status": "Bom", "rendimento": 320.00, "ultima_manutencao": "2024-02-15"},
    {"id": "GW-004", "modelo": "22kW", "status": "Falha", "rendimento": 0.00, "ultima_manutencao": "2024-03-01"}
]

# ==========================================
# SEÇÃO 3: DADOS DO USUÁRIO (RESIDENCIAL)
# ==========================================
# Hardware padrão para simulação residencial
residencial_hardware = {
    "id": "GW-HOME-01", 
    "modelo": "7kW (Wallbox Smart)", 
    "status": "Bom",
    "conexao": "Wi-Fi Casa",
    "versao_firmware": "v2.0.4"
}

# Dados do usuário (começa vazio para o setup preencher)
residencial_data = {
    "usuario": "",
    "modelo_carro": "",
    "id_dispositivo": "",
    "valor_kwh_casa": 0.0,
    "configurado": False
}