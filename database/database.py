POTENCIA_ESTABELECIMENTO = 11
POTENCIA_RESIDENCIA = 7

users = [
    {
        "id": 1000,
        "nome": "Gabriel Dias",
        "email": "gabriel.dias@email.com",
        "telefone": "11999991111",
        "senha": "123456",
        "perfil": "cliente_comercial",
        "cidade": "São Paulo",
        "status": "ativo",
        "data_cadastro": "2026-06-01",
        "total_recargas": 12,
        "energia_consumida_kwh": 185.5
    },
    {
        "id": 1001,
        "nome": "Maria Oliveira",
        "email": "maria.oliveira@email.com",
        "telefone": "11999992222",
        "senha": "123456",
        "perfil": "cliente_comercial",
        "cidade": "São Paulo",
        "status": "ativo",
        "data_cadastro": "2026-05-20",
        "total_recargas": 8,
        "energia_consumida_kwh": 96.3
    },
    {
        "id": 1002,
        "nome": "Carlos Souza",
        "email": "carlos.souza@email.com",
        "telefone": "11999993333",
        "senha": "123456",
        "perfil": "cliente_residencial",
        "cidade": "Barueri",
        "status": "ativo",
        "data_cadastro": "2026-04-15",
        "total_recargas": 25,
        "energia_consumida_kwh": 412.8
    },
    {
        "id": 1003,
        "nome": "Operador ChargeGrid Plaza",
        "email": "gestao@plazacenters.com",
        "telefone": "1140040000",
        "senha": "admin123",
        "perfil": "dono_estabelecimento",
        "empresa": "Rede Plaza Centers",
        "cnpj": "12345678000190",
        "cidade": "São Paulo",
        "status": "ativo",
        "data_cadastro": "2025-01-10"
    },
    {
        "id": 1004,
        "nome": "Administrador GoodWe",
        "email": "admin@goodwe.com",
        "telefone": "1130009999",
        "senha": "goodwe123",
        "perfil": "administrador",
        "departamento": "Operações",
        "status": "ativo",
        "data_cadastro": "2024-08-01"
    }
]

vehicles = [
    {
        "id": 1,
        "usuario_id": 1000,
        "modelo": "BYD Dolphin",
        "fabricante": "BYD",
        "placa": "ABC1D23",
        "bateria_kwh": 44,
        "nivel_bateria": 35
    },
    {
        "id": 2,
        "usuario_id": 1001,
        "modelo": "Volvo EX30",
        "fabricante": "Volvo",
        "placa": "XYZ4E56",
        "bateria_kwh": 51,
        "nivel_bateria": 62
    },
    {
        "id": 3,
        "usuario_id": 1002,
        "modelo": "Tesla Model 3",
        "fabricante": "Tesla",
        "placa": "TES9L88",
        "bateria_kwh": 60,
        "nivel_bateria": 18
    }
]

establishments = [
    {
        "id": 1,
        "id_dono": 1003,
        "nome": "Shopping Morumbi",
        "endereco": "Av. Roque Petroni Júnior, 1089",
        "empresa_responsavel": "Rede Plaza Centers",
        "demanda_maxima_kw": 35,
        "potencia_em_uso_kw": 33,         
        "energia_total_distribuida_kwh": 185.5,
        "faturamento": 867.30,
        "status": "ativo",
        "possui_energia_solar": True,
        "carregadores_disponiveis": 4
    }
]

establishment_chargers = [
    {
        "id": 1,
        "estabelecimento_id": 1,
        "numero": 1,
        "modelo": "GoodWe GW-DC20",
        "status": "em_uso",
        "potencia_maxima": POTENCIA_ESTABELECIMENTO,
        "potencia_atual": 11,              
        "reservado_premium": False,
        "total_sessoes": 35,
        "energia_fornecida_kwh": 580.5
    },
    {
        "id": 2,
        "estabelecimento_id": 1,
        "numero": 2,
        "modelo": "GoodWe GW-DC20",
        "status": "em_uso",
        "potencia_maxima": POTENCIA_ESTABELECIMENTO,
        "potencia_atual": 11,             
        "reservado_premium": True,
        "total_sessoes": 42,
        "energia_fornecida_kwh": 710.8
    },
    {
        "id": 3,
        "estabelecimento_id": 1,
        "numero": 3,
        "modelo": "GoodWe GW-DC20",
        "status": "em_uso",
        "potencia_maxima": POTENCIA_ESTABELECIMENTO,
        "potencia_atual": 11,              
        "reservado_premium": False,
        "total_sessoes": 28,
        "energia_fornecida_kwh": 450.2
    },
    {
        "id": 4,
        "estabelecimento_id": 1,
        "numero": 4,
        "modelo": "GoodWe GW-DC20",
        "status": "manutencao",
        "potencia_maxima": POTENCIA_ESTABELECIMENTO,
        "potencia_atual": 0,              
        "reservado_premium": False,
        "total_sessoes": 12,
        "energia_fornecida_kwh": 190.4
    }
]

residencial_charger = [
    {
        "id": 1,
        "usuario_id": 1002,
        "modelo": "GoodWe Home 7kW",
        "status": "livre",
        "potencia_maxima": POTENCIA_RESIDENCIA,
        "potencia_atual": 0,
        "total_sessoes": 12,
        "energia_fornecida_kwh": 120.3
    }
]

sessions = [
    {
        "id": 4,
        "usuario_id": 1000,
        "veiculo_id": 1,
        "carregador_id": 4,
        "tipo": "comum",
        "potencia_kw": 11,
        "energia_kwh": 22,
        "tarifa_kwh": 4.26,
        "valor": 93.72,
        "inicio": "2026-06-10 10:00",
        "fim": "2026-06-10 12:00",
        "status": "finalizada"
    },
    {
        "id": 1,
        "usuario_id": 1000,
        "veiculo_id": 1,
        "carregador_id": 2,        
        "tipo": "premium",
        "potencia_kw": POTENCIA_ESTABELECIMENTO,
        "energia_kwh": 10,
        "tarifa_kwh": 5.11,
        "valor": 76.65,
        "inicio": "2026-06-12 18:30",
        "fim": None,
        "status": "ativa"
    },
    {
        "id": 2,
        "usuario_id": 1001,
        "veiculo_id": 2,
        "carregador_id": 3,        
        "tipo": "comum",
        "potencia_kw": POTENCIA_ESTABELECIMENTO,
        "energia_kwh": 10,
        "tarifa_kwh": 4.26,
        "valor": 42.60,
        "inicio": "2026-06-12 18:45",
        "fim": None,
        "status": "ativa"
    },
    {
        "id": 3,
        "usuario_id": 1002,
        "veiculo_id": 3,
        "carregador_id": 1,        
        "tipo": "comum",           
        "potencia_kw": POTENCIA_ESTABELECIMENTO,
        "energia_kwh": 8,
        "tarifa_kwh": 4.26,        
        "valor": 34.08,           
        "inicio": "2026-06-12 19:00",
        "fim": None,
        "status": "ativa"
    }
]

fares = {
    "base": 4.26,
    "premium": 5.11,
    "horario_pico": 4.90,
    "cortesia_solar": 1.00,
    "inicio_horario_pico": 18,
    "fim_horario_pico": 21
}

settings = {
    "ocpp_ativo": True,
    "modo_dlm": True,
    "versao_ocpp": "1.6J",
    "empresa_operadora": "GoodWe"
}

ocpp_logs = [
    {
        "id": 1,
        "carregador_id": 2,
        "tipo": "BootNotification",
        "mensagem": "Carregador conectado",
        "timestamp": "2026-06-12 18:29"
    },
    {
        "id": 2,
        "carregador_id": 2,
        "tipo": "StartTransaction",
        "mensagem": "Sessão iniciada",
        "timestamp": "2026-06-12 18:30"
    },
    {
        "id": 3,
        "carregador_id": 3,
        "tipo": "MeterValues",
        "mensagem": "Potência atual 11 kW",  # corrigido de 10 para 11
        "timestamp": "2026-06-12 18:45"
    }
]