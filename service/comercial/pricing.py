from database.database import fares


def calculate_fare(is_premium, is_peak, has_solar):
    if has_solar:
        return fares['cortesia_solar'], 'comum', 'Cortesia solar ☀'

    if is_premium:
        return fares['premium'], 'premium', 'Plano Premium 🔶'

    if is_peak:
        return fares['horario_pico'], 'comum', 'Horário de pico ⚡'

    return fares['base'], 'comum', 'Tarifa base'


def show_fare_table():
    from utils.system import reset_terminal
    from utils.ui import header

    reset_terminal()
    header("TABELA DE TARIFAS")

    from datetime import datetime
    hora = datetime.now().hour
    is_peak = fares['inicio_horario_pico'] <= hora < fares['fim_horario_pico']

    print(f"\nHora atual: {hora}h  |  Horário de pico: {'✅ SIM' if is_peak else '❌ NÃO'}")
    print(f"Pico: {fares['inicio_horario_pico']}h às {fares['fim_horario_pico']}h\n")
    print(f"{'Tarifa':<25} {'R$/kWh':>8}")
    print("-" * 35)
    print(f"{'Base (comum)':<25} {'R$ '+str(fares['base']):.2f:>8}")
    print(f"{'Horário de pico':<25} {'R$ '+str(fares['horario_pico']):.2f:>8}")
    print(f"{'Premium':<25} {'R$ '+str(fares['premium']):.2f:>8}")
    print(f"{'Cortesia solar':<25} {'R$ '+str(fares['cortesia_solar']):.2f:>8}")
    print("\n" + "=" * 40)

    if is_peak:
        print("⚡ Pico ativo — sessões comuns cobradas a R$ 4.90/kWh")
    else:
        print("✅ Fora do pico — tarifa base R$ 4.26/kWh")

    input("\nAperte Enter para voltar...")