"""
Пользовательский интерфейс (CLI)
"""

from typing import Optional
from lab07.app import ServerApplication
from lab07.exceptions import ItemNotFoundError, DuplicateItemError, InvalidInputError


class CLI:
    """Консольный интерфейс для управления серверами"""
    
    def __init__(self, app: ServerApplication) -> None:
        """Инициализация CLI."""
        self._app = app
        self._running = True
    
    def _display_menu(self) -> None:
        """Отображает главное меню."""
        print("\n" + "="*50)
        print("    УПРАВЛЕНИЕ IT-ИНФРАСТРУКТУРОЙ")
        print("="*50)
        print("1. Показать все серверы")
        print("2. Добавить веб-сервер")
        print("3. Добавить сервер БД")
        print("4. Добавить файловый сервер")
        print("5. Найти сервер по имени")
        print("6. Найти сервер по IP")
        print("7. Показать активные серверы")
        print("8. Сортировать серверы")
        print("9. Удалить сервер")
        print("0. Выход")
        print("-"*50)
    
    def _get_choice(self) -> int:
        """Получает выбор пользователя с обработкой ошибок."""
        try:
            choice = int(input("Выберите пункт: "))
            return choice
        except ValueError:
            raise InvalidInputError("Введите число от 0 до 9")
    
    def _show_servers(self) -> None:
        """Показывает все серверы в табличном виде."""
        servers = self._app.get_all_servers()
        if not servers:
            print("\n⚠️ Серверов нет. Добавьте хотя бы один.")
            return
        
        print("\n" + "-"*80)
        print(f"{'#'} | {'Имя':<20} | {'IP':<15} | {'Тип':<15} | {'Статус':<10} | {'Нагрузка':<8}")
        print("-"*80)
        for i, s in enumerate(servers, 1):
            load = s.calculate_load()
            status_icon = "🟢" if s.status == "active" else "⚫" if s.status == "inactive" else "🟡"
            print(f"{i:<2} | {s.hostname:<20} | {s.ip_address:<15} | {s.get_server_type():<15} | {status_icon} {s.status:<7} | {load:>5.1f}%")
        print("-"*80)
    
    def _add_web_server(self) -> None:
        """Добавляет веб-сервер."""
        print("\n--- Добавление веб-сервера ---")
        try:
            hostname = input("Имя хоста: ").strip()
            if not hostname:
                raise InvalidInputError("Имя хоста не может быть пустым")
            
            ip_address = input("IP-адрес: ").strip()
            if not ip_address:
                raise InvalidInputError("IP-адрес не может быть пустым")
            
            domain = input("Домен: ").strip()
            if not domain:
                domain = "default.com"
            
            ssl = input("Включить SSL? (y/n): ").lower() == 'y'
            
            server = self._app.add_web_server(hostname, ip_address, domain, 100, "inactive", ssl)
            print(f"✅ Веб-сервер '{server.hostname}' добавлен")
            print(f"💡 Чтобы активировать сервер, используйте активацию (будет в следующей версии)")
        except DuplicateItemError as e:
            print(f"❌ Ошибка: {e}")
        except InvalidInputError as e:
            print(f"❌ Ошибка ввода: {e}")
    
    def _add_database_server(self) -> None:
        """Добавляет сервер БД."""
        print("\n--- Добавление сервера БД ---")
        try:
            hostname = input("Имя хоста: ").strip()
            if not hostname:
                raise InvalidInputError("Имя хоста не может быть пустым")
            
            ip_address = input("IP-адрес: ").strip()
            if not ip_address:
                raise InvalidInputError("IP-адрес не может быть пустым")
            
            db_type = input("Тип БД (PostgreSQL/MySQL/MongoDB): ").strip()
            if not db_type:
                db_type = "PostgreSQL"
            
            storage = int(input("Объём хранилища (GB): ") or 500)
            
            server = self._app.add_database_server(hostname, ip_address, db_type, storage, 200, "inactive")
            print(f"✅ Сервер БД '{server.hostname}' добавлен")
        except DuplicateItemError as e:
            print(f"❌ Ошибка: {e}")
        except ValueError:
            print("❌ Ошибка: объём хранилища должен быть числом")
        except InvalidInputError as e:
            print(f"❌ Ошибка ввода: {e}")
    
    def _add_file_server(self) -> None:
        """Добавляет файловый сервер."""
        print("\n--- Добавление файлового сервера ---")
        try:
            hostname = input("Имя хоста: ").strip()
            if not hostname:
                raise InvalidInputError("Имя хоста не может быть пустым")
            
            ip_address = input("IP-адрес: ").strip()
            if not ip_address:
                raise InvalidInputError("IP-адрес не может быть пустым")
            
            protocol = input("Протокол (FTP/SMB/NFS): ").strip()
            if not protocol:
                protocol = "FTP"
            
            server = self._app.add_file_server(hostname, ip_address, protocol, 150, "inactive")
            print(f"✅ Файловый сервер '{server.hostname}' добавлен")
        except DuplicateItemError as e:
            print(f"❌ Ошибка: {e}")
        except InvalidInputError as e:
            print(f"❌ Ошибка ввода: {e}")
    
    def _find_by_name(self) -> None:
        """Поиск сервера по имени."""
        print("\n--- Поиск по имени ---")
        name = input("Введите имя хоста: ").strip()
        if not name:
            print("❌ Имя не может быть пустым")
            return
        
        server = self._app.find_by_name(name)
        if server:
            print(f"\n✅ Найден:")
            print(f"   Имя: {server.hostname}")
            print(f"   IP: {server.ip_address}")
            print(f"   Тип: {server.get_server_type()}")
            print(f"   Статус: {server.status}")
            print(f"   Нагрузка: {server.calculate_load():.1f}%")
        else:
            print(f"❌ Сервер с именем '{name}' не найден")
            raise ItemNotFoundError(f"Сервер с именем {name} не найден")
    
    def _find_by_ip(self) -> None:
        """Поиск сервера по IP."""
        print("\n--- Поиск по IP ---")
        ip = input("Введите IP-адрес: ").strip()
        if not ip:
            print("❌ IP не может быть пустым")
            return
        
        server = self._app.find_by_ip(ip)
        if server:
            print(f"\n✅ Найден:")
            print(f"   Имя: {server.hostname}")
            print(f"   IP: {server.ip_address}")
            print(f"   Тип: {server.get_server_type()}")
            print(f"   Статус: {server.status}")
            print(f"   Нагрузка: {server.calculate_load():.1f}%")
        else:
            print(f"❌ Сервер с IP '{ip}' не найден")
            raise ItemNotFoundError(f"Сервер с IP {ip} не найден")
    
    def _show_active_servers(self) -> None:
        """Показывает только активные серверы."""
        servers = self._app.get_active_servers()
        if not servers:
            print("\n⚠️ Активных серверов нет.")
            return
        
        print("\n--- АКТИВНЫЕ СЕРВЕРЫ ---")
        for s in servers:
            print(f"   🟢 {s.hostname} ({s.ip_address}) - {s.get_server_type()} - нагрузка: {s.calculate_load():.1f}%")
    
    def _sort_servers(self) -> None:
        """Меню сортировки."""
        print("\n--- СОРТИРОВКА ---")
        print("1. По имени (А → Я)")
        print("2. По имени (Я → А)")
        print("3. По нагрузке (возрастание)")
        print("4. По нагрузке (убывание)")
        
        try:
            choice = int(input("Выберите тип сортировки: "))
            
            if choice == 1:
                self._app.sort_by_hostname(reverse=False)
                print("✅ Отсортировано по имени (А → Я)")
            elif choice == 2:
                self._app.sort_by_hostname(reverse=True)
                print("✅ Отсортировано по имени (Я → А)")
            elif choice == 3:
                self._app.sort_by_load(reverse=False)
                print("✅ Отсортировано по нагрузке (возрастание)")
            elif choice == 4:
                self._app.sort_by_load(reverse=True)
                print("✅ Отсортировано по нагрузке (убывание)")
            else:
                print("❌ Неверный выбор")
                return
            
            self._show_servers()
        except ValueError:
            print("❌ Ошибка: введите число от 1 до 4")
    
    def _delete_server(self) -> None:
        """Удаление сервера с подтверждением."""
        print("\n--- УДАЛЕНИЕ СЕРВЕРА ---")
        ip = input("Введите IP-адрес сервера для удаления: ").strip()
        if not ip:
            print("❌ IP не может быть пустым")
            return
        
        server = self._app.find_by_ip(ip)
        if not server:
            print(f"❌ Сервер с IP '{ip}' не найден")
            raise ItemNotFoundError(f"Сервер с IP {ip} не найден")
        
        print(f"\n⚠️ Сервер: {server.hostname} ({server.ip_address})")
        confirm = input(f"Удалить сервер '{server.hostname}'? (y/n): ").lower()
        
        if confirm == 'y':
            self._app.delete_server_by_ip(ip)
            print(f"✅ Сервер '{server.hostname}' удалён")
        else:
            print("❌ Удаление отменено")
    
    def run(self) -> None:
        """Запуск основного цикла приложения."""
        print("\n" + "="*50)
        print("   ДОБРО ПОЖАЛОВАТЬ В IT-INFRA MANAGER")
        print("="*50)
        
        while self._running:
            try:
                self._display_menu()
                choice = self._get_choice()
                
                if choice == 1:
                    self._show_servers()
                elif choice == 2:
                    self._add_web_server()
                elif choice == 3:
                    self._add_database_server()
                elif choice == 4:
                    self._add_file_server()
                elif choice == 5:
                    self._find_by_name()
                elif choice == 6:
                    self._find_by_ip()
                elif choice == 7:
                    self._show_active_servers()
                elif choice == 8:
                    self._sort_servers()
                elif choice == 9:
                    self._delete_server()
                elif choice == 0:
                    print("\n👋 До свидания! Данные сохранены.")
                    self._running = False
                else:
                    print("❌ Неверный пункт. Выберите от 0 до 9.")
            
            except ItemNotFoundError as e:
                print(f"⚠️ {e}")
            except DuplicateItemError as e:
                print(f"⚠️ {e}")
            except InvalidInputError as e:
                print(f"⚠️ {e}")
            except Exception as e:
                print(f"⚠️ Непредвиденная ошибка: {e}")