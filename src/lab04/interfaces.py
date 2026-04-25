from abc import ABC, abstractmethod


class IManageable(ABC):
    @abstractmethod
    def activate(self):
        pass
    
    @abstractmethod
    def deactivate(self):
        pass
    
    @abstractmethod
    def get_status(self):
        pass


class IMonitorable(ABC):
    @abstractmethod
    def get_load(self):
        pass
    
    @abstractmethod
    def get_info(self):
        pass


class IComparable(ABC):
    @abstractmethod
    def compare_to(self, other):
        pass


class IPrintable(ABC):
    @abstractmethod
    def to_string(self):
        pass