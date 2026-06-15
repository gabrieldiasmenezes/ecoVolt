from database.database import fares
from datetime import datetime
from utils.system import reset_terminal
from utils.ui import footer, header, separator
from database.settings import LINE_SEPARATOR, SESSION_STATUS,ICON_TYPE

def get_current_fare(session):
    hora = datetime.now().hour
    is_peak = fares['inicio_horario_pico'] <= hora < fares['fim_horario_pico']

    if session['tipo'] == 'premium':
        return session['tarifa_kwh'], "Premium"
    if is_peak:
        return fares['horario_pico'], "Horário de pico"
    return fares['base'], "Tarifa base"


def pricing_service(sessions):
    reset_terminal()
    header("TARIFAÇÃO E FATURAMENTO")

    hora = datetime.now().hour
    is_peak = fares['inicio_horario_pico'] <= hora < fares['fim_horario_pico']

    total_revenue   = sum(s['energia_kwh'] * s['tarifa_kwh'] for s in sessions)
    total_energy    = sum(s['energia_kwh'] for s in sessions)
    active_sessions = [s for s in sessions if s['status'] == 'ativa']
    peak_label      = "⚡ SIM" if is_peak else "✅ NÃO"

    print(f"""
  Horário de pico ({fares['inicio_horario_pico']}h–{fares['fim_horario_pico']}h): {peak_label}

  {LINE_SEPARATOR}
  Tarifa base:       R$ {fares['base']:.2f}/kWh
  Tarifa pico:       R$ {fares['horario_pico']:.2f}/kWh
  Tarifa premium:    R$ {fares['premium']:.2f}/kWh
  Cortesia solar:    R$ {fares['cortesia_solar']:.2f}/kWh
  {LINE_SEPARATOR}

  Sessões ativas:    {len(active_sessions)}
  Energia total:     {total_energy:.1f} kWh
""")
    separator()

    for s in sessions:
        tipo_label   = ICON_TYPE.get(s['tipo'], s['tipo'].upper())
        status_label = SESSION_STATUS.get(s['status'], s['status'].upper())
        valor        = s['energia_kwh'] * s['tarifa_kwh']
        motivo = get_current_fare(s)

        print(f"  Sessão #{s['id']}  {tipo_label}  {status_label}")
        separator()
        print(f"  Energia:  {s['energia_kwh']} kWh")
        print(f"  Tarifa:   R$ {s['tarifa_kwh']:.2f}/kWh  ({motivo})")
        print(f"  Valor:    R$ {valor:.2f}")
        print()

    separator()
    print(f"  💰 Faturamento total:   R$ {total_revenue:.2f}")
    print(f"  ⚡ Energia distribuída: {total_energy:.1f} kWh")

    footer()