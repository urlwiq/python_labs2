import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lab06.container import TypedCollection, Displayable, Scorable, D, S
from lab03.base import Server
from lab03.models import WebServer, DatabaseServer, FileServer


def scenario_1_basic():
    print("СЦЕНАРИЙ 1: Базовый")
    
    servers: TypedCollection[Server] = TypedCollection()
    
    web = WebServer("web-01", "10.0.0.1", "example.com", 100, "active", True)
    db = DatabaseServer("db-01", "10.0.0.2", "PostgreSQL", 500, 200, "active")
    file = FileServer("file-01", "10.0.0.3", "FTP", 150, "active")
    
    servers.add(web)
    servers.add(db)
    servers.add(file)
    
    print(f"Добавлено {len(servers)} серверов")
    
    print("\nВсе серверы:")
    for s in servers.get_all():
        print(f"  {s.hostname} ({s.get_server_type()})")



def scenario_2_find_filter_map():
    print("СЦЕНАРИЙ 2: find, filter, map")
    
    servers: TypedCollection[Server] = TypedCollection()
    
    servers.add(WebServer("alpha-web", "10.0.0.1", "alpha.com", 100, "active", True))
    servers.add(WebServer("beta-web", "10.0.0.2", "beta.com", 100, "active", False))
    servers.add(DatabaseServer("gamma-db", "10.0.0.3", "PostgreSQL", 1000, 500, "active"))
    servers.add(DatabaseServer("delta-db", "10.0.0.4", "MySQL", 800, 300, "inactive"))
    servers.add(FileServer("storage-01", "10.0.0.5", "NFS", 300, "active"))
    for s in servers:
        if s.status != "active":
            s.activate()
    for s in servers:
        if hasattr(s, "handle_request"):
            s.handle_request()
            if "alpha" in s.hostname:
                s.handle_request()
                s.handle_request()
        if hasattr(s, "execute_query"):
            s.execute_query("SELECT * FROM table")
    
    print("\n1. find() - поиск сервера с именем 'alpha-web':")
    found = servers.find(lambda s: s.hostname == "alpha-web")
    if found:
        print(f"   Найден: {found.hostname}")
    
    print("\n2. find() - поиск сервера с именем 'not-exist':")
    not_found = servers.find(lambda s: s.hostname == "not-exist")
    if not_found is None:
        print("   Не найден (вернулся None)")
    
    print("\n3. filter() - только активные серверы:")
    active = servers.filter(lambda s: s.status == "active")
    for s in active:
        print(f"   {s.hostname} - {s.status}")
    
    print("\n4. filter() - только веб-серверы:")
    web_servers = servers.filter(lambda s: s.__class__.__name__ == "WebServer")
    for s in web_servers:
        print(f"   {s.hostname}")
    
    print("\n5. map() - преобразование в строки (list[str]):")
    names: list[str] = servers.map(lambda s: s.hostname)
    print(f"   {names}")
    
    print("\n6. map() - преобразование в нагрузку (list[float]):")
    loads: list[float] = servers.map(lambda s: s.calculate_load())
    for i, load in enumerate(loads):
        print(f"   {servers[i].hostname}: {load:.1f}%")
    
    print("\n7. map() - преобразование в кортежи (list[tuple]):")
    tuples: list[tuple] = servers.map(lambda s: (s.hostname, s.calculate_load()))
    for t in tuples:
        print(f"   {t}")


def scenario_3_protocols():
    print("СЦЕНАРИЙ 3: Protocol и bound")
    
    print("\n1. TypedCollection[D] - только объекты с методом display():")
    displayable_collection: TypedCollection[D] = TypedCollection()
    
    web = WebServer("web-01", "10.0.0.1", "example.com", 100, "active", True)
    db = DatabaseServer("db-01", "10.0.0.2", "PostgreSQL", 500, 200, "active")
    file = FileServer("file-01", "10.0.0.3", "FTP", 150, "active")
    
    displayable_collection.add(web)
    displayable_collection.add(db)
    displayable_collection.add(file)
    
    print(f"Добавлено {len(displayable_collection)} объектов")
    
    print("\n   Вызов display():")
    for obj in displayable_collection.get_all():
        print(f"     {obj.display()}")
    
    print("\n2. TypedCollection[S] - только объекты с методом score():")
    scorable_collection: TypedCollection[S] = TypedCollection()
    
    scorable_collection.add(web)
    scorable_collection.add(db)
    scorable_collection.add(file)
    
    print(f"Добавлено {len(scorable_collection)} объектов")
    
    print("\n   Вызов score():")
    for obj in scorable_collection.get_all():
        print(f"     {obj.hostname}: score = {obj.score():.1f}")
    
    print("\n3. filter() в TypedCollection[D]:")
    active = displayable_collection.filter(lambda s: s.status == "active")
    for s in active:
        print(f"   {s.display()}")
    
    print("\n4. map() в TypedCollection[D] -> имена:")
    names = displayable_collection.map(lambda s: s.hostname)
    print(f"   {names}")


def main():
    print("ЛАБОРАТОРНАЯ РАБОТА №6")
    print("Generics и typing")
    
    scenario_1_basic()
    scenario_2_find_filter_map()
    scenario_3_protocols()
    print("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
    


if __name__ == "__main__":
    main()