
from model import Server
from lab03.collection import ServerCollection


def scenario_1_basic_operations():
    print("СЦЕНАРИЙ 1: Базовые операции (добавление, удаление, вывод)")

    print("\n1. Создание серверов:")
    web_server = Server("web-01", "192.168.1.10", 100, "inactive")
    db_server = Server("db-01", "192.168.1.20", 200, "inactive")
    cache_server = Server("cache-01", "192.168.1.30", 50, "inactive")
    
    print(f"   Созданы: {web_server.hostname}, {db_server.hostname}, {cache_server.hostname}")
    
    print("\n2. Создание коллекции 'Production':")
    infra = ServerCollection("Production")
    
    print("\n3. Добавление серверов в коллекцию:")
    infra.add(web_server)
    infra.add(db_server)
    infra.add(cache_server)
    print("\n4. Вывод всех серверов (get_all):")
    all_servers = infra.get_all()
    for server in all_servers:
        print(f"   - {server.hostname} ({server.ip_address}), статус: {server.status}")
    
    print(f"\n5. Количество серверов в коллекции: {len(infra)}")
    print("\n6. Удаление сервера cache-01:")
    infra.remove(cache_server)
    
    print("\n7. Вывод всех серверов после удаления:")
    for server in infra:  # используем __iter__
        print(f"   - {server.hostname} ({server.ip_address})")
    
    print(f"\n8. Количество серверов после удаления: {len(infra)}")


def scenario_2_search_and_constraints():
    print("СЦЕНАРИЙ 2: Поиск и проверка ограничений")
    
    print("\n1. Создание коллекции и добавление серверов:")
    infra = ServerCollection("TestEnv")
    
    s1 = Server("app-01", "10.0.0.1", 150, "active")
    s2 = Server("app-02", "10.0.0.2", 150, "inactive")
    s3 = Server("db-master", "10.0.0.3", 500, "active")
    s4 = Server("db-slave", "10.0.0.4", 500, "maintenance")
    
    infra.add(s1)
    infra.add(s2)
    infra.add(s3)
    infra.add(s4)
    
    print(f"   Добавлено {len(infra)} серверов")
    
    print("\n2. Поиск сервера по hostname 'db-master':")
    found = infra.find_by_name("db-master")
    if found:
        print(f"   Найден: {found.hostname} ({found.ip_address}), статус: {found.status}")
    else:
        print("   Сервер не найден")
    
    print("\n3. Поиск сервера по IP '10.0.0.2':")
    found = infra.find_by_ip("10.0.0.2")
    if found:
        print(f"   Найден: {found.hostname} ({found.ip_address}), статус: {found.status}")
    else:
        print("   Сервер не найден")
    
    print("\n4. Поиск по несуществующему IP '10.0.0.99':")
    found = infra.find_by_ip("10.0.0.99")
    if found:
        print(f"   Найден: {found.hostname}")
    else:
        print("   Сервер не найден (вернулся None)")
    
    print("\n5. Поиск всех серверов со статусом 'active':")
    active_servers = infra.find_by_status("active")
    print(f"   Найдено {len(active_servers)} серверов:")
    for server in active_servers:
        print(f"   - {server.hostname}")
    
    print("\n6. Поиск серверов в режиме 'maintenance':")
    maintenance_servers = infra.find_by_status("maintenance")
    print(f"   Найдено {len(maintenance_servers)} серверов:")
    for server in maintenance_servers:
        print(f"   - {server.hostname}")
    
    print("\n7. Проверка ограничения на дубликаты (тот же IP):")
    try:
        duplicate_server = Server("duplicate", "10.0.0.1", 100, "inactive")
        infra.add(duplicate_server)
        print("   ОШИБКА: Дубликат не должен был добавиться!")
    except ValueError as e:
        print(f"   ✓ Ограничение сработало: {e}")
    
    print("\n8. Проверка типа при добавлении (не Server):")
    try:
        infra.add("это строка, а не сервер")
        print("   ОШИБКА: Строка не должна была добавиться!")
    except TypeError as e:
        print(f"   ✓ Проверка типа сработала: {e}")


def scenario_3_indexing_sorting_filtering():
    print("СЦЕНАРИЙ 3: Индексация, сортировка и фильтрация")
    
    print("\n1. Создание коллекции с 5 серверами:")
    infra = ServerCollection("DataCenter")
    
    servers = [
        Server("zebra-01", "192.168.1.10", 100, "active"),
        Server("alpha-01", "192.168.1.20", 200, "inactive"),
        Server("main-01", "192.168.1.30", 300, "active"),
        Server("beta-01", "192.168.1.40", 150, "maintenance"),
        Server("gamma-01", "192.168.1.50", 250, "active")
    ]
    
    for server in servers:
        infra.add(server)
    
    print(f"   Добавлено {len(infra)} серверов")
    
    print("\n2. Исходный порядок серверов:")
    for i, server in enumerate(infra):
        print(f"   [{i}] {server.hostname} ({server.status})")
    
    print("\n3. Доступ к серверам по индексу:")
    print(f"   infra[0] = {infra[0].hostname}")
    print(f"   infra[2] = {infra[2].hostname}")
    print(f"   infra[-1] = {infra[-1].hostname}")
    
    print("\n4. Удаление сервера по индексу 1:")
    removed = infra.remove_at(1)
    print(f"   Удалён: {removed.hostname}")
    print(f"   Осталось серверов: {len(infra)}")
    
    print("\n   Серверы после удаления:")
    for i, server in enumerate(infra):
        print(f"   [{i}] {server.hostname}")
    
    print("\n5. Сортировка по hostname (алфавитный порядок):")
    infra.sort_by_hostname()
    for i, server in enumerate(infra):
        print(f"   [{i}] {server.hostname}")
    
    print("\n6. Сортировка по hostname (обратный порядок):")
    infra.sort_by_hostname(reverse=True)
    for i, server in enumerate(infra):
        print(f"   [{i}] {server.hostname}")
    
    print("\n7. Фильтрация: только активные серверы (get_active_servers):")
    active_collection = infra.get_active_servers()
    print(f"   Найдено активных серверов: {len(active_collection)}")
    for server in active_collection:
        print(f"   - {server.hostname} (статус: {server.status})")
    
    print("\n8. Работа с отфильтрованной коллекцией:")
    print(f"   Тип: {type(active_collection).__name__}")
    print(f"   Можно использовать len(): {len(active_collection)}")
    print("   Можно итерировать:")
    for server in active_collection:
        print(f"     → {server.hostname}")


def main():
    print("Демонстрация на 3 сценария")
    scenario_1_basic_operations()
    scenario_2_search_and_constraints()
    scenario_3_indexing_sorting_filtering()
    

if __name__ == "__main__":
    main()