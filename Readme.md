# ChargeGrid Intelligence

**Plataforma integrada de gestão para recarga de veículos elétricos**  
Desenvolvido para GoodWe | Disciplina: Data Structures and Algorithms — FIAP | Sprint 1, Maio 2026

---

## Sumário

1. [Visão Geral](#visão-geral)
2. [Problema e Solução](#problema-e-solução)
3. [Funcionalidades por Módulo](#funcionalidades-por-módulo)
4. [Arquitetura do Sistema](#arquitetura-do-sistema)
5. [Pré-requisitos e Instalação](#pré-requisitos-e-instalação)
6. [Como Executar](#como-executar)
7. [Estrutura de Diretórios](#estrutura-de-diretórios)
8. [Guia de Uso por Perfil](#guia-de-uso-por-perfil)
9. [Referência de Módulos](#referência-de-módulos)
10. [Testes Validados](#testes-validados)
11. [Roadmap](#roadmap)

---

## Visão Geral

ChargeGrid Intelligence é um sistema de gerenciamento de infraestrutura de recarga de veículos elétricos (VEs) voltado ao setor comercial. A plataforma centraliza o controle de demanda energética, o gerenciamento de eletropostos e a aplicação de políticas de tarifação dinâmica em uma única base de dados.

O sistema atende simultaneamente a três perfis distintos de usuário — clientes finais (residencial e comercial), gestores de estabelecimentos parceiros e administradores globais da GoodWe — garantindo consistência operacional e rastreabilidade completa das sessões de recarga.

A implementação utiliza Python puro com arquitetura MVC, sem dependências externas, o que facilita a execução em qualquer ambiente com Python 3.7 ou superior instalado.

---

## Problema e Solução

A infraestrutura comercial de recarga de VEs enfrenta três lacunas críticas:

- Ausência de mecanismos integrados para controle de potência entre carregadores.
- Falta de registro estruturado de sessões de recarga para auditoria e faturamento.
- Políticas de tarifação e pagamento inadequadas para cenários de uso variável.

ChargeGrid Intelligence endereça cada um desses pontos:

| Lacuna | Solução Implementada |
|--------|----------------------|
| Controle de potência | Seleção de carregador por nível (7kW / 11kW / 22kW) com cálculo de tempo e energia |
| Registro de sessões | Armazenamento centralizado em `session_history` com todos os parâmetros da sessão |
| Tarifação inadequada | Tarifação dinâmica por horário: R$ 1,60/kWh (normal) e R$ 2,10/kWh (pico: 18h–21h) |

---

## Funcionalidades por Módulo

### Módulo Comercial (Perfil B2C — Recarga Pública)

Simula a experiência de recarga em postos parceiros da GoodWe.

- Seleção de potência: 7kW (lenta), 11kW (padrão) ou 22kW (rápida).
- Tarifação dinâmica baseada no horário da sessão.
- Cálculo automático de energia necessária, tempo estimado e custo total.
- Simulação de transferência de energia com barra de progresso (incrementos de 5%).
- Registro completo da sessão ao término (potência, energia, custo, duração).

Fluxo de uso:

```
Selecionar carregador -> Inserir dados da bateria -> Revisar custo e tempo ->
Confirmar recarga -> Acompanhar progresso -> Receber relatório final
```

### Módulo Residencial (Perfil Smart Home)

Experiência simplificada para usuários com carregador doméstico, sem complexidade de pagamentos.

- Onboarding inicial: nome do usuário, modelo do veículo (validado) e ID do carregador.
- Dashboard de economia: comparação de custos mensais entre eletricidade e gasolina.
- Telemetria simplificada: nível de bateria atual e meta de carga.
- Informações técnicas do carregador doméstico.

Modelos de veículos aceitos: Tesla Model 3, Tesla Model S, Nissan Leaf, BMW i3, Chevrolet Bolt, Hyundai Kona Electric, Volkswagen ID.4.

### Módulo Estabelecimento (Perfil B2B — Gestores)

Ferramentas de gestão para proprietários de locais com carregadores instalados.

- Relatórios financeiros simulados: faturamento diário, semanal e mensal.
- Monitoramento de hardware: lista de dispositivos com status (Bom, Aviso, Falha).
- Gestão de manutenção: alteração manual de status de dispositivos.
- Ranking de rendimento financeiro por carregador.

### Módulo Admin Master (Perfil GoodWe)

Controle macro da infraestrutura nacional de carregadores.

- KPIs de disponibilidade: taxa de dispositivos online e saúde geral da rede.
- Ajuste global de tarifas: altera preços base e de pico para todos os postos.
- Relatório de royalties: cálculo automático de comissões sobre faturamento de parceiros.
- Filtro de falhas: identifica dispositivos críticos para priorização de manutenção.

---

## Arquitetura do Sistema

O projeto segue o padrão MVC (Model-View-Controller), com separação clara de responsabilidades entre camadas.

```
main.py (Portal de entrada)
    |
    +-- modules/commercial/   controller -> logic -> view
    +-- modules/residencial/  controller -> logic -> view
    +-- modules/establishment/ controller -> logic -> view
    +-- modules/admin/        controller -> view
    +-- modules/common/       database.py (Single Source of Truth)
    +-- core/                 auth.py, utils.py
```

| Camada | Responsabilidade | Exemplos |
|--------|------------------|----------|
| View | Interação com o usuário | Exibição de menus, coleta de inputs, formatação de saída |
| Logic | Cálculos e validações | Tarifação dinâmica, validação de modelo de veículo, cálculo de economia |
| Controller | Orquestração do fluxo | Chamar view para inputs, chamar logic para cálculos, gerenciar estados |
| Database | Armazenamento centralizado | `session_history`, `residencial_data` — compartilhados entre módulos |

**Tecnologias utilizadas:** Python 3.x, `datetime`, `time`, `os`, `re`. Sem dependências externas.

---

## Pré-requisitos e Instalação

**Requisitos mínimos:**
- Python 3.7 ou superior
- Terminal (CMD ou PowerShell no Windows; bash no macOS/Linux)
- Aproximadamente 50 MB de espaço em disco

**Verificar instalação do Python:**

```bash
python --version
# ou
python3 --version
```

**Obter o projeto:**

```bash
# Via Git
git clone https://github.com/seu-repositorio/chargeGrid-intelligence.git
cd chargeGrid-intelligence

# Via arquivo ZIP
unzip chargeGrid-intelligence.zip
cd chargeGrid-intelligence
```

Nenhuma instalação adicional é necessária. O projeto não utiliza bibliotecas de terceiros.

---

## Como Executar

```bash
# Windows
python main.py

# macOS / Linux
python3 main.py
```

**Sequência de execução:**

1. O sistema solicita o nome do usuário (autenticação simulada).
2. O menu principal exibe as 6 opções de perfil disponíveis.
3. O usuário seleciona o perfil e é direcionado ao módulo correspondente.
4. Ao encerrar o módulo, o sistema retorna ao menu principal.
5. A opção 6 encerra o programa.

---

## Estrutura de Diretórios

```
chargeGrid-intelligence/
├── main.py
├── README.md
├── core/
│   ├── __init__.py
│   ├── auth.py
│   └── utils.py
└── modules/
    ├── __init__.py
    ├── commercial/
    │   ├── __init__.py
    │   ├── controller.py
    │   ├── logic.py
    │   └── view.py
    ├── residencial/
    │   ├── __init__.py
    │   ├── controller.py
    │   ├── logic.py
    │   └── view.py
    ├── establishment/
    │   ├── __init__.py
    │   ├── controller.py
    │   ├── logic.py
    │   └── view.py
    ├── admin/
    │   ├── __init__.py
    │   ├── controller.py
    │   └── view.py
    └── common/
        └── database.py
```

---

## Guia de Uso por Perfil

### Perfil 1 — Cliente Comercial

Cenário de uso: recarga em um posto parceiro GoodWe.

Exemplo prático:
- Veículo: bateria de 60 kWh, nível atual 20%, meta de 80%.
- Carregador selecionado: 11kW.
- Horário: 19h30 (período de pico).
- Resultado: 36 kWh a serem transferidos, duração estimada de 327 minutos, custo total de R$ 75,60.

### Perfil 2 — Dono de Estabelecimento

Cenário de uso: monitoramento e gestão dos carregadores instalados no local.

Acesso disponível:
- Relatórios de faturamento por período.
- Status de cada dispositivo com possibilidade de atualização manual.
- Ranking de rendimento entre os carregadores do estabelecimento.

### Perfil 3 — Cliente Residencial

Cenário de uso: gerenciamento da recarga no carregador doméstico.

Exemplo prático:
- Usuário: Maria Silva, Tesla Model 3, carregador ID RES-0001.
- Dashboard exibe economia simulada de R$ 60/mês em comparação ao abastecimento com gasolina.

### Perfil 4 — GoodWe Admin

Cenário de uso: visão consolidada de toda a rede nacional de carregadores.

Acesso disponível:
- KPIs de disponibilidade e saúde da rede.
- Ajuste centralizado de tarifas (afeta todos os postos imediatamente).
- Cálculo automático de royalties por parceiro (percentual configurável, padrão: 10%).
- Lista de dispositivos com falha crítica para acionamento de equipes de manutenção.

### Perfil 5 — Saiba Mais

Exibe informações sobre o projeto: descrição, objetivos, diferenciais e tecnologias utilizadas.

### Perfil 6 — Sair

Encerra o programa.

---

## Referência de Módulos

### core/auth.py

| Função | Descrição |
|--------|-----------|
| `welcome(name_prompt)` | Exibe boas-vindas e coleta o nome do usuário |

### core/utils.py

| Função | Descrição |
|--------|-----------|
| `clear_terminal()` | Limpa o console |
| `get_menu_option(title, menu_text)` | Exibe menu e retorna opção válida com validação de entrada |
| `get_numeric_input(prompt, min_val, max_val, error_msg)` | Coleta entrada numérica com validação de intervalo |
| `get_separator(length)` | Retorna linha de separação formatada |
| `header(title, length)` | Exibe título com bordas formatadas |

### modules/commercial/

| Arquivo | Função | Descrição |
|---------|--------|-----------|
| controller.py | `run_commercial_module()` | Orquestra o fluxo completo: seleção, cálculo, simulação e registro |
| logic.py | `get_fee_per_kwh()` | Retorna a tarifa vigente com base no horário atual |
| view.py | `get_charge_power()` | Menu de seleção de potência (7kW / 11kW / 22kW) |
| view.py | `get_battery_data()` | Coleta e valida os dados da bateria do usuário |
| view.py | `start_charging_simulation(battery_data, charger_power)` | Exibe a barra de progresso da recarga |

### modules/residencial/

| Arquivo | Função | Descrição |
|---------|--------|-----------|
| controller.py | `run_residential_module(name)` | Menu residencial com 4 opções |
| logic.py | `validate_car_model(model)` | Valida o modelo do veículo contra a lista pré-definida |
| logic.py | `get_home_battery_telemetry()` | Simula telemetria de bateria doméstica |
| logic.py | `calculate_home_economy_savings(user_data)` | Calcula a economia mensal em comparação ao combustível |
| view.py | `setup_residential_user(name)` | Onboarding: coleta nome, modelo do veículo e ID do carregador |
| view.py | `display_home_economy(savings)` | Exibe o dashboard de economia |
| view.py | `display_home_hardware_details()` | Exibe informações técnicas do carregador |
| view.py | `start_home_charging_simulation(battery_data)` | Simula a recarga doméstica |

### modules/common/database.py

| Estrutura | Tipo | Descrição |
|-----------|------|-----------|
| `session_history` | Lista | Registro de todas as sessões comerciais realizadas |
| `residencial_data` | Dicionário | Dados de configuração do usuário residencial |

---

## Testes Validados

| Cenário | Entrada | Saída Esperada | Status |
|---------|---------|----------------|--------|
| Menu comercial — opção válida | `1` (carregador 7kW) | Confirmação do carregador selecionado | Aprovado |
| Dados de bateria válidos | Cap: 60 kWh, Atual: 20%, Meta: 80% | Cálculo de 36 kWh necessários | Aprovado |
| Tarifação no horário de pico | Horário: 19h | Tarifa aplicada: R$ 2,10/kWh | Aprovado |
| Tarifação no horário normal | Horário: 14h | Tarifa aplicada: R$ 1,60/kWh | Aprovado |
| Setup residencial completo | Nome: João, Carro: Tesla Model 3 | Confirmação de setup concluído | Aprovado |
| Modelo de veículo inválido | "Fiat 500" | Loop de validação até entrada correta | Aprovado |
| Cálculo de economia residencial | 30 kWh x R$ 0,80 | Comparação com custo equivalente de gasolina | Aprovado |
| Simulação de progresso de carga | Bateria: 20% -> 80% | Barra de progresso exibida do início ao fim | Aprovado |

---

## Roadmap

Este projeto é desenvolvido em 4 sprints. O Sprint 1 (atual) cobre estruturas de dados e algoritmos fundamentais.

**Sprint 1 (concluído):** Simulador de sessão de recarga, estruturas condicionais, repetição e validações.

**Sprints 2–4 (planejados):**
- Integração com protocolo OCPP (Open Charge Point Protocol).
- Banco de dados persistente (SQL ou NoSQL).
- Autenticação com JWT/OAuth.
- Dashboard web com Flask ou React.
- Previsão de demanda com Machine Learning.
- Integração com sistemas de pagamento.
- Exportação de relatórios em PDF.

---

## Autores

Desenvolvedor: [Seu Nome]  
Disciplina: Data Structures and Algorithms — FIAP  
Desafio: GoodWe — ChargeGrid Intelligence  
Contato: [seu.email@fiap.com.br]

---

Versão 1.0 — Sprint 1 — Maio 2026