import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base import Server
from models import WebServer, DatabaseServer, FileServer
from lab02.collection import ServerCollection

def scenario_1_basic_inheritance():
    print("\n")
    print("СЦЕНАРИЙ 1: Базовое наследование")
    print("")
    
    print("\n1. Создание объектов разных типов:")
    generic = Server("generic-01", "10.0.0.1", 100, "inactive")
    web = WebServer("web-01", "10.0.0.10", "example.com", 200, "active", True)
    db = DatabaseServer("db-01", "10.0.0.20", "PostgreSQL", 500, 300, "active")
    file = FileServer("file-01", "10.0.0.30", "FTP", 150, "active")
    
    print(f"   Создан: {generic.get_server_type()} - {generic.hostname}")
    print(f"   Создан: {web.get_server_type()} - {web.hostname}")
    print(f"   Создан: {db.get_server_type()} - {db.hostname}")
    print(f"   Создан: {file.get_server_type()} - {file.hostname}")
    
    print("\n2. Использование новых методов дочерних классов:")
    
    print(f"\n   Веб-сервер {web.hostname}:")
    web.handle_request()
    web.handle_request()
    print(f"   HTTP статус: {web.get_http_status()}")
    
    print(f"\n   Сервер БД {db.hostname}:")
    db.execute_query("SELECT * FROM users")
    db.execute_query("INSERT INTO logs VALUES ('test')")
    print(f"   Свободно места: {db.get_free_space():.1f} GB")
    
    print(f"\n   Файловый сервер {file.hostname}:")
    file.upload_file("document.pdf", 2.5)
    file.upload_file("image.jpg", 1.2)
    print(f"   Средний размер файла: {file.get_avg_file_size():.1f} MB")
    
    print("\n3. Вывод объектов (переопределённый __str__):")
    print("\n" + str(web))
    print("\n" + str(db))
    print("\n" + str(file))


def scenario_2_polymorphism():
    print("\n")
    print("СЦЕНАРИЙ 2: Полиморфизм")
    print("")
    
    print("\n1. Создание коллекции с разными типами серверов:")
    infra = ServerCollection("DataCenter")
    
    web = WebServer("web-01", "192.168.1.10", "site.com", 200, "active", True)
    db = DatabaseServer("db-01", "192.168.1.20", "PostgreSQL", 1000, 300, "active")
    file = FileServer("file-01", "192.168.1.30", "SMB", 100, "active")
    
    infra.add(web)
    infra.add(db)
    infra.add(file)
    
    print(f"   Добавлено {len(infra)} серверов")
    
    print("\n2. Полиморфизм через get_server_type():")
    for server in infra:
        print(f"   {server.hostname}: {server.get_server_type()}")
    
    print("\n3. Полиморфизм через calculate_load():")
    for server in infra:
        if isinstance(server, WebServer):
            server.handle_request()
            server.handle_request()
        elif isinstance(server, DatabaseServer):
            server.execute_query("SELECT * FROM big_table")
        elif isinstance(server, FileServer):
            server.upload_file("data.bin", 10)
        
        print(f"   {server.hostname}: нагрузка {server.calculate_load():.1f}%")
    
    print("\n4. Проверка типов через isinstance():")
    for server in infra:
        if isinstance(server, WebServer):
            print(f"   {server.hostname} - WebServer (SSL: {server.ssl_enabled})")
        elif isinstance(server, DatabaseServer):
            print(f"   {server.hostname} - DatabaseServer (тип: {server.db_type})")
        elif isinstance(server, FileServer):
            print(f"   {server.hostname} - FileServer (протокол: {server.protocol})")
    
    print("\n5. Работа с коллекцией из ЛР-2:")
    print(f"   Всего серверов: {len(infra)}")
    for server in infra:
        print(f"   - {server.hostname} ({server.get_server_type()})")


def scenario_3_filtering():
    print("\n")
    print("СЦЕНАРИЙ 3: Фильтрация по типу и полиморфизм без условий")
    print("")
    
    print("\n1. Создание разнотипной коллекции:")
    infra = ServerCollection("Cloud")
    
    infra.add(WebServer("web-app", "10.0.0.1", "app.com", 200, "active", True))
    infra.add(WebServer("web-api", "10.0.0.2", "api.com", 150, "active", False))
    infra.add(DatabaseServer("db-main", "10.0.0.3", "PostgreSQL", 2000, 500, "active"))
    infra.add(DatabaseServer("db-replica", "10.0.0.4", "PostgreSQL", 2000, 300, "active"))
    infra.add(FileServer("storage-01", "10.0.0.5", "NFS", 300, "active"))
    infra.add(FileServer("backup-01", "10.0.0.6", "FTP", 100, "inactive"))
    infra.add(Server("monitoring", "10.0.0.7", 50, "active"))
    
    print(f"   Добавлено {len(infra)} серверов")
    
    print("\n2. Фильтрация по типу (только веб-серверы):")
    web_servers = []
    for server in infra:
        if isinstance(server, WebServer):
            web_servers.append(server)
    
    print(f"   Найдено: {len(web_servers)}")
    for server in web_servers:
        print(f"   - {server.hostname} (SSL: {server.ssl_enabled})")
    
    print("\n3. Фильтрация по типу (только серверы БД):")
    db_servers = []
    for server in infra:
        if isinstance(server, DatabaseServer):
            db_servers.append(server)
    
    print(f"   Найдено: {len(db_servers)}")
    for server in db_servers:
        print(f"   - {server.hostname} (тип: {server.db_type})")
    
    print("\n4. Фильтрация по типу (только файловые серверы):")
    file_servers = []
    for server in infra:
        if isinstance(server, FileServer):
            file_servers.append(server)
    
    print(f"   Найдено: {len(file_servers)}")
    for server in file_servers:
        print(f"   - {server.hostname} (протокол: {server.protocol})")
    
    print("\n5. Полиморфизм без условий (Good паттерн):")
    print("   Анти-паттерн: if type(server) == WebServer")
    print("   Good-паттерн: server.get_server_type()")
    
    print("\n   Результат:")
    for server in infra:
        print(f"   {server.hostname} -> {server.get_server_type()}")
    
    print("\n6. Статистика по типам:")
    types = {}
    for server in infra:
        t = server.__class__.__name__
        if t in types:
            types[t] = types[t] + 1
        else:
            types[t] = 1
    
    for t, count in types.items():
        print(f"   {t}: {count} шт.")


def main():
    print("ЛАБОРАТОРНАЯ РАБОТА №3")
    print("Наследование и иерархия классов")
    scenario_1_basic_inheritance()
    scenario_2_polymorphism()
    scenario_3_filtering()

if __name__ == "__main__":
    main()