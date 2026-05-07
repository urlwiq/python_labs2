import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lab03.base import Server
from lab03.models import WebServer, DatabaseServer, FileServer
from lab05.collection import ServerCollection
from lab05.strategies import *


def create_test_collection():
    infra = ServerCollection("TestDC")
    
    infra.add(WebServer("zebra-web", "10.0.0.1", "zebra.com", 100, "active", True))
    infra.add(WebServer("alpha-web", "10.0.0.2", "alpha.com", 200, "active", False))
    infra.add(DatabaseServer("gamma-db", "10.0.0.3", "PostgreSQL", 1000, 500, "active"))
    infra.add(DatabaseServer("delta-db", "10.0.0.4", "MySQL", 800, 300, "active"))
    infra.add(FileServer("storage-01", "10.0.0.5", "NFS", 300, "active"))
    
    for s in infra:
        if isinstance(s, WebServer):
            s.handle_request()
            if "alpha" in s.hostname:
                s.handle_request()
                s.handle_request()
        elif isinstance(s, DatabaseServer):
            s.execute_query("SELECT * FROM table")
    
    return infra


def main():
    print("ЛАБОРАТОРНАЯ РАБОТА №5")
    print("Функции как аргументы. Стратегии и делегаты.")
    
    infra = create_test_collection()
    
    print("СЦЕНАРИЙ 1: Сортировка тремя разными стратегиями")
    
    print("\n1. Сортировка по hostname (функция by_hostname):")
    for s in sorted(infra, key=by_hostname):
        print(f"   {s.hostname}")
    
    print("\n2. Сортировка по нагрузке (lambda):")
    for s in sorted(infra, key=lambda x: x.calculate_load()):
        print(f"   {s.hostname}: {s.calculate_load():.1f}%")
    
    print("\n3. Сортировка по нагрузке убывание (метод sort_by):")
    infra2 = create_test_collection()
    infra2.sort_by(by_load_desc)
    for s in infra2:
        print(f"   {s.hostname}: {s.calculate_load():.1f}%")
    
    print("СЦЕНАРИЙ 2: Фильтрация, фабрика функций и map")
    
    print("\n4. Фильтрация через filter() (только активные):")
    for s in filter(is_active, infra):
        print(f"   {s.hostname}")
    
    print("\n5. Фильтрация через метод filter_by() (только веб-серверы):")
    for s in infra.filter_by(is_web_server):
        print(f"   {s.hostname}")
    
    print("\n6. Фабрика функций (нагрузка > 20%):")
    high_load = has_high_load(20)
    for s in filter(high_load, infra):
        print(f"   {s.hostname}: {s.calculate_load():.1f}%")
    
    print("\n7. Преобразование через map() (имена серверов):")
    names = list(map(lambda s: s.hostname, infra))
    print(f"   {names}")
    
    print("СЦЕНАРИЙ 3: Цепочка операций и callable-объект")
    
    print("\n8. Цепочка: filter() -> sort_by() -> apply():")
    (create_test_collection()
        .filter_by(is_active)
        .sort_by(by_load_desc)
        .apply(log_server))
    
    print("\n9. Callable-объект как стратегия (LoadSortStrategy):")
    strategy = LoadSortStrategy(reverse=True)
    for s in sorted(infra, key=strategy):
        print(f"   {s.hostname}: {s.calculate_load():.1f}%")
    
    print("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")


if __name__ == "__main__":
    main()