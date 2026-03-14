
import re

def validate_hostname(hostname):
    """Проверка имени сервера"""
    if not isinstance(hostname, str):
        raise TypeError("Hostname должен быть строкой")
    if not hostname.strip():
        raise ValueError("Hostname не может быть пустым")
    if len(hostname) > 63:
        raise ValueError("Hostname не может быть длиннее 63 символов")
    if not re.match(r'^[a-zA-Z0-9\-]+$', hostname):
        raise ValueError("Hostname может содержать только буквы, цифры и дефис")
    return hostname.strip()

def validate_ip_address(ip):
    """Проверка IP-адреса (формат IPv4)"""
    if not isinstance(ip, str):
        raise ValueError("IP-адрес должен быть строкой")
    pattern = r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$'
    match = re.match(pattern, ip)
    if not match:
        raise ValueError("Неверный формат IP-адреса. Используйте формат XXX.XXX.XXX.XXX")
    for octet in match.groups():
        if int(octet) > 255:
            raise ValueError(f"Октет {octet} превышает 255")
    return ip

def validate_status(status):
    """Проверка статуса сервера"""
    valid_statuses = ['active', 'inactive', 'maintenance']
    if status not in valid_statuses:
        raise ValueError(f"Статус должен быть одним из: {', '.join(valid_statuses)}")
    return status

def validate_connections(connections, max_connections=None):
    """Проверка количества подключений"""
    if not isinstance(connections, int):
        raise ValueError("Количество подключений должно быть целым числом")
    if connections < 0:
        raise ValueError("Количество подключений не может быть отрицательным")
    if max_connections is not None and connections > max_connections:
        raise ValueError(f"Количество подключений не может превышать {max_connections}")
    return connections

def validate_max_connections(max_conn):
    """Проверка максимального количества подключений"""
    if not isinstance(max_conn, int):
        raise ValueError("Максимальное количество подключений должно быть целым числом")
    if max_conn <= 0:
        raise ValueError("Максимальное количество подключений должно быть положительным")
    if max_conn > 1000:
        raise ValueError("Максимальное количество подключений не может превышать 1000")
    return max_conn
