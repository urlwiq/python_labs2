from model import Server
class ServerCollection:

    def __init__(self, name="Infrastructure"):
        self._name = name
        self._items = []

    def add(self,server):
        if not isinstance(server,Server):
            raise TypeError(f"Можно добавлять только объекты Server")
        for existing in self._items:
            if existing.ip_address == server.ip_address:
                raise ValueError(f"Сервер с IP'{server.ip_address}' уже существует")
        self._items.append(server)
        print(f"Сервер '{server.hostname}' добавлен в коллекцию '{self._name}'")

    def remove(self, server):
        if server not in self._items:
            raise ValueError("Сервер не найден в коллекции")
        
        self._items.remove(server)
        print(f"Сервер {server.hostname} удален из коллекции '{self._name}'")

    def get_all(self):
        return self._items.copy()
    
    def find_by_name(self, hostname):
        for server in self._items:
            if server.hostname == hostname:
                return server
        return None
    
    def find_by_ip(self, ip_address):
        for server in self._items:
            if server.ip_address == ip_address:
                return server
        return None
    
    def find_by_status(self, status):
        result = []
        
        for server in self._items:  
            if server.status == status:  
                result.append(server)  
        return result
    def __len__(self):
        return len(self._items)
    
    def __iter__(self):
        return iter(self._items)
    
    def __getitem__(self, index):
        return self._items[index]
    def remove_at(self, index):
        if 0 <= index < len(self._items):
            return self._items.pop(index)
        raise IndexError("Индекс вне диапазона")
    
    def sort_by_hostname(self, reverse=False):
        self._items.sort(key=lambda s: s.hostname, reverse=reverse)
    
    def get_active_servers(self):
        result = ServerCollection()
        for server in self._items:
            if server.status == 'active':
                result.add(server)
        return result
