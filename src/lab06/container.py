import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import TypeVar, Generic, Callable, Optional, Protocol
from lab03.base import Server
from lab03.models import WebServer, DatabaseServer, FileServer


T = TypeVar('T')
R = TypeVar('R')


class TypedCollection(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []
    
    def add(self, item: T) -> None:
        self._items.append(item)
    
    def remove(self, item: T) -> None:
        self._items.remove(item)
    
    def get_all(self) -> list[T]:
        return list(self._items)
    
    def find_by_name(self, name: str) -> Optional[T]:
        for item in self._items:
            if hasattr(item, 'hostname') and item.hostname == name:
                return item
        return None
    
    def find_by_ip(self, ip: str) -> Optional[T]:
        for item in self._items:
            if hasattr(item, 'ip_address') and item.ip_address == ip:
                return item
        return None
    
    def find_by_status(self, status: str) -> list[T]:
        result = []
        for item in self._items:
            if hasattr(item, 'status') and item.status == status:
                result.append(item)
        return result
    
    def remove_at(self, index: int) -> T:
        if 0 <= index < len(self._items):
            return self._items.pop(index)
        raise IndexError("Индекс вне диапазона")
    
    def sort_by_hostname(self, reverse: bool = False) -> None:
        self._items.sort(key=lambda x: x.hostname if hasattr(x, 'hostname') else str(x), reverse=reverse)
    
    def get_active_servers(self) -> list[T]:
        return [item for item in self._items if hasattr(item, 'status') and item.status == 'active']
    
    def __len__(self) -> int:
        return len(self._items)
    
    def __iter__(self):
        return iter(self._items)
    
    def __getitem__(self, index: int) -> T:
        return self._items[index]
    
    def find(self, predicate: Callable[[T], bool]) -> Optional[T]:
        for item in self._items:
            if predicate(item):
                return item
        return None
    
    def filter(self, predicate: Callable[[T], bool]) -> list[T]:
        return [item for item in self._items if predicate(item)]
    
    def map(self, transform: Callable[[T], R]) -> list[R]:
        return [transform(item) for item in self._items]
    def __str__(self) -> str:
        return f"TypedCollection({len(self._items)} элементов)"

class Displayable(Protocol):
    def display(self) -> str:
        ...

class Scorable(Protocol):
    def score(self) -> float:
        ...


D = TypeVar('D', bound=Displayable)
S = TypeVar('S', bound=Scorable)


def add_protocol_methods():
    if not hasattr(Server, 'display'):
        Server.display = lambda self: f"{self.get_server_type()}: {self.hostname} ({self.ip_address})"
    if not hasattr(Server, 'score'):
        Server.score = lambda self: self.calculate_load()

add_protocol_methods()