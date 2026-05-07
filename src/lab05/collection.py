import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lab02.collection import ServerCollection as BaseCollection


class ServerCollection(BaseCollection):
    def __init__(self, name="Infrastructure"):
        super().__init__(name)
    
    def sort_by(self, key_func, reverse=False):
        self._items.sort(key=key_func, reverse=reverse)
        return self
    
    def filter_by(self, predicate):
        result = ServerCollection(f"{self._name}_filtered")
        result._items = [item for item in self._items if predicate(item)]
        return result
    
    def apply(self, func):
        for i, item in enumerate(self._items):
            self._items[i] = func(item)
        return self