from model import Server

def s1():
    print("\nСЦЕНАРИЙ 1: Базовый")
    s = Server("web-01", "192.168.1.100", 5, "inactive")
    print(f"Создан: {s}")
    print(f"repr: {repr(s)}")
    
    s2 = Server("web-02", "192.168.1.100", 5, "inactive")
    s3 = Server("db-01", "192.168.1.200", 10, "inactive")
    print(f"Равны (один IP): {s == s2}")
    print(f"Равны (разный IP): {s == s3}")

def s2():
    print("\nСЦЕНАРИЙ 2: Свойства и методы")
    s = Server("test", "10.0.0.1", 3, "inactive")
    print(f"Статус: {s.status}, лимит: {s.max_connections}")
    print(f"ОС: {Server.os_type}")
    
    s.status = "active"
    print(f"Статус изменен на: {s.status}")
    
    s.max_connections = 5
    print(f"Лимит изменен на: {s.max_connections}")
    
    s.connect_user("alice")
    s.connect_user("bob")
    print(f"Подключены: {s.current_connections}/{s.max_connections}")

def s3():
    print("\nСЦЕНАРИЙ 3: Состояния")
    s = Server("prod", "10.10.0.1", 3, "inactive")
    
    s.activate()
    print(f"Активирован: {s.status}")
    
    s.connect_user("admin")
    print(f"Admin подключен: {s.current_connections}/{s.max_connections}")
    
    s.disconnect_user("admin")
    s.maintenance_mode()
    print(f"Режим обслуживания: {s.status}")

def s4():
    print("\nСЦЕНАРИЙ 4: Ошибки")
    print("Попытка создать сервер с неверным IP:")
    s_bad = Server("web-01", "300.500.1.1")  
def main():
    print(" Класс Server (IT-инфраструктура)")
    s1(); print()
    s2(); print()
    s3(); print()
    s4()

if __name__ == "__main__":
    main()