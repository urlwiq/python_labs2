from typing import List, Optional, Callable
from lab02.collection import ServerCollection
from lab03.base import Server
from lab03.models import WebServer, DatabaseServer, FileServer
from lab07.exceptions import ItemNotFoundError, DuplicateItemError


class ServerApplication:
    def __init__(self, collection: ServerCollection = None) -> None:
        self._collection = collection if collection else ServerCollection()
    
    @property
    def collection(self) -> ServerCollection:
        return self._collection
    
    
    def add_web_server(self, hostname: str, ip_address: str, domain: str,
                       max_connections: int = 100, status: str = "inactive",
                       ssl_enabled: bool = False) -> WebServer:
        if self._collection.find_by_ip(ip_address):
            raise DuplicateItemError(f"Сервер с IP {ip_address} уже существует")
        
        server = WebServer(hostname, ip_address, domain, max_connections, status, ssl_enabled)
        self._collection.add(server)
        return server
    
    def add_database_server(self, hostname: str, ip_address: str, db_type: str,
                            storage_gb: int, max_connections: int = 200,
                            status: str = "inactive") -> DatabaseServer:
        if self._collection.find_by_ip(ip_address):
            raise DuplicateItemError(f"Сервер с IP {ip_address} уже существует")
        
        server = DatabaseServer(hostname, ip_address, db_type, storage_gb, max_connections, status)
        self._collection.add(server)
        return server
    
    def add_file_server(self, hostname: str, ip_address: str, protocol: str,
                        max_connections: int = 150, status: str = "inactive") -> FileServer:
        if self._collection.find_by_ip(ip_address):
            raise DuplicateItemError(f"Сервер с IP {ip_address} уже существует")
        
        server = FileServer(hostname, ip_address, protocol, max_connections, status)
        self._collection.add(server)
        return server
    
    
    def delete_server_by_ip(self, ip_address: str) -> Server:
        server = self._collection.find_by_ip(ip_address)
        if not server:
            raise ItemNotFoundError(f"Сервер с IP {ip_address} не найден")
        
        self._collection.remove(server)
        return server
    
    
    def find_by_name(self, hostname: str) -> Optional[Server]:
        return self._collection.find_by_name(hostname)
    
    def find_by_ip(self, ip_address: str) -> Optional[Server]:
        return self._collection.find_by_ip(ip_address)
    
    def find_by_status(self, status: str) -> List[Server]:
        return self._collection.find_by_status(status)
    
    def get_active_servers(self) -> List[Server]:
        return self._collection.get_active_servers()
    
    
    def sort_by_hostname(self, reverse: bool = False) -> None:
        self._collection.sort_by_hostname(reverse)
    
    def sort_by_load(self, reverse: bool = False) -> None:
        self._collection._items.sort(key=lambda s: s.calculate_load(), reverse=reverse)
    
    
    def get_all_servers(self) -> List[Server]:
        return self._collection.get_all()
    
    def get_server_count(self) -> int:
        return len(self._collection)
    
    def activate_server(self, ip_address: str) -> None:
        server = self.find_by_ip(ip_address)
        if not server:
            raise ItemNotFoundError(f"Сервер с IP {ip_address} не найден")
        server.activate()