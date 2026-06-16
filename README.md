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
| **Cliente Comercial** | Iniciar recargas, ver histórico e economia de CO₂ |
| **Cliente Residencial** | Iniciar recargas, consultar custos, ver histórico e economia de CO₂ baseado em seu próprio carregador |


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
Exclusivo para o Administrador Master,o módulo de IA deste sistema tem o objetivo de mostrar o funcionamento base do modelo preditivo que queremos implementar no sistema real da solução, com o objetivo de antecipar picos de consumo e gerar relatórios gerenciais em linguagem natural a partir da telemetria coletada.Ele é composto por:

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
├── doc/                      # Relatório Técnico feito em formato .html
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

## Tipo de cadastro 

###  1 — Cadastrar um usuário

**Tipos de conta disponíveis:** `cliente_residencial` | `cliente_comercial` | `dono_estabelecimento` | 

Exemplo de entrada informações do usuário:
```json
{
  "name": "Test User",
  "email": "test.user@example.com",
  "phone": "11999999999",
  "password": "Test@1234",
  "city": "São Paulo",
  "account_type": "cliente_residencial",
}
```


Caso escolha `dono_estabelecimento` o sistema pedirá dados do estabelecimento que serão instalados os carregadores:
```json
{
  "name": "Condomínio Solar",
  "address": "Rua das Flores, 123",
  "cnpj": "45917263000106",
  "energia_solar": "S",
  "demanda_contratada_kw": 44,
  "quantidade_carregador":4
}
```
---

### 2 — Fazer login

```json
{
  "email": "maria.oliveira@email.com",
  "password": "123456",
}
```

---

### 3 — Cadastro de veículo

Caso nao tenha veículo cadastrado o sistema solicitará o cadastro do veículo para iniciar a recarga:
O sistema te mostraá os modelos disponíveis para cadastro, caso o modelo do veículo não esteja na lista, o usuário pode cadastrar um novo modelo com as seguintes informações:
```json
  {
      "usuario_id": "id_do_usuario_logado",
      "modelo": "BYD Dolphin",
      "fabricante": "BYD",
      "placa": "HJC2D33",
      "bateria_kwh": 44,
      "nivel_bateria": 40
  }
```

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


## Formato das sessões de recarga
Cada sessão de recarga é representada por um objeto JSON com os seguintes campos:

```json
  {
        "id": 1,
        "usuario_id": 1000,
        "veiculo_id": 2000,
        "carregador_id": 2,
        "energia_consumida_kwh": 22.5,
        "custo_total": 11.25,
        "inicio": "2026-06-12T18:30:00",
        "fim": "2026-06-12T20:00:00",
        "status": "finalizada"
  },
```

As sessões são responsáveis por armazenar e registrar todas as recargas realizadas nos estabelecimentos, permitindo uma gestão mais eficiente de todo o fluxo do sistema. Elas contribuem diretamente para o controle do atendimento aos clientes, a administração dos estabelecimentos — tanto no aspecto operacional quanto financeiro — e também servem como base essencial para o monitoramento de demanda e o correto faturamento das operações.


## Formato dos logs (OCPP simulado)

Cada evento crítico gera um log em JSON para auditoria e faturamento como:

```json
  {
        "id": 1,
        "carregador_id": 2,
        "tipo": "BootNotification",
        "mensagem": "Carregador conectado",
        "timestamp": "2026-06-12 18:29"
  },
```

---

## Próximos passos (Sprint 2)

- [ ] Scripts de simulação com 3+ sessões simultâneas e planos diferentes
- [ ] Testes automatizados com `pytest` para os fluxos de auth e vehicles
- [ ] Módulo de IA (`ai/predictor.py`) para previsão de picos de consumo
- [ ] Documentação de contratos de mensagens em `docs/messages.md`