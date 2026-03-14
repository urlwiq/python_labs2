from datetime import datetime
import validate
class Server:
    os_type = "Linux"

    def __init__(self, hostname, ip_address, max_connections=100, status="inactive"):
        self._hostname = validate.validate_hostname(hostname)
        self._ip_address = validate.validate_ip_address(ip_address)
        self._max_connections = validate.validate_max_connections(max_connections)
        self._status = validate.validate_status(status)
        
        self._current_connections = 0
        self._created_at = datetime.now()
        self._users = [] 
        
    @property
    def hostname(self):
        return self._hostname
    
    @property
    def ip_address(self):
        return self._ip_address
    
    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, new_status):
        old_status = self._status
        validated_status = validate.validate_status(new_status)
        
        if old_status == 'active' and new_status == 'maintenance':
            if self._current_connections > 0:
                raise ValueError("Нельзя перевести в обслуживание сервер с активными подключениями")
        
        self._status = validated_status
        print(f"Статус сервера {self._hostname} изменен: {old_status} -> {new_status}")
    
    @property
    def max_connections(self):
        return self._max_connections
    
    @max_connections.setter
    def max_connections(self, value):
        old_max = self._max_connections
        new_max = validate.validate_max_connections(value)
        
        if new_max < self._current_connections:
            raise ValueError(f"Нельзя установить лимит {new_max} меньше текущих подключений ({self._current_connections})")
        
        self._max_connections = new_max
        print(f"Лимит подключений изменен: {old_max} -> {new_max}")
    
    @property
    def current_connections(self):
        return self._current_connections
    
    @property
    def created_at(self):
        return self._created_at
    
    def connect_user(self, username):
        if self._status != "active":
            raise Exception(f"Невозможно подключиться. Сервер в статусе: {self._status}")
        
        if self._current_connections >= self._max_connections:
            raise Exception(f"Достигнут лимит подключений ({self._max_connections})")
        
        if username in self._users:
            print(f"Пользователь {username} уже подключен к серверу")
            return False
        
        self._users.append(username)
        self._current_connections += 1
        print(f"Пользователь {username} подключен к серверу {self._hostname}")
        print(f"Текущих подключений: {self._current_connections}/{self._max_connections}")
        return True
    
    def disconnect_user(self, username):
        if username not in self._users:
            print(f"Пользователь {username} не найден среди подключенных")
            return False
        
        self._users.remove(username)
        self._current_connections -= 1
        print(f"Пользователь {username} отключен от сервера {self._hostname}")
        print(f"Осталось подключений: {self._current_connections}")
        return True
    
    def activate(self):
        if self._status == "active":
            print(f"Сервер {self._hostname} уже активен")
            return
        
        self.status = "active" 
        print(f"Сервер {self._hostname} активирован")
    
    def deactivate(self):
        if self._status == "inactive":
            print(f"Сервер {self._hostname} уже неактивен")
            return
        
        if self._current_connections > 0:
            print(f"Невозможно деактивировать: есть активные подключения ({self._current_connections})")
            return
        
        self.status = "inactive"
        print(f"Сервер {self._hostname} деактивирован")
    
    def maintenance_mode(self):
        if self._status == "maintenance":
            print(f"Сервер {self._hostname} уже в режиме обслуживания")
            return
        
        if self._current_connections > 0:
            print(f"Невозможно перевести в обслуживание: есть активные подключения ({self._current_connections})")
            return
        
        self.status = "maintenance"
        print(f"Сервер {self._hostname} переведен в режим обслуживания")
    
    def __str__(self):
        status_emoji = {
            "active": "🟢",
            "inactive": "⚫",
            "maintenance": "🟡"
        }
        return (f"{status_emoji.get(self._status, '⚪')} Сервер {self._hostname} ({self._ip_address})\n"
                f"   Статус: {self._status.upper()}\n"
                f"   Подключения: {self._current_connections}/{self._max_connections}\n"
                f"   ОС: {self.os_type}\n"
                f"   Создан: {self._created_at.strftime('%Y-%m-%d %H:%M')}")
    
    def __repr__(self):
        return (f"Server(hostname='{self._hostname}', "
                f"ip_address='{self._ip_address}', "
                f"max_connections={self._max_connections}, "
                f"status='{self._status}')")
    
    def __eq__(self, other):
        if not isinstance(other, Server):
            return False
        return self._ip_address == other._ip_address