def get_yield_ranking(devices_list):
    """Retorna a lista de dispositivos ordenada por rendimento usando lambda."""
    return sorted( devices_list,key= lambda x: x['rendimento'], reverse=True)

def update_device_status_logic(devices_list,devices_id,new_status):
    """Busca um dispositivo pelo ID e atualiza seu status."""
    for dev in devices_list:
        if dev['id'] == devices_id:
            dev['status'] = new_status
            return True
    return False