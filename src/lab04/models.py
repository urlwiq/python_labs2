from lab03.base import Server
from lab04.interfaces import IComparable, IPrintable

class WebServer(Server, IComparable, IPrintable):
    def __init__(self, hostname, ip_address, domain, max_connections=100, status="inactive", ssl_enabled=False):
        super().__init__(hostname, ip_address, max_connections, status)
        self._domain = domain
        self._ssl_enabled = ssl_enabled
        self._requests = 0
    
    @property
    def domain(self):
        return self._domain
    
    @property
    def ssl_enabled(self):
        return self._ssl_enabled
    
    def handle_request(self):
        if self._status != "active":
            raise Exception("Сервер не активен")
        self._requests += 1
        print(f"Веб-сервер {self._hostname} обработал запрос #{self._requests}")
        return True
    
    def get_http_status(self):
        return "200 OK" if self._status == "active" else "503 Service Unavailable"
    
    def calculate_load(self):
        base_load = super().calculate_load()
        return min(100, base_load + self._requests * 0.5)
    
    def get_server_type(self):
        return "Web Server"
    
    def get_info(self):
        ssl_str = "Да" if self._ssl_enabled else "Нет"
        return f"WebServer {self._hostname} | {self._domain} | SSL: {ssl_str}"
    
    def compare_to(self, other):
        if not isinstance(other, WebServer):
            return -1
        if self._hostname < other._hostname:
            return -1
        elif self._hostname > other._hostname:
            return 1
        return 0
    
    def to_string(self):
        return (f"[WebServer] {self._hostname} | Домен: {self._domain} | "
                f"SSL: {self._ssl_enabled} | Запросов: {self._requests}")
    
    def __str__(self):
        return (f"🌐 {self.get_server_type()} {self._hostname} ({self._ip_address})\n"
                f"   Домен: {self._domain}\n"
                f"   SSL: {'Включен' if self._ssl_enabled else 'Выключен'}\n"
                f"   Запросов: {self._requests}\n"
                f"   Нагрузка: {self.calculate_load():.1f}%")


class DatabaseServer(Server, IComparable, IPrintable):
    def __init__(self, hostname, ip_address, db_type, storage_gb, max_connections=200, status="inactive"):
        super().__init__(hostname, ip_address, max_connections, status)
        self._db_type = db_type
        self._storage_gb = storage_gb
        self._queries = 0
    
    @property
    def db_type(self):
        return self._db_type
    
    @property
    def storage_gb(self):
        return self._storage_gb
    
    def execute_query(self, query):
        if self._status != "active":
            raise Exception("БД не активна")
        self._queries += 1
        print(f"БД {self._hostname} выполнила запрос #{self._queries}")
        return True
    
    def get_free_space(self):
        return self._storage_gb * 0.3
    
    def calculate_load(self):
        base_load = super().calculate_load()
        return min(100, base_load + self._queries * 0.3)
    
    def get_server_type(self):
        return "Database Server"
    
    def get_info(self):
        return f"DatabaseServer {self._hostname} | Тип: {self._db_type} | Место: {self._storage_gb}GB"
    
    def compare_to(self, other):
        if not isinstance(other, DatabaseServer):
            return -1
        if self.calculate_load() < other.calculate_load():
            return -1
        elif self.calculate_load() > other.calculate_load():
            return 1
        return 0
    
    def to_string(self):
        return (f"[DatabaseServer] {self._hostname} | Тип: {self._db_type} | "
                f"Место: {self._storage_gb}GB | Запросов: {self._queries}")
    
    def __str__(self):
        return (f"🗄️ {self.get_server_type()} {self._hostname} ({self._ip_address})\n"
                f"   Тип БД: {self._db_type}\n"
                f"   Место: {self._storage_gb} GB\n"
                f"   Запросов: {self._queries}\n"
                f"   Нагрузка: {self.calculate_load():.1f}%")


class FileServer(Server, IPrintable):
    def __init__(self, hostname, ip_address, protocol, max_connections=150, status="inactive"):
        super().__init__(hostname, ip_address, max_connections, status)
        self._protocol = protocol
        self._files = 0
        self._total_size_mb = 0
    
    @property
    def protocol(self):
        return self._protocol
    
    @property
    def files(self):
        return self._files
    
    def upload_file(self, filename, size_mb=1):
        if self._status != "active":
            raise Exception("Сервер не активен")
        self._files += 1
        self._total_size_mb += size_mb
        print(f"Файл '{filename}' ({size_mb}MB) загружен на {self._hostname}")
        return True
    
    def get_avg_file_size(self):
        if self._files == 0:
            return 0
        return self._total_size_mb / self._files
    
    def calculate_load(self):
        base_load = super().calculate_load()
        return min(100, base_load + self._files * 2)
    
    def get_server_type(self):
        return "File Server"
    
    def get_info(self):
        return f"FileServer {self._hostname} | Протокол: {self._protocol} | Файлов: {self._files}"
    
    def to_string(self):
        return (f"[FileServer] {self._hostname} | Протокол: {self._protocol} | "
                f"Файлов: {self._files} | Размер: {self._total_size_mb}MB")
    
    def __str__(self):
        return (f"📁 {self.get_server_type()} {self._hostname} ({self._ip_address})\n"
                f"   Протокол: {self._protocol}\n"
                f"   Файлов: {self._files}\n"
                f"   Размер: {self._total_size_mb} MB\n"
                f"   Нагрузка: {self.calculate_load():.1f}%")