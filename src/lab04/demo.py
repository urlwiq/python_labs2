import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lab03.base import Server
from lab03.collection import ServerCollection
from lab04.models import WebServer, DatabaseServer, FileServer
from lab04.interfaces import IManageable, IMonitorable, IComparable, IPrintable


def print_all_printable(items):
    print("\n=== Вывод через интерфейс IPrintable ===")
    for item in items:
        print(f"  {item.to_string()}")


def compare_by_interface(obj1, obj2):
    if isinstance(obj1, IComparable) and isinstance(obj2, IComparable):
        result = obj1.compare_to(obj2)
        if result < 0:
            return f"{obj1.hostname} < {obj2.hostname}"
        elif result > 0:
            return f"{obj1.hostname} > {obj2.hostname}"
        else:
            return f"{obj1.hostname} == {obj2.hostname}"
    return "Объекты не поддерживают сравнение"


def get_all_loads(monitorable_items):
    loads = {}
    for item in monitorable_items:
        loads[item.hostname] = item.calculate_load()
    return loads


def scenario_1_basic_interfaces():
    print("СЦЕНАРИЙ 1: Базовые интерфейсы")
    
    web = WebServer("web-01", "10.0.0.1", "example.com", 100, "active", True)
    db = DatabaseServer("db-01", "10.0.0.2", "PostgreSQL", 500, 200, "active")
    file = FileServer("file-01", "10.0.0.3", "FTP", 150, "active")
    
    print("\nПроверка реализации интерфейсов:")
    print(f"  web - IComparable: {isinstance(web, IComparable)}")
    print(f"  web - IPrintable: {isinstance(web, IPrintable)}")
    print(f"  db - IComparable: {isinstance(db, IComparable)}")
    print(f"  file - IPrintable: {isinstance(file, IPrintable)}")
    
    web.handle_request()
    web.handle_request()
    db.execute_query("SELECT * FROM users")
    file.upload_file("doc.pdf", 10)
    
    print(f"\nget_info():")
    print(f"  WebServer: {web.get_info()}")
    print(f"  DatabaseServer: {db.get_info()}")
    print(f"  FileServer: {file.get_info()}")
    
    print(f"\ncalculate_load():")
    print(f"  WebServer: {web.calculate_load():.1f}%")
    print(f"  DatabaseServer: {db.calculate_load():.1f}%")
    print(f"  FileServer: {file.calculate_load():.1f}%")


def scenario_2_universal_functions():
    print("СЦЕНАРИЙ 2: Универсальные функции через интерфейсы")
    
    web1 = WebServer("alpha-web", "10.0.0.1", "alpha.com", 100, "active", True)
    web2 = WebServer("beta-web", "10.0.0.2", "beta.com", 100, "active", False)
    db1 = DatabaseServer("gamma-db", "10.0.0.3", "PostgreSQL", 1000, 300, "active")
    db2 = DatabaseServer("delta-db", "10.0.0.4", "MySQL", 500, 200, "active")
    file = FileServer("epsilon-file", "10.0.0.5", "NFS", 200, "active")
    
    web1.handle_request()
    web1.handle_request()
    db1.execute_query("SELECT * FROM users")
    file.upload_file("data.bin", 50)
    
    printable_objects = [web1, web2, db1, db2, file]
    print_all_printable(printable_objects)
    
    print("\nСравнение через IComparable:")
    print(f"  {compare_by_interface(web1, web2)}")
    print(f"  {compare_by_interface(db1, db2)}")
    
    loads = get_all_loads([web1, db1, file])
    print("\nНагрузка через IMonitorable:")
    for name, load in loads.items():
        print(f"  {name}: {load:.1f}%")


def scenario_3_collection_filtering():
    print("СЦЕНАРИЙ 3: Фильтрация коллекции по интерфейсам")
    
    infra = ServerCollection("Cloud")
    
    infra.add(WebServer("web-01", "10.0.0.1", "app.com", 200, "active", True))
    infra.add(WebServer("web-02", "10.0.0.2", "api.com", 150, "active", False))
    infra.add(DatabaseServer("db-01", "10.0.0.3", "PostgreSQL", 2000, 500, "active"))
    infra.add(DatabaseServer("db-02", "10.0.0.4", "MySQL", 1000, 300, "active"))
    infra.add(FileServer("storage-01", "10.0.0.5", "NFS", 300, "active"))
    infra.add(FileServer("backup-01", "10.0.0.6", "FTP", 100, "inactive"))
    infra.add(Server("monitoring", "10.0.0.7", 50, "active"))
    
    print(f"\nВсего серверов: {len(infra)}")
    
    printable_items = [item for item in infra if isinstance(item, IPrintable)]
    comparable_items = [item for item in infra if isinstance(item, IComparable)]
    
    print(f"\nIPrintable ({len(printable_items)}): {[item.hostname for item in printable_items]}")
    print(f"IComparable ({len(comparable_items)}): {[item.hostname for item in comparable_items]}")
    
    print("\nПолиморфизм через интерфейс (без условий):")
    print("  Плохо: if isinstance(obj, WebServer): ...")
    print("  Хорошо: obj.to_string()")
    print("\n  to_string():")
    for item in printable_items[:5]:
        print(f"    {item.to_string()}")


def main():
    print("ЛАБОРАТОРНАЯ РАБОТА №4")
    print("Интерфейсы и абстрактные классы (ABC)")
    
    scenario_1_basic_interfaces()
    scenario_2_universal_functions()
    scenario_3_collection_filtering()
    print("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")


if __name__ == "__main__":
    main()