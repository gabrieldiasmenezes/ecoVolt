# ⚡ ChargeGrid Intelligence

> Gateway de inteligência para carregadores de veículos elétricos — controle de demanda, tarifação dinâmica e telemetria em tempo real.

---
---

## Integrantes

| RM | Nome |
|---|---|
| 571836 | Bruna Yukimy Hada |
| 571562 | Denize Ferrante |
| 570436 | Gabriel Del Pizzo Pintor |
| 572395 | Gabriel Dias Menezes |
| 570540 | Ian Rodrigues Martins |
| 572899 | Patrick Fernandes Martins Pais |

---

## O que é este projeto?

O **ChargeGrid Intelligence** transforma carregadores de veículos elétricos (VEs) e medidores inteligentes em um hub de dados inteligente. Cada sessão de recarga gera telemetria, eventos e metadados que são processados, armazenados e disponibilizados para faturamento, dashboards e módulos de IA.

Em termos simples: é um **middleware em Python** que fica entre os dispositivos físicos (carregadores GoodWe, medidores inteligentes) e os sistemas de gestão, garantindo que a energia seja distribuída de forma inteligente e que cada sessão seja registrada com precisão.

---

## Para quem é este sistema?

| Perfil | O que pode fazer |
|---|---|
| **Administrador Master (GoodWe)** | Monitorar frota completa, acessar toda a telemetria, gerir royalties |
| **Gestor do Estabelecimento (B2B)** | Ver relatórios financeiros, métricas do hardware, receber alertas |
| **Cliente Final** | Iniciar recargas, consultar custos, ver histórico e economia de CO₂ |

---

## Os 4 pilares do sistema

### 1. Controle de Demanda (DLM)
Quando o consumo total do prédio se aproxima do limite contratado, o sistema **reduz automaticamente a potência dos carregadores** — priorizando usuários Premium e cortando primeiro os de menor prioridade.

### 2. Protocolos Abertos
O gateway traduz dados dos dispositivos físicos (MODBUS / SEMS Plus) para o formato **OCPP simulado**, garantindo compatibilidade com sistemas de faturamento e gestão de terceiros.

### 3. Tarifação Dinâmica
O custo do kWh varia conforme:
- Horário (pico / fora de pico)
- Tipo de usuário (Premium, Cortesia Solar, etc.)
- Disponibilidade de energia solar

### 4. IA Aplicada
- **Modelo preditivo**: antecipa picos de consumo nas próximas horas
- **Síndico Virtual**: gera relatórios gerenciais em linguagem natural a partir da telemetria

---

## Estrutura de pastas

```
📦 projeto/
├── main.py                    # Ponto de entrada — inicializa o gateway
├── demo.py                    # Script de demonstração automática (Sprint 2)
│
├── auth/                      # Autenticação e cadastro de usuários
│   ├── auth.py
│   ├── login.py
│   ├── get_data_user.py
│   └── sign_up/               # Fluxo completo de cadastro
│
├── modules/                   # Núcleo de funcionalidades
│   ├── vehicles/              # CRUD de veículos
│   ├── sessions/              # Gestão de sessões de recarga + DLM
│   ├── commercial/            # Gestão de clientes comerciais
│   ├── establishment/         # Gestão do estabelecimento
│   └── administration/        # Painel administrativo
│   └── residential/        # Gestão de clientes residenciais
│
├── database/
│   ├── database.py            # Conexão com banco de dados
│   └── settings.py            # Configurações de persistência
│
└── utils/					   # Funções utilitárias 
    └── validation/            # Regras de validação compartilhadas
```

---

## Como rodar localmente

### Pré-requisitos
- Python 3.8 ou superior

### Instalação

```bash
# 1. Entre na pasta do projeto
cd caminho/para/o/projeto

# 2. (Recomendado) Crie um ambiente virtual
python -m venv .venv

# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Inicie a aplicação
python main.py
```

### Rodar a demonstração automática (Sprint 2)

O `demo.py` executa os principais cenários sem nenhuma interação manual:

```bash
python demo.py
```

**O que acontece ao rodar:**
1. 3 sessões de recarga são iniciadas simultaneamente (usuários 1000, 1001 e 1002)
2. Logs OCPP simulados são exibidos (Boot / Start / MeterValues)
3. A simulação DLM de sobrecarga é executada e a redistribuição de potência é impressa
4. Um relatório final é gerado (energia consumida, faturamento, CO₂ evitado)

---

## Guia de uso — passo a passo

> Siga esta ordem: primeiro crie um usuário, depois cadastre um veículo.

### Passo 1 — Cadastrar um usuário

```bash
python auth/sign_up/sign_up.py \
  --name "Test User" \
  --email "test.user@example.com" \
  --password "Test@1234" \
  --account-type "cliente_residencial" \
  --rfid "RFID-1001" \
  --phone "11999999999"
```

**Tipos de conta disponíveis:** `cliente_residencial` | `cliente_comercial` | `dono_estabelecimento` | 

Exemplo de entrada (formato JSON):
```json
{
  "name": "Test User",
  "email": "test.user@example.com",
  "password": "Test@1234",
  "account_type": "cliente_residencial",
  "rfid": "RFID-1001",
  "phone": "11999999999"
}
```

> ⚠️ Anote o `user_id` retornado — você vai precisar dele nos próximos passos.

---

### Passo 2 — Fazer login

```bash
python auth/login.py \
  --email "test.user@example.com" \
  --password "Test@1234"
```

**Retorno esperado:** token de sessão (JWT) ou objeto com dados do usuário autenticado.

---

### Passo 3 — Consultar dados do usuário

```bash
python auth/get_data_user.py --user-id user-0001
```

**Retorno esperado:** JSON com `name`, `email`, `account_type`, `rfid`.

---

### Passo 4 — Cadastrar um veículo

```bash
python modules/vehicles/register_vehicle.py \
  --user-id user-0001 \
  --plate ABC1D23 \
  --model "Leaf 40kWh" \
  --brand Nissan \
  --battery_capacity_kwh 40
```

Exemplo de entrada (formato JSON):
```json
{
  "user_id": "user-0001",
  "plate": "ABC1D23",
  "model": "Leaf 40kWh",
  "brand": "Nissan",
  "battery_capacity_kwh": 40
}
```

---

### Passo 5 — Atualizar dados do veículo

```bash
python modules/vehicles/update_vehicle.py \
  --vehicle-id vehicle-0001 \
  --alias "Carro do João"
```

**Campos que podem ser atualizados:** `alias`, `plate`, `model`, `battery_capacity_kwh`

---

### Passo 6 — Listar / consultar veículos

```bash
# Listar todos os veículos de um usuário
python modules/vehicles/vehicle_meneger.py --list --user user-0001

# Consultar um veículo específico
python modules/vehicles/vehicle_meneger.py --vehicle-id vehicle-0001
```

---

### Passo 7 — Simular múltiplas sessões (DLM)

```bash
python modules/sessions/session_menager.py --simulate-multiple
```

Simula 3 veículos carregando ao mesmo tempo e demonstra o balanceamento automático de potência.

---

## Como funciona o DLM (Controle de Demanda)

Quando múltiplos veículos carregam simultaneamente, o sistema calcula:

```
potência disponível = limite contratado − consumo atual do prédio
```

Se o consumo ultrapassar **95% do limite contratado**, o sistema reduz a potência dos carregadores automaticamente, seguindo esta ordem de corte:

1. Usuários sem plano / Cortesia Solar (cortados primeiro)
2. Usuários padrão
3. Usuários Premium / Fast (mantêm mínimo de 80% da potência solicitada)

### Prioridade de fonte de energia

Ao alocar potência para uma sessão, o sistema sempre prefere:

```
1º Energia Solar (direta)  →  2º Bateria  →  3º Rede Elétrica
```

---

## Formato dos logs (OCPP simulado)

Cada evento crítico gera um log em JSON para auditoria e faturamento:

```json
{
  "messageType": "StartTransaction",
  "timestamp": "2026-06-15T12:34:56Z",
  "connectorId": 1,
  "transactionId": "tx-12345",
  "meterValue": 12.34,
  "userId": "u-987",
  "notes": "simulated"
}
```

**Tipos de mensagem:** `MeterValues` | `StartTransaction` | `StopTransaction` | `BootNotification`

---

## Dicas para avaliação

- Use sempre `user-0001` e `vehicle-0001` como IDs nos testes para manter consistência
- Use `RFID-1001` como RFID de exemplo
- Crie o usuário **antes** de cadastrar veículos — o `user_id` é obrigatório no cadastro de veículos
- Campos opcionais (`phone`, `rfid`, `vin`) podem ser omitidos; se ocorrer erro de validação, inclua-os
- Se os scripts não aceitarem argumentos CLI, use a chamada direta:

```bash
python -c "from auth.sign_up import sign_up; sign_up({'name':'Test User','email':'test.user@example.com','password':'Test@1234','account_type':'resident'})"
```

---

## Próximos passos (Sprint 2)

- [ ] Scripts de simulação com 3+ sessões simultâneas e planos diferentes
- [ ] Testes automatizados com `pytest` para os fluxos de auth e vehicles
- [ ] Módulo de IA (`ai/predictor.py`) para previsão de picos de consumo
- [ ] Documentação de contratos de mensagens em `docs/messages.md`