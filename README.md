
# ChargeGrid Intelligence — Documento Técnico

Resumo técnico e guia de uso do projeto ChargeGrid Intelligence. Este documento apresenta a visão geral, arquitetura, pilares técnicos, simulação prevista para a Sprint 2, descrição dos componentes do código e uma tabela de testes prática baseada nas pastas `auth` e `modules/vehicles` para facilitar a avaliação do professor.

---

**Índice**
- **Introdução**
- **Objetivo**
- **Personas**
- **Visão Geral do Projeto**
- **Quatro Pilares da Solução**
- **Arquitetura (MVC) e Componentes**
- **Fluxos e Simulação Técnica (Sprint 2)**
- **Algoritmos Principais**
- **Logs e Auditoria (formato OCPP-simulado)**
- **Tabela de Testes (base: `auth`, `modules/vehicles`)**
- **Execução local e Comandos `bash`**
- **Referência de Arquivos Principais**
- **Próximos passos / Observações para avaliação**

---

**Introdução**

Este projeto converte carregadores de veículos elétricos (VEs) e medidores inteligentes em um Hub de Inteligência. Cada sessão de recarga gera telemetria, eventos e metadados que são traduzidos, armazenados e disponibilizados para faturamento, dashboards e módulos de IA.

**Objetivo**

Construir um gateway (middleware) em Python que:
- Coleta dados da camada física (GoodWe HCA G2, Smart Meters, portal SEMS Plus).
- Traduz dados brutos para mensagens compatíveis com OCPP (simuladas) e armazena sessões estruturadas.
- Implementa controle de demanda (DLM), tarifação dinâmica e priorização de usuários.
- Fornece APIs/rotinas administrativas para administração, gestão e clientes finais.

**Personas**

- **Administrador Master (GoodWe)**: Monitora frota, acesso completo à telemetria e gestão de royalties.
- **Gestor do Estabelecimento (B2B)**: Recebe relatórios financeiros, métricas de saúde do hardware e alertas.
- **Cliente Final**: Inicia sessões de recarga, consulta custos estimados, histórico e economia de CO2.

---

**Quatro Pilares da Solução**

1. Controle de Demanda (DLM)
	- Reduz potência dos carregadores quando o consumo total se aproxima do limite contratado da edificação.
2. Protocolos Abertos
	- Gateway traduz MODBUS/SEMS Plus para mensagens OCPP simuladas para interoperabilidade.
3. Tarifação e Pagamento
	- Tarifação dinâmica via API: custo do kWh varia por horário, tipo de usuário e contexto de demanda.
4. IA Aplicada
	- Modelos preditivos para antecipar picos e um Síndico Virtual (NLP) para gerar relatórios gerenciais.

---

**Arquitetura (MVC) e Componentes**

O projeto segue MVC: modelos (persistência/estrutura de dados), controladores (lógica de negócios) e visões (APIs / UI simulada). Diretórios principais:

- `auth/` — Autenticação e cadastro de usuários (login, sign-up, descrições de tipo de conta, coleta de dados do usuário).
- `database/` — Inicialização e acesso ao armazenamento (conexões, settings).
- `modules/` — Núcleo de features e serviços: administrações, comercial, establishment, sessions e `vehicles`.
- `utils/` — Helpers, validações e utilitários (UI helpers, validações comuns).
- `main.py` — Ponto de entrada da aplicação (inicialização do gateway e dos serviços).

Cada camada é modular para permitir simulação local: os adaptadores de dispositivo (GoodWe/SEMS) são representados por rotinas de coleta que populam eventos e sessões.

**Componentes-chave (descrição resumida)**

- `auth/auth.py` e `auth/login.py`: rotinas de autenticação e sessão de usuário.
- `auth/sign_up/**`: fluxo de cadastro, captura de tipo de conta e dados do usuário.
- `modules/vehicles/register_vehicle.py`: cadastro de veículo associado a um usuário.
- `modules/vehicles/update_vehicle.py`: atualização de metadados do veículo.
- `modules/sessions/*`: gerenciamento de sessões de recarga (start/stop/summary).

---

**Fluxos e Simulação Técnica (Sprint 2)**

1. Coleta de Dados (modelo pull):
	- Periodicamente (`cron`/loop), o gateway consulta o portal SEMS Plus e/ou adaptadores locais.
	- Dados coletados por sessão: ID do usuário (RFID), energia consumida (kWh), tempo de sessão, estado do carregador.

2. Geração de Sessão Estruturada:
	- Cada evento é transformado em um objeto sessão com metadados (usuario_id, vehicle_id, energy_kwh, start_ts, end_ts, peak_power_kw).

3. Prioridade de Fonte de Energia:
	- Ao alocar potência, aplicar ordem de prioridade: 1º Energia Solar (direta), 2º Bateria, 3º Rede Elétrica.

4. Gerenciamento de Múltiplas Sessões e DLM:
	- Simular 3+ veículos iniciando sessão concorrente. O módulo DLM calcula potência disponível = contratado - consumo_restante.
	- Se consumo_total > limiar (ex.: 95% do contratado), reduzir potência de carregadores por ordem de prioridade de usuário/plano.

5. Tarifação Dinâmica:
	- Tarifas definidas por janelas (off-peak, peak) e por tipo de usuário (Premium, Cortesia Solar).
	- O cálculo de custo da sessão: custo = energy_kwh * tarifa(horario, plano).

6. IA (preditivo e síntese):
	- Modelo simples preditivo (regressão/ML) estima tendência de consumo nas próximas N horas.
	- Síndico Virtual: rotinas que transformam telemetria em resumo textual para gestores.

---

**Algoritmos Principais (resumo técnico)**

1. Balanceador DLM (pseudo):

```python
# Entrada: lista_de_sessoes_ativas, limite_contratado_kw, prioridades_usuarios
def distribuir_potencia(sessoes, limite_kw, prioridades):
	 demanda_total = sum(s.requested_kw for s in sessoes)
	 if demanda_total <= limite_kw:
		  alocar_potencia_normal(sessoes)
	 else:
		  # reduzir por prioridades: cortar consumidores não-VIP primeiro
		  sessoes_ordenadas = ordenar_por_prioridade(sessoes, prioridades)
		  reduzir_para_encaixar(sessoes_ordenadas, limite_kw)

	 return sessoes  # com `allocated_kw` atualizado
```

2. Prioridade por Plano
	- `Premium/Fast` mantém margem mínima (ex.: 80% do pedido); `Cortesia Solar` recebe carga apenas se houver solar disponível.

3. Escalonamento por Fonte de Energia
	- Ao calcular potência disponível, considerar contribuição solar instantânea (se disponível) e reduzir uso de rede.

---

**Logs e Auditoria (formato OCPP-simulado)**

As mensagens de auditoria são geradas em formato JSON com campos chave similares ao OCPP para facilitar integração com sistemas de faturamento:

```json
{
  "messageType": "MeterValues|StartTransaction|StopTransaction",
  "timestamp": "2026-06-15T12:34:56Z",
  "connectorId": 1,
  "transactionId": "tx-12345",
  "meterValue": 12.34,
  "userId": "u-987",
  "notes": "simulated"
}
```

Cada evento crítico possui um log com carimbo de tempo para auditoria e faturamento.

---

**Guia de Dados para Teste (inputs exemplares)**

Esta seção substitui a tabela de testes por exemplos concretos de entradas para os scripts que realizam cadastro/consulta. Use os exemplos abaixo para preencher prompts ou parâmetros de linha de comando — assim o avaliador não precisa adivinhar formatos ou valores.

- `auth/sign_up/sign_up.py` (campos comuns para cadastro):
	- `name`: "Test User"
	- `email`: "test.user@example.com"
	- `password`: "Test@1234" (exemplo seguro para teste)
	- `account_type`: valores válidos: `resident`, `comercial`, `admin`, `goodwe`
	- `rfid` (opcional): "RFID-1001"
	- `phone` (opcional): "+5511999999999"
	- Exemplo JSON de entrada:

```json
{
	"name": "Test User",
	"email": "test.user@example.com",
	"password": "Test@1234",
	"account_type": "resident",
	"rfid": "RFID-1001",
	"phone": "+5511999999999"
}
```

- `auth/login.py` (autenticação):
	- `email` ou `username`: "test.user@example.com"
	- `password`: "Test@1234"
	- Resultado esperado: token de sessão (JWT ou string) ou objeto usuário autenticado.

- `auth/get_data_user.py` (consulta de usuário):
	- `--user-id`: exemplo `user-0001` ou `1` conforme formato do `user_id` usado na aplicação
	- Se houver endpoint/API, usar `GET /users/<user-id>` e esperar JSON com campos `name`, `email`, `account_type`, `rfid`.

- `modules/vehicles/register_vehicle.py` (cadastro de veículo):
	- `user_id`: exemplo `user-0001` (associar veículo a usuário existente)
	- `plate`: "ABC1D23" (formato local)
	- `model`: "Leaf 40kWh"
	- `brand`: "Nissan"
	- `battery_capacity_kwh`: 40
	- `vin` (opcional): "VIN123456789"
	- Exemplo JSON de entrada:

```json
{
	"user_id": "user-0001",
	"plate": "ABC1D23",
	"model": "Leaf 40kWh",
	"brand": "Nissan",
	"battery_capacity_kwh": 40
}
```

- `modules/vehicles/update_vehicle.py` (atualização de dados do veículo):
	- `--vehicle-id`: exemplo `vehicle-0001`
	- Campos para atualização: `alias`, `plate`, `model`, `battery_capacity_kwh`
	- Exemplo: atualizar `alias` para "Carro do João".

- `modules/vehicles/vehicle_meneger.py` (consulta/listagem):
	- Para listar veículos de um usuário: `--list --user user-0001`
	- Para consultar um veículo específico: `--vehicle-id vehicle-0001`

Exemplos de comandos (quando os scripts suportam argumentos):

```bash
python auth/sign_up/sign_up.py --name "Test User" --email "test.user@example.com" --password "Test@1234" --account-type "resident" --rfid "RFID-1001"
python auth/login.py --email "test.user@example.com" --password "Test@1234"
python auth/get_data_user.py --user-id user-0001
python modules/vehicles/register_vehicle.py --user-id user-0001 --plate ABC1D23 --model "Leaf 40kWh" --brand Nissan --battery_capacity_kwh 40
python modules/vehicles/update_vehicle.py --vehicle-id vehicle-0001 --alias "Carro do João"
python modules/vehicles/vehicle_meneger.py --list --user user-0001
```

Se os scripts não aceitarem argumentos de linha de comando, use os JSON de exemplo e invoque internamente (exemplo):

```bash
python -c "from auth.sign_up import sign_up; sign_up({\"name\":\"Test User\",\"email\":\"test.user@example.com\",\"password\":\"Test@1234\",\"account_type\":\"resident\"})"
```

Observações úteis para o avaliador:
- Sempre crie um usuário de teste antes de cadastrar veículos; anote o `user_id` retornado para usar nos passos seguintes.
- Use `RFID-1001` e `vehicle-0001` como convenção de exemplo ao preencher prompts para manter consistência entre testes.
- Campos opcionais podem ser omitidos; se ocorrer erro de validação, tente incluir `phone` e `rfid` conforme os exemplos acima.


---

**Execução local e Comandos `bash`**

Passos mínimos para rodar localmente (assumindo Python 3.8+):

```bash
# entrar na pasta do projeto
cd c:/Users/Administrador/Desktop/MyArea/2026/fiap/dataStructure/ecoVolt

# executar a aplicação (ponto de entrada)
python main.py

# executar scripts específicos (ex.: cadastro)
python auth/sign_up/sign_up.py
python auth/login.py
python modules/vehicles/register_vehicle.py

# rodar uma simulação DLM (se houver script específico)
python modules/sessions/session_menager.py --simulate-multiple
```

Se preferir, crie um ambiente virtual e instale dependências (se houver `requirements.txt`):

```bash
python -m venv .venv
source .venv/bin/activate   # no Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

**Referência de Arquivos Principais**

- `main.py`: inicialização do gateway e rotinas agendadas.
- `auth/`: login, sign-up e utilitários de coleta/validação de dados do usuário.
- `database/database.py` e `database/settings.py`: conexão e configurações de persistência.
- `modules/sessions/`: lógica de sessões, DLM e relatórios de sessão.
- `modules/vehicles/`: CRUD de veículos.
- `utils/validation/*`: regras de validação usadas por `auth` e `vehicles`.

---

**Próximos passos sugeridos para a entrega da Sprint 2**

1. Implementar cenários de simulação completos: criar scripts que disparem 3+ sessões simultâneas com diferentes planos.
2. Adicionar testes automatizados (pytest) para os casos listados na tabela de testes.
3. Conectar o módulo de IA básico (p.ex. um notebook ou serviço `ai/predictor.py`) para gerar previsões de pico.
4. Documentar contratos de mensagens (JSON/OCPP-simulado) em um arquivo separado `docs/messages.md`.

---

**Demo script: `demo.py`**

- **Localização:** `demo.py` (arquivo na raiz do projeto).
- **Objetivo:** demonstrar automaticamente os principais cenários da Sprint 2 para avaliação.
- **O que o script realiza:**
	- Inicia 3 sessões de recarga (usuários 1000, 1001 e 1002) sem interação.
	- Mostra logs OCPP simulados (Boot/Start/MeterValues).
	- Executa a simulação DLM de sobrecarga e imprime a redistribuição proposta.
	- Gera e imprime relatório do estabelecimento (energia, faturamento, CO₂ evitado).
- **Como executar:**

```bash
python demo.py
```

- **Saída esperada:** resumo de sessões ativas, mensagens OCPP simuladas, resultado da simulação DLM e relatório final.

---

Se quiser, eu posso:
- Gerar os scripts de simulação DLM para 3 veículos simultâneos.
- Criar testes `pytest` a partir da tabela de testes acima.

Deseja que eu aplique essas próximas ações agora? 

